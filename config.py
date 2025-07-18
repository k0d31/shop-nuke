import os
from dotenv import load_dotenv

load_dotenv()  # Загружает .env файл

config = {
    "token": os.getenv("TOKEN"),
}
