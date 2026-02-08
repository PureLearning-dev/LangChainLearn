from dotenv import load_dotenv

from src.models import deep_seek_mode

load_dotenv()

response = deep_seek_mode(
    "请翻译以下对话：hello, How are you?"
)

print(response.content)
