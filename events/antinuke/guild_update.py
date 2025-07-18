import disnake
import datetime
from disnake.ext import commands, tasks
from db.db import Database
from utils.quarantinenotmember import add_to_quarantinenotmember
from utils.restorevanityurl import restore_vanity_url

db = Database("db/db.db")

class GuildUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warning_counts = {}
        self.previous_guild_states = {}
        self.delete_warns.start()

    @tasks.loop(minutes=10)
    async def delete_warns(self):
        for author, warns in self.warning_counts.items():
            if warns >= 1:
                self.warning_counts[author] -= 1

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        guild = after
        data_settings = await db.get_infomainsettings(guild.id)

        quarantine_role = guild.get_role(int(data_settings[2]))
        booster_role = guild.get_role(int(data_settings[1]))

        if not quarantine_role or not booster_role:
            warning_channel = self.bot.get_channel(data_settings[4])
            if warning_channel:
                await warning_channel.send("Роли quarantine или booster не найдены. Проверьте настройки.")
            return
        
        entry = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.guild_update).flatten()
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
        
        if author.id == 1222210757329162281:
            return

        await self.check_and_apply_sanctions(author, before, after, data_settings, quarantine_role, booster_role)

        await self.rollback_guild_changes(before, after, data_settings)

    async def check_and_apply_sanctions(self, author, before, after, data_settings, quarantine_role, booster_role):
        guild = after

        embed = disnake.Embed(
            title="Пользователь отправлен в карантин",
            color=disnake.Color.red()
        )
        embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}", inline=False)
        embed.add_field(name="Действие", value="Изменение гильдии", inline=False)

        embeduser = disnake.Embed(
            title="Вы были отправлены в карантин",
            description=f"{author.mention}, вы были отправлены в карантин на сервере {guild.name} за изменение гильдии",
            color=disnake.Color.red()
        )

        roles_data = await db.get_anticrashrole(guild.id, author.top_role.id)
        user_data = await db.get_anticrashuser(guild.id, author.id)

        if not roles_data and not user_data:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        if (roles_data and roles_data[0][2] == 'false') or (user_data and user_data[0][2] == 'false'):
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        ban_value = None
        if roles_data:
            ban_value = roles_data[0][2]
        elif user_data:
            ban_value = user_data[0][2]

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
                warning_embed.add_field(name="Действие", value=f"Изменение гильдии было откатано. Осталось предупреждений: {remaining_warnings}/{ban_value}", inline=False)
                await warning_channel.send(embed=warning_embed)

    async def rollback_guild_changes(self, before, after, data_settings):
        guild = after

        if before.name != after.name:
            await guild.edit(name=before.name)
        if before.description != after.description:
            await guild.edit(description=before.description)
        if before.afk_timeout != after.afk_timeout:
            await guild.edit(afk_timeout=before.afk_timeout)
        if before.verification_level != after.verification_level:
            await guild.edit(verification_level=before.verification_level)
        if before.explicit_content_filter != after.explicit_content_filter:
            await guild.edit(explicit_content_filter=before.explicit_content_filter)

def setup(bot):
    bot.add_cog(GuildUpdate(bot))
