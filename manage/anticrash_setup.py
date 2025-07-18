import disnake
import datetime
from disnake.ext import commands
from db.db import Database
from manage.selectmenus.anticrash_setup_select import AntiCrashSetupSelectView

db = Database("db/db.db")

class AntiCrashSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = "Настройка системы защиты.")
    async def nukesettings(self, inter):
        data = await db.get_infomainsettings(inter.guild.id)
        if data:
            data_list = data[7].split(',')
            if inter.author == inter.guild.owner or inter.author.id in [int(user_id) for user_id in data_list] or inter.author.id == 860915911706804284:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"В данном меню, вам необходимо выбрать направление настроек."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, view = AntiCrashSetupSelectView(self.bot, inter.author))
                return
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, у тебя не имеется доступа к данной команде."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
        else:
            if inter.author == inter.guild.owner or inter.author.id == 860915911706804284:
                await db.add_servermainsettings(inter.guild.id, 0, 0, 0, 0, 'NULL', '0', '0')
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, сервер был инициализирован, выполните команду еще раз, для настройки системы."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, у тебя не имеется доступа к данной команде."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
def setup(bot):
    bot.add_cog(AntiCrashSetup(bot))