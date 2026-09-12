from unittest.mock import MagicMock, patch

import pytest

from core.bridge import LightroomBridge


def test_bridge_get_token(tmp_path):
    token_file = tmp_path / "token"
    token_file.write_text("test_token_12345", encoding="utf-8")

    b = LightroomBridge(auth_file_path=str(token_file))
    assert b.get_token() == "test_token_12345"


def test_bridge_get_token_missing():
    b = LightroomBridge(auth_file_path="/non/existent/token/path")
    with pytest.raises(FileNotFoundError):
        b.get_token()


@patch("socket.socket")
def test_bridge_execute_success(mock_socket_class, tmp_path):
    token_file = tmp_path / "token"
    token_file.write_text("valid_token", encoding="utf-8")

    resp_mock = MagicMock()
    req_mock = MagicMock()

    # Configure mock socket instances
    mock_socket_class.side_effect = [resp_mock, req_mock]

    # Mock recv to return a valid JSON response with matched ID
    b = LightroomBridge(auth_file_path=str(token_file))

    def fake_sendall(data):
        import json
        req = json.loads(data.decode("utf-8").strip())
        req_id = req["id"]
        resp_payload = json.dumps({"id": req_id, "result": {"photos": [{"id": 101}]}}) + "\n"
        resp_mock.recv.return_value = resp_payload.encode("utf-8")

    req_mock.sendall.side_effect = fake_sendall

    res = b.execute("get_selected_photos", {"limit": 10})
    assert res == {"photos": [{"id": 101}]}
