import requests
from client.config.app_config import AppConfig

def get_user_conversations(user_id: str):
    app_config = AppConfig()
    try:
        res = requests.get(f'http://{app_config.ip}:{app_config.http_port}/conversations/{user_id}')
        conversations = res.json()
        return conversations
    except Exception as e:
        print(f"Get Conversations Error: {e}")
        return []

def get_conversation_messages(conversation_id: str):
    app_config = AppConfig()
    try:
        res = requests.get(f'http://{app_config.ip}:{app_config.http_port}/messages/{conversation_id}')
        print(res)
        messages = res.json()
        return messages
    except Exception as e:
        print(f"Get Messages Error: {e}")
        return []

def get_all_users():
    app_config = AppConfig()
    try:
        res = requests.get(f'http://{app_config.ip}:{app_config.http_port}/users')
        return res.json()
    except Exception as e:
        print(f"Get Users Error: {e}")
        return []

def create_conversation(name: str, type: int, members: list[str]):
    app_config = AppConfig()
    try:
        data = {
            "name": name,
            "type": type,
            "members": members
        }
        res = requests.post(f'http://{app_config.ip}:{app_config.http_port}/conversations', json=data)
        return res.json()
    except Exception as e:
        print(f"Create Conversation Error: {e}")
        return None

def get_conversation(conversation_id: str, user_id: str = None):
    app_config = AppConfig()
    try:
        url = f'http://{app_config.ip}:{app_config.http_port}/conversation/{conversation_id}'
        if user_id:
            url += f'?user_id={user_id}'
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        print(f"Get Conversation Error: {e}")
        return None