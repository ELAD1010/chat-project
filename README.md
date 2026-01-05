## Rift — Online Chat in Python

Rift is a Python-based chat project with:
- a **socket server** for real-time connections
- a **Flask HTTP API** for authentication and fetching conversations
- a **NiceGUI desktop UI** (dark WhatsApp-web style) with login/register + loading + chat views

---

## Tech Stack

- **Python 3.10+**
- **NiceGUI** (UI)
- **Flask** (HTTP API)
- **Sockets (TCP)** (real-time transport + handshake)
- **SQLAlchemy + SQLite** (persistence)
- **python-dotenv** (environment configuration)
- **requests** (used by the CLI client)

---

## Project Structure (high level)

- `server/`: socket server + Flask HTTP server + DB services
- `client/ui/`: NiceGUI UI app
- `client/main.py`: CLI socket client (separate from the UI)
- `run_server.py`: server entrypoint
- `run_client.py`: CLI client entrypoint

---

## Prerequisites

- Python installed and available on PATH (`python --version`)
- (Recommended) a virtual environment

---

## Setup

### 1) Create and activate a virtual environment

**Windows (PowerShell)**

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

This repo currently doesn’t ship a `requirements.txt`, so install the core libraries manually:

```bash
pip install nicegui flask sqlalchemy python-dotenv requests
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
IP=127.0.0.1
PORT=5001
HTTP_PORT=5000
DB_NAME=rift
```

- **`IP`**: bind/target address
- **`PORT`**: TCP socket server port
- **`HTTP_PORT`**: Flask HTTP API port
- **`DB_NAME`**: SQLite database filename prefix (creates `<DB_NAME>.db`)

---

## Running

### 1) Start the server

From the repo root:

```bash
python run_server.py
```

This starts:
- a TCP socket server at `IP:PORT`
- a Flask API at `http://IP:HTTP_PORT`

### 2) Start the UI (NiceGUI desktop app)

In a new terminal:

```bash
python client/ui/chat.py
```

You’ll land on the **Login** page by default.  
Successful auth shows a short **loading screen**, then the **Chats** UI.

### (Optional) Run the CLI socket client

In a new terminal:

```bash
python run_client.py
```

---

## Notes / Current Behavior

- Auth functions are currently **dummy** and live in `client/ui/authentication.py`.
- Chat list + message data are currently **dummy** and live in `client/ui/fetch_chat_data.py`.
- The UI is modularized under `client/ui/` (see `client/ui/UI_FOLDER_SUMMARY.txt` for per-file details).

---

## Troubleshooting

- **App can’t connect / wrong ports**: double-check `.env` values and that `run_server.py` is running.
- **PowerShell activation blocked**: run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then re-activate the venv.
- **Module import errors in UI**: make sure you run it as `python client/ui/chat.py` from the repo root (or run it directly from that folder).

