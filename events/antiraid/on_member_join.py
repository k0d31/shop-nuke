import disnake
import datetime
from disnake.ext import commands
from db.db import Database
from config import config


db = Database("db/db.db")

class AntiRaidJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        data = await db.get_antiraid(guild.id)
        owner_id = config['owner_id']

        if data[3] == 1:
            timereguser = member.created_at
            time_nuke = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=data[2])

            if timereguser > time_nuke:
                embedlog = disnake.Embed(
                    title='Nuke',
                    description=f'Заблокировала участника {member.mention}, его аккаунт был создан `{timereguser.strftime("%Y-%m-%d")}`'
                )
                embedlog.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
                embedlog.set_thumbnail(url=member.display_avatar.url)
                
                log_channel = self.bot.get_channel(data[1])
                if log_channel:
                    await log_channel.send(embed=embedlog)

                embed = disnake.Embed(
                    title='Nuke',
                    description=(
                        f'Привет! {member.mention}, нам очень жаль, но наша система посчитала твой аккаунт подозрительным и заблокировала его.\n'
                        f'Для входа на сервер, твоему аккаунту должно быть больше {data[2]} дней.'
                    )
                )
                embed.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
                embed.set_thumbnail(url=member.display_avatar.url)
                
                try:
                    await member.send(embed=embed)
                except disnake.Forbidden:
                    print(f"Не удалось отправить сообщение {member.mention}.")

                await member.ban(reason=f"AntiNuke < {data[2]} days :3")
            else:
                embedlog = disnake.Embed(
                    title='Nuke',
                    description=f'Участник зашел на сервер {member.mention}, его аккаунт был создан `{timereguser.strftime("%Y-%m-%d %H:%M:%S")}`'
                )
                embedlog.set_author(name=guild.name, icon_url=guild.icon.url if guild.icon else None)
                embedlog.set_thumbnail(url=member.display_avatar.url)
                
                log_channel = self.bot.get_channel(data[1])
                if log_channel:
                    await log_channel.send(embed=embedlog)


def setup(bot):
    bot.add_cog(AntiRaidJoin(bot))
