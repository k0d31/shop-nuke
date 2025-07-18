import disnake
from disnake.ext import commands
from db.db import Database
from manage.selectmenus.anticrash.anticrash_setup_role import AnticrashSetupRoleSelectView
from manage.selectmenus.anticrash.anticrash_setup_member import AnticrashSetupMemberSelectView
db = Database("db/db.db")

class AntiCrashSetupRoleSelectView(disnake.ui.View):
    def __init__(self, bot, author, data):
        self.bot = bot
        self.author = author
        self.data = data
        super().__init__()
        self.add_item(AntiCrashSetupRoleSelect(self.bot, self.author, self.data))

class AntiCrashSetupRoleSelect(disnake.ui.Select):
    def __init__(self, bot, author, data):
        self.bot = bot
        self.author = author
        self.data = data
        options = []

        role_ids = data if isinstance(data, list) else [data]
        guild_id = data[0][0] if isinstance(data[0][0], list) else [data[0][0]]
        guild = self.bot.get_guild(guild_id[0])

        for role_id in role_ids:
            role_id = role_id[1]
            role = guild.get_role(int(role_id))
            if role:
                options.append(disnake.SelectOption(label=role.name, value=str(role_id), description=str(role.id)))
            else:
                db.anticrash_deleterole(guild_id[0], role_id)

        super().__init__(placeholder="Выберите роль", min_values=1, max_values=1, options=options)

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title='Nuke',
                description=f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon)
            embed.set_thumbnail(url=inter.author.display_avatar)
            embed.set_footer(text=f"Нажал - {inter.author}", icon_url=inter.author.display_avatar)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        data = await db.get_anticrashrole(inter.guild.id, inter.values[0])

        if not data:
            await inter.response.send_message(
                "Ошибка: данные не найдены в базе данных.", ephemeral=True
            )
            return

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", "give_timeout"
        ]

        embed = disnake.Embed(
            title="Nuke",
            description=f"Вы попали в настройку параметров для роли <@&{inter.values[0]}>"
        )
        embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon)
        embed.set_thumbnail(url=inter.author.display_avatar)
        embed.set_footer(text=f"Нажал - {inter.author}", icon_url=inter.author.display_avatar)

        for i, key in enumerate(field_names, start=2):
            value = data[i]
            if value == 'true':
                status = "`Разрешено`"
            elif value == 'false':
                status = "`Запрещено`"
            else:
                status = f"`{value}`"
            
            embed.add_field(name=key, value=status, inline=True)


        await inter.response.edit_message(embed=embed, view=AnticrashSetupRoleSelectView(self.bot, inter.author, inter.values[0]))

class AntiCrashSetupUserSelectView(disnake.ui.View):
    def __init__(self, bot, author, data):
        self.bot = bot
        self.author = author
        self.data = data
        super().__init__()
        self.add_item(AntiCrashSetupUserSelect(self.bot, self.author, self.data))

class AntiCrashSetupUserSelect(disnake.ui.Select):
    def __init__(self, bot, author, data):
        self.bot = bot
        self.author = author
        self.data = data
        options = []

        user_ids = data if isinstance(data, list) else [data]
        guild_id = data[0][0] if isinstance(data[0][1], list) else [data[0][0]]

        for user_id in user_ids:
            user_id = user_id[1]
            user = self.bot.get_user(user_id)
            if user:
                options.append(disnake.SelectOption(label=user.name, value=str(user_id), description=str(user.id)))
            else:
                db.anticrash_deleteuser(guild_id, user_id)
        super().__init__(placeholder="Выберите пользователя", min_values=1, max_values=1, options=options)

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title='Nuke',
                description=f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon)
            embed.set_thumbnail(url=inter.author.display_avatar)
            embed.set_footer(text=f"Нажал - {inter.author}", icon_url=inter.author.display_avatar)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        data = await db.get_anticrashuser(inter.guild.id, inter.values[0])

        if not data:
            await inter.response.send_message(
                "Ошибка: данные не найдены в базе данных.", ephemeral=True
            )
            return

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", "give_timeout"
        ]

        embed = disnake.Embed(
            title="Nuke",
            description=f"Вы попали в настройку параметров для пользователя <@{inter.values[0]}>"
        )
        embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon)
        embed.set_thumbnail(url=inter.author.display_avatar)
        embed.set_footer(text=f"Нажал - {inter.author}", icon_url=inter.author.display_avatar)

        for i, key in enumerate(field_names, start=2):
            value = data[i]
            if value == 'true':
                status = "`Разрешено`"
            elif value == 'false':
                status = "`Запрещено`"
            else:
                status = f"`{value}`"
            
            embed.add_field(name=key, value=status, inline=True)


        await inter.response.edit_message(embed=embed, view=AnticrashSetupMemberSelectView(self.bot, inter.author, inter.values[0]))

class AntiCrashAddorDeleteRoleView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiCrashAddorDeleteRole(bot, author, arg))

