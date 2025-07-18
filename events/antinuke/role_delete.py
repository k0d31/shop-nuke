import disnake
import datetime
from disnake.ext import commands, tasks
from db.db import Database
from utils.quarantinenotmember import add_to_quarantinenotmember

db = Database("db/db.db")

class RoleDelete(commands.Cog):
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
    async def on_guild_role_delete(self, role):
        guild = self.bot.get_guild(role.guild.id)
        data_settings = await db.get_infomainsettings(guild.id)
    
        quarantine_role = guild.get_role(int(data_settings[2]))
        booster_role = guild.get_role(int(data_settings[1]))

        if not quarantine_role or not booster_role:
            channel = self.bot.get_channel(data_settings[4])
            if channel:
                await channel.send("Роли quarantine или booster не найдены. Проверьте настройки.")
            return

        entry = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete).flatten()
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
        embed.add_field(name="Действие", value=f"Удаление роли - `{role.name}`", inline=False)

        embeduser = disnake.Embed(
            title="Вы были отправлены в карантин",
            description=f"{author.mention}, вы были отправлены в карантин на сервере {guild.name} за удаление роли - `{role.name}`",
            color=disnake.Color.red()
        )

        if not roles_data and not user_data:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            await self.recreate_role(guild, role)
            return

        if (roles_data and roles_data[0][13] == 'false') or (user_data and user_data[0][13] == 'false'):
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            await self.recreate_role(guild, role)
            return

        ban_value = None
        if roles_data:
            ban_value = roles_data[0][13]
        elif user_data:
            ban_value = user_data[0][13]

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
            await self.recreate_role(guild, role)
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
                warning_embed.add_field(name="Действие", value=f"Удаление роли - `{role.name}`. Осталось предупреждений: {remaining_warnings}/{ban_value}", inline=False)
                await warning_channel.send(embed=warning_embed)

    async def recreate_role(self, guild, old_role):
        name = old_role.name
        permissions = old_role.permissions
        position = old_role.position
        icon = old_role.icon
        emoji = old_role.emoji
        color = old_role.colour
        new_role = await guild.create_role(name=name, permissions=permissions, color=color, icon=icon, emoji=emoji)
        try:
            await new_role.edit(position=position)
        except:
            pass
        for member in guild.members:
            if old_role in member.roles:
                await member.add_roles(new_role)

def setup(bot):
    bot.add_cog(RoleDelete(bot))
