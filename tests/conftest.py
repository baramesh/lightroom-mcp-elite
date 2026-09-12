from unittest.mock import MagicMock

import pytest

from core.bridge import LightroomBridge


@pytest.fixture
def mock_bridge(monkeypatch):
    """Mock LightroomBridge for isolated unit testing."""
    mock = MagicMock(spec=LightroomBridge)
    monkeypatch.setattr("tools.selection.bridge", mock)
    monkeypatch.setattr("tools.develop.bridge", mock)
    monkeypatch.setattr("tools.organization.bridge", mock)
    monkeypatch.setattr("tools.coop.bridge", mock)
    return mock