class AntiCrashAddorDeleteRole(disnake.ui.RoleSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(placeholder="Выберите роль", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            return

        if self.arg == 'addrole':
            memberid = inter.values[0]
            data = await db.get_anticrashrole(inter.guild.id, memberid)

            if data:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Роль уже была добавлена в антикраш."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed)
            else:
                await db.anticrash_addrole(inter.guild.id, memberid, 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false')
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"Роль - <@&{memberid}> была добавлен в антикраш."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)

        if self.arg == 'deleterole':
            memberid = inter.values[0]
            data = await db.get_anticrashrole(inter.guild.id, memberid)

            if data:
                await db.anticrash_deleterole(inter.guild.id, memberid)
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"Роль - <@&{memberid}> была удалена из антикраша."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Роли нету в антикраше."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed)

class AntiCrashAddorDeleteUserView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiCrashAddorDeleteUser(bot, author, arg))

class AntiCrashAddorDeleteUser(disnake.ui.UserSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(placeholder="Выберите пользователя", min_values=1, max_values=1)

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            return

        if self.arg == 'adduser':
            memberid = inter.values[0]
            data = await db.get_anticrashuser(inter.guild.id, memberid)

            if data:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Пользователь уже был добавлен в антикраш."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed)
            else:
                await db.anticrash_adduser(inter.guild.id, memberid, 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false', 'false')
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"Пользователь - <@{memberid}> был добавлен в антикраш."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)

        if self.arg == 'deleteuser':
            memberid = inter.values[0]
            data = await db.get_anticrashuser(inter.guild.id, memberid)

            if data:
                await db.anticrash_deleteuser(inter.guild.id, memberid)
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"Пользователь - <@{memberid}> был удален из антикраша."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Пользователь нету в антикраше."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed)

class AntiCrashAddUserOrRoleView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__(timeout = None)

    @disnake.ui.button(label = "Добавить роль", style = disnake.ButtonStyle.gray)
    async def add_role(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            
        embed = disnake.Embed(
            title = 'Nuke',
            description = 'Выберите ниже роль, которую хотите добавить в антикраш.'
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiCrashAddorDeleteRoleView(self.bot, inter.author, 'addrole'))
        
    @disnake.ui.button(label = "Добавить пользователя", style = disnake.ButtonStyle.gray)
    async def add_user(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            return

        embed = disnake.Embed(
            title = 'Nuke',
            description = 'Выберите ниже пользователя, которого хотите добавить в антикраш.'
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiCrashAddorDeleteUserView(self.bot, inter.author, 'adduser'))
        
class AntiCrashDelUserOrRoleView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__(timeout = None)

    @disnake.ui.button(label = "Удалить роль", style = disnake.ButtonStyle.gray)
    async def add_role(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            
        embed = disnake.Embed(
            title = 'Nuke',
            description = 'Выберите ниже роль, которую хотите удалить из антикраша.'
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiCrashAddorDeleteRoleView(self.bot, inter.author, 'deleterole'))
        
    @disnake.ui.button(label = "Удалить пользователя", style = disnake.ButtonStyle.gray)
    async def add_user(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title = "Nuke",
                description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.send_message(embed = embed, ephemeral = True)
            return

        embed = disnake.Embed(
            title = 'Nuke',
            description = 'Выберите ниже пользователя, которого хотите удалить из антикраша.'
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiCrashAddorDeleteUserView(self.bot, inter.author, 'deleteuser'))

class AntiCrashSetupSelectView6(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__()
        self.add_item(AntiCrashSetupSelect(bot, author))

class AntiCrashSetupSelect(disnake.ui.Select):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        options = [
            disnake.SelectOption(
                label = "Настроить роль",
                description = "Выбрав данную опцию вы можете настроить роль",
                value = "anticrash_setup_role",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Настроить пользователя",
                description = "Выбрав данную опцию вы можете настроить пользователя",
                value = "anticrash_setup_user",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Добавить Роль/Пользователя",
                description = "Выбрав данную опцию вы можете добавить роль/пользователя",
                value = "anticrash_setup_add",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Удалить Роль/Пользователя",
                description = "Выбрав данную опцию вы можете удалить роль/пользователя",
                value = "anticrash_setup_remove",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Выход",
                description = "Выбрав данную опцию вы удалите данное сообщение",
                value = "anticrash_setup_exit",
                emoji = "❌"
            )
        ]
        super().__init__(placeholder = "Выберите опцию", options = options)

    async def callback(self, inter: disnake.MessageInteraction):
        
        if self.values[0] == 'anticrash_setup_role':
            if inter.author != self.author:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            data = await db.get_anticrashroles(inter.guild.id)

            if data:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Выберите ниже роль, которую хотите настроить"
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = AntiCrashSetupRoleSelectView(self.bot, inter.author, data))
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "В базе данных нет ролей для антикраша."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)

        if self.values[0] == 'anticrash_setup_user':
            if inter.author != self.author:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            data = await db.get_anticrashusers(inter.guild.id)

            if data:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Выберите ниже пользователя, которого хотите настроить"
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = AntiCrashSetupUserSelectView(self.bot, inter.author, data))
            else:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "В базе данных нет пользователей для антикраша."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)

        if self.values[0] == 'anticrash_setup_add':
            if inter.author != self.author:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            embed = disnake.Embed(
                title = "Nuke",
                description = "Выберите что вы хотите добавить."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiCrashAddUserOrRoleView(self.bot, inter.author))

        if self.values[0] == 'anticrash_setup_remove':
            if inter.author != self.author:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            embed = disnake.Embed(
                title = "Nuke",
                description = "Выберите что вы хотите удалить."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiCrashDelUserOrRoleView(self.bot, inter.author))

        if self.values[0] == 'anticrash_setup_exit':
            if inter.author != self.author:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            await inter.message.delete()
