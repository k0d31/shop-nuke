import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "token": os.getenv("TOKEN"),
    "owner_id": int(os.getenv("OWNER_ID", 0))
}
