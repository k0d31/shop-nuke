import disnake
from disnake.ext import commands
from disnake.ui import View, Button
from db.db import Database

db = Database("db/db.db")

class RoleRestoreView(View):
    def __init__(self, bot, guild_id, user_id, embed):
        super().__init__()
        self.bot = bot
        self.guild_id = guild_id
        self.user_id = user_id
        self.embed = embed

        self.add_item(disnake.ui.Button(label = "Восстановить роли", style = disnake.ButtonStyle.success, custom_id = 'accept_restore'))
        self.add_item(disnake.ui.Button(label = "Отклонить", style = disnake.ButtonStyle.danger, custom_id = 'deny_restore'))