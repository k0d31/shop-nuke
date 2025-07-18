import requests
import json
from db.db import Database
from config import config

db = Database("db/db.db")


async def restore_vanity_url(guild):
    data = await db.get_infomainsettings(guild.id)
    
    vanity_code = data[5]
    if not vanity_code:
        print("Vanity URL code is missing.")
        return

    token = config['usertoken']

    headers = {
        'Authorization': f'{token}',
        'Content-Type': 'application/json'
    }

    url = f'https://discord.com/api/v9/guilds/{guild.id}/vanity-url'

    payload = {
        'code': vanity_code
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Guild link updated successfully to {vanity_code}")
    except requests.RequestException as e:
        print(f"Failed to update guild link. Error: {e}")
