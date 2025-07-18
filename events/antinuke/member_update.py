import disnake
import datetime
from disnake.ext import commands, tasks
from db.db import Database
from utils.quarantinenotmember import add_to_quarantinenotmember

db = Database("db/db.db")


class MemberUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warning_counts = {}
        self.allowed_role_ids = [1275189842883383307, 1275189843948736553, 1275189845148565505, 1275189846406598738,
                                 1275189856011681986, 1275189857374834710, 1275189857374834710, 1275189855042928798,
                                 1275189858129936408, 1275189847656497174, 1275189853902077953]
        self.delete_warns.start()


    @tasks.loop(minutes=10)
    async def delete_warns(self):
        for author, warns in self.warning_counts.items():
            if warns >= 1:
                self.warning_counts[author] -= 1

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = before.guild
        data_settings = await db.get_infomainsettings(guild.id)

        quarantine_role = guild.get_role(int(data_settings[2]))
        booster_role = guild.get_role(int(data_settings[1]))

        if not quarantine_role or not booster_role:
            notify_channel = self.bot.get_channel(data_settings[4])
            if notify_channel:
                await notify_channel.send("Роли quarantine или booster не найдены. Проверьте настройки.")
            return

        logs = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.member_role_update).flatten()

        entry = logs[0] if logs else None
        if not entry:
            return

        log_creation_time = entry.created_at
        now = datetime.datetime.now(datetime.timezone.utc)
        if now - log_creation_time > datetime.timedelta(minutes=1):
            return

        author = entry.user

        if before.roles != after.roles or after.roles != before.roles:
            before_roles = set(before.roles)
            after_roles = set(after.roles)

            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles

            for role in added_roles:
                if role.id in self.allowed_role_ids:
                    print('Role added: {}'.format(role.name))
                    return

            for role in removed_roles:
                if role.id in self.allowed_role_ids:
                    print('Role removed: {}'.format(role.name))
                    return

            if author.top_role >= guild.me.top_role:
                return

            if author.id in [int(user_id) for user_id in data_settings[6].split(',')]:
                return

            await self.role_quarantine(guild, author, before, after, data_settings, quarantine_role, booster_role)

        if before.current_timeout != after.current_timeout or after.current_timeout != before.current_timeout:

            if author.top_role >= guild.me.top_role:
                return

            if author.id in [int(user_id) for user_id in data_settings[6].split(',')]:
                return

    async def role_quarantine(self, guild, author, before, after, data_settings, quarantine_role, booster_role):

        roles_data = await db.get_anticrashrole(guild.id, author.top_role.id)
        user_data = await db.get_anticrashuser(guild.id, author.id)



        embed = disnake.Embed(
            title="Пользователь отправлен в карантин",
            color=disnake.Color.red()
        )
        embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}", inline=False)
        embed.add_field(name="Действие", value=f"Обновление - {before.mention}", inline=False)

        embeduser = disnake.Embed(
            title="Вы были отправлены в карантин",
            description=f"{author.mention}, вы были отправлены в карантин на сервере {guild.name} за обновление - `{before.name}`",
            color=disnake.Color.red()
        )

        if not roles_data and not user_data:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        if (roles_data and roles_data[0][9] == 'false') or (user_data and user_data[0][9] == 'false'):
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        ban_value = None
        if roles_data:
            ban_value = roles_data[0][9]
        elif user_data:
            ban_value = user_data[0][9]

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
            await after.edit(
                nick=before.nick,
                roles=before.roles
            )
            del self.warning_counts[author.id]
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role,
                                             booster_role,
                                             data_settings)
        else:
            warning_channel = self.bot.get_channel(data_settings[3])
            remaining_warnings = ban_value - self.warning_counts[author.id]
            if warning_channel:
                warning_embed = disnake.Embed(
                    title="Предупреждение",
                    color=disnake.Color.yellow()
                )
                warning_embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}",
                                        inline=False)
                warning_embed.add_field(name="Действие",
                                        value=f"Обновление ролей - {before.mention}. Осталось предупреждений: {remaining_warnings}/{ban_value}",
                                        inline=False)
                await warning_channel.send(embed=warning_embed)

    async def member_quarantine(self, guild, author, before, after, data_settings, quarantine_role, booster_role):
        roles_data = await db.get_anticrashrole(guild.id, author.top_role.id)
        user_data = await db.get_anticrashuser(guild.id, author.id)

        embed = disnake.Embed(
            title="Пользователь отправлен в карантин",
            color=disnake.Color.red()
        )
        embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}", inline=False)
        embed.add_field(name="Действие", value=f"Выдача таймаута - {before.mention}", inline=False)

        embeduser = disnake.Embed(
            title="Вы были отправлены в карантин",
            description=f"{author.mention}, вы были отправлены в карантин на сервере {guild.name} за обновление - `{before.name}`",
            color=disnake.Color.red()
        )

        if not roles_data and not user_data:
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        if (roles_data and roles_data[0][16] == 'false') or (user_data and user_data[0][16] == 'false'):
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role, booster_role, data_settings)
            return

        ban_value = None
        if roles_data:
            ban_value = roles_data[0][16]
        elif user_data:
            ban_value = user_data[0][16]

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
            await after.edit(
                current_timeout = before.current_timeout
            )
            del self.warning_counts[author.id]
            await add_to_quarantinenotmember(self.bot, guild, author, embed, embeduser, quarantine_role,
                                             booster_role,
                                             data_settings)
        else:
            warning_channel = self.bot.get_channel(data_settings[3])
            remaining_warnings = ban_value - self.warning_counts[author.id]
            if warning_channel:
                warning_embed = disnake.Embed(
                    title="Предупреждение",
                    color=disnake.Color.yellow()
                )
                warning_embed.add_field(name="Пользователь", value=f"{author.mention} | {author} | {author.id}",
                                        inline=False)
                warning_embed.add_field(name="Действие",
                                        value=f"Выдача таймаута - {before.mention}. Осталось предупреждений: {remaining_warnings}/{ban_value}",
                                        inline=False)
                await warning_channel.send(embed=warning_embed)


def setup(bot):
    bot.add_cog(MemberUpdate(bot))
