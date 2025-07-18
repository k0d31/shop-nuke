import disnake
from disnake.ext import commands
from db.db import Database
from utils.restore_roles import RoleRestoreView

db = Database("db/db.db")

async def add_to_quarantine(bot, guild, author, member, embed, embeduser, quarantine_role, booster_role, data_settings):
    roles = [role.id for role in author.roles[1:]][::-1]

    try:
        if booster_role in author.roles:
            await author.edit(roles=[quarantine_role, booster_role])
        else:
            await author.edit(roles=[quarantine_role])

        channel = bot.get_channel(data_settings[4])
        if channel:
            embed.add_field(name = "Роли пользователя", value = ''.join([f'<@&{role_id}>\n' for role_id in roles]), inline=False)
            msg = await channel.send(embed=embed, view = RoleRestoreView(bot, guild.id, author.id, embed))
            await db.add_quarantineduser(msg.id, author.id, '0')
            await db.add_quarantinedroles(msg.id, author.id, ','.join(map(str, roles)))

        try:
            await author.send(embed = embeduser)
        except disnake.Forbidden:
            pass

    except Exception as e:
        print(f"Ошибка при отправке пользователя в карантин: {e}")