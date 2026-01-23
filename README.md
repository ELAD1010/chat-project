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
- `client/main.py`: Main client application entry point (connects UI & Sockets)
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

Run the following command in your terminal to install all the necessary libraries.

```bash
pip install -r requirements.txt
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


### 2) Run the client
Run the following command in a separate terminal:

```python
python run_client.py
```
You should see the UI open up a few moments after executing this. 
You will land on the login page:

![loginpage](/readme-images/loginpage.png)

In the bottom of the form, you will find the *Register Now* button. It will redirect you to the register page.

![registerpage](/readme-images/registerpage.png)

Fill out your email and password, and click the *register* button.

Great job! You are now successfully a Rift user!

After clicking register, you will be directed to the chat app, as demonstrated in the figure below.

![welcome-page](/readme-images/welcome-page.png)

For now, you don't see any open chats. That's alright, because you simply haven't initiated any conversation!

To start a new conversation, press the "+" button at the top of the left sidebar. 
A modal should appear with a list of existing users.

![users-choose](/readme-images/chat-lists.png)

Choose a user to start a new conversation with them.

You can send messages via the bottom input bar.

![messages](/readme-images/messages.png)

You could also share different emojis. To do that, click the smiley icon at the bottom input bar. It will open an emoji picker. We are also working on adding support for GIFs, so stay tuned for version updates.

![emoji-picker](/readme-images/emoji-picker.png)


## Troubleshooting

- **App can’t connect / wrong ports**: Double-check `.env` values and that `run_server.py` is running.
- **Connecting from another PC**: Ensure your server binds to `0.0.0.0` (in `.env`) and that your firewall allows traffic on the configured ports.
- **PowerShell activation blocked**: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then re-activate the venv.
- **Module import errors**: Always run the app using `python run_client.py` from the root directory.


