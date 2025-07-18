import disnake
import datetime
from disnake.ext import commands, tasks
from db.db import Database
from utils.quarantinenotmember import add_to_quarantinenotmember

db = Database("db/db.db")

class ChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warning_counts = {}
        self.delete_warns.start()

    @tasks.loop(minutes=10)
    async def delete_warns(self):
        for author, warns in self.warning_counts.items():
            if warns >= 1:
                self.warning_counts[author] -= 1

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        data_settings = await db.get_infomainsettings(guild.id)
    
        quarantine_role = guild.get_role(int(data_settings[2]))
        booster_role = guild.get_role(int(data_settings[1]))

        if not quarantine_role or not booster_role:
            notify_channel = self.bot.get_channel(data_settings[4])
            if notify_channel:
                await notify_channel.send("Роли quarantine или booster не найдены. Проверьте настройки.")
            return

        entry = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete).flatten()
        entry = entry[0] if entry else None

        if not entry:
            return
        
        log_creation_time = entry.created_at

        now = datetime.datetime.now(datetime.timezone.utc)
        if now - log_creation_time > datetime.timedelta(minutes=1):
            return

        author = entry.user

        if author.top_role >= guild.me.top_role:
            return

        if author.id in [int(user_id) for user_id in data_settings[6].split(',')]:
            return


        roles_data = await db.get_anticrashrole(guild.id, author.top_role.id)
        user_data = await db.get_anticrashuser(guild.id, author.id)

        embed = disnake.Embed(
            title="Пользователь отправлен в карантин",
            color=disnake.Color.red()
        )
        embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}", inline=False)
        embed.add_field(name="Действие", value=f"Удаление канала - `{channel.name}`", inline=False)

        embeduser = disnake.Embed(
            title="Вы были отправлены в карантин",
            description=f"{author.mention}, вы были отправлены в карантин на сервере {guild.name} за удаление канала - `{channel.name}`",
            color=disnake.Color.red()
        )

        if not roles_data and not user_data:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            await self._restore_channel(channel, entry.guild)
            return

        if (roles_data and roles_data[0][5] == 'false') or (user_data and user_data[0][5] == 'false'):
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            await self._restore_channel(channel, entry.guild)
            return

        ban_value = None
        if roles_data:
            ban_value = roles_data[0][5]
        elif user_data:
            ban_value = user_data[0][5]

        if ban_value == 'true':
            return

        try:
            ban_value = int(ban_value)
        except ValueError:
            return

        if author.id not in self.warning_counts:
            self.warning_counts[author.id] = 0

        self.warning_counts[author.id] += 1

        if self.warning_counts[author.id] >= ban_value:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            await self._restore_channel(channel, entry.guild)
            del self.warning_counts[author.id]
        else:
            warning_channel = self.bot.get_channel(data_settings[3])
            remaining_warnings = ban_value - self.warning_counts[author.id]
            if warning_channel:
                warning_embed = disnake.Embed(
                    title="Предупреждение",
                    color=disnake.Color.yellow()
                )
                warning_embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}", inline=False)
                warning_embed.add_field(name="Действие", value=f"Удаление канала - `{channel.name}`. Осталось предупреждений: {remaining_warnings}/{ban_value}", inline=False)
                await warning_channel.send(embed=warning_embed)

    async def _restore_channel(self, channel, guild):
        """Восстанавливает удаленный канал с прежними настройками."""
        if channel.type == disnake.ChannelType.text:
            new_channel = await guild.create_text_channel(
                name=channel.name, 
                position=channel.position, 
                nsfw=channel.is_nsfw(), 
                category=channel.category
            )
        else:
            new_channel = await guild.create_voice_channel(
                name=channel.name, 
                position=channel.position, 
                nsfw=channel.is_nsfw(), 
                category=channel.category
            )
        overwrites = channel.overwrites
        for role, overwrite in overwrites.items():
            if isinstance(role, disnake.Role):
                new_role = guild.get_role(role.id)
                await new_channel.set_permissions(new_role, overwrite=overwrite)
            elif isinstance(role, disnake.Member):
                new_member = guild.get_member(role.id)
                await new_channel.set_permissions(new_member, overwrite=overwrite)

def setup(bot):
    bot.add_cog(ChannelDelete(bot))
