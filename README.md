# Lightroom MCP Elite (`lightroom-mcp-elite`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-brightgreen.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-2.0-orange.svg)](https://modelcontextprotocol.io/)

A high-performance, native Python **Model Context Protocol (MCP)** server for **Adobe Lightroom Classic** on macOS, featuring Develop controls, batch preset syncing, catalog curation, and seamless round-trip handoff with **Adobe Photoshop**.

---

## 🌟 Key Features

| Category | Features |
| :--- | :--- |
| **Develop & Grading** | Full control over Lightroom Develop engine: Exposure, Highlights, Shadows, Whites, Blacks, Clarity, Dehaze, Vibrance, White Balance, HSL, and Tone Curves. |
| **Preset Management** | Discover, inspect, apply, and save custom Develop presets. |
| **Photoshop Co-op** | Round-trip handoff (`lightroom_send_to_photoshop` and `lightroom_import_retouched_photo`) for surgical AI inpainting and multi-layer compositing. |
| **Catalog Curation** | Search photos, star ratings (0–5), keywords, collections, and export. |
| **Robust Architecture** | Python native socket client with automatic token retrieval from `~/.config/lightroom-mcp/token`. |

---

## 🚀 Quickstart

### Prerequisites
* macOS with Adobe Lightroom Classic (installed and running)
* `LightroomMCP.lrplugin` installed in Lightroom Classic (`File > Plug-in Manager`)
* [uv](https://docs.astral.sh/uv/) or Python 3.12+

### 1. Clone the Repository
```bash
git clone https://github.com/baramesh/lightroom-mcp-elite.git
cd lightroom-mcp-elite
```

### 2. Install Dependencies
Using `uv`:
```bash
uv sync
```

---

## ⚙️ MCP Configuration

Add `lightroom` to your MCP configuration (`~/.gemini/config/mcp_config.json` or Claude Desktop):

```json
{
  "mcpServers": {
    "lightroom": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/lightroom-mcp-elite",
        "python",
        "server.py"
      ]
    }
  }
}
```

---

## 🧠 AI Agent Skill (`SKILL.md`)

This repository includes a ready-to-use Agent Skill in `skill/SKILL.md` with:
* Non-destructive RAW development principles.
* Golden Example for Lightroom + Photoshop round-trip retouching (`skill/examples/lightroom_photoshop_coop.md`).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
