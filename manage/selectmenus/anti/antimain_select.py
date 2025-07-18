import disnake
from disnake.ext import commands
from db.db import Database
from manage.selectmenus.anti.antimainselectsetup import AntiMainSelectSetupView

db = Database("db/db.db")

class AntiMainSelectDeleteUserSelectView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiMainSelectDeleteUserSelect(self.bot, self.author, self.arg))

class AntiMainSelectDeleteUserSelect(disnake.ui.UserSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(
            placeholder="Выберите пользователя...",
            min_values=1,
            max_values=1,
            custom_id='select_user_dropdown'
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'select_user_dropdown':
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
            
            selected_user_id = inter.values[0]
            data = await db.get_infomainsettings(inter.guild.id)

            if self.arg == 'whitelist':
                data_list = data[6].split(',')
                if selected_user_id in [str(user_id) for user_id in data_list]:
                    await db.delete_from_whitelist(inter.guild.id, selected_user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно удалили пользователя <@{selected_user_id}> из Whitelist"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
                else:
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Выбранный вами пользователь не находится в Whitelist\nВыберите другого пользователя."
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = AntiMainSelectDeleteUserSelectView(self.bot, inter.author, 'whitelist'))
                
            if self.arg == 'settings':
                data_list = data[7].split(',')
                if selected_user_id in [str(user_id) for user_id in data_list]:
                    await db.delete_from_hasaccess(inter.guild.id, selected_user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно удалили пользователя <@{selected_user_id}> из доступа к настройкам"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
                else:
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Выбранный вами пользователь не находится в доступе к настройкам\nВыберите другого пользователя."
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = AntiMainSelectDeleteUserSelectView(self.bot, inter.author, 'settings'))

class AntiMainSelectDeleteUser(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__(timeout = None)
    
    @disnake.ui.button(label = "Удалить из вайтлиста", style = disnake.ButtonStyle.gray)
    async def delete_from_whitelist(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
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
            description = "Выберите пользователя, которого хотите удалить из вайтлиста"
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiMainSelectDeleteUserSelectView(self.bot, inter.author, 'whitelist'))

    @disnake.ui.button(label = "Удалить из доступа к настройкам", style = disnake.ButtonStyle.gray)
    async def delete_from_settings(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
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
            description = "Выберите пользователя, которого хотите удалить из доступа к настройкам"
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiMainSelectDeleteUserSelectView(self.bot, inter.author, 'settings'))

class AntiMainSelectUserSelectView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiMainSelectUserSelect(self.bot, self.author, self.arg))

class AntiMainSelectUserSelect(disnake.ui.UserSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(
            placeholder="Выберите пользователя...",
            min_values=1,
            max_values=1,
            custom_id='select_user_dropdown'
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'select_user_dropdown':
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
            
            selected_user_id = inter.values[0]
            user_id = f'{selected_user_id}'
            data = await db.get_infomainsettings(inter.guild.id)

            if self.arg == 'whitelist':
                if data[6] == '0':
                    await db.set_user_whitelist(inter.guild.id, user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно добавили пользователя <@{selected_user_id}> в Whitelist"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
                else:
                    await db.add_user_to_whitelist(inter.guild.id, selected_user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно добавили пользователя <@{selected_user_id}> в Whitelist"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
                
            if self.arg == 'settings':
                if data[7] == '0':
                    await db.set_user_hasaccess(inter.guild.id, user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно добавили пользователя <@{selected_user_id}> в доступ к настройкам"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
                else:
                    await db.add_user_to_hasaccess(inter.guild.id, selected_user_id)
                    embed = disnake.Embed(
                        title = "Nuke",
                        description = f"Вы успешно добавили пользователя <@{selected_user_id}> в доступ к настройкам"
                    )
                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)

class AntiMainSelectUserButtons(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__(timeout = None)

    @disnake.ui.button(label = "Добавить в вайтлист", style = disnake.ButtonStyle.gray)
    async def add_to_whitelist(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
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
            description = "Выберите пользователя, которого хотите добавить в вайтлист"
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiMainSelectUserSelectView(self.bot, inter.author, 'whitelist'))

    @disnake.ui.button(label = "Добавить в доступ к настройкам", style = disnake.ButtonStyle.gray)
    async def add_to_settings(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
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
            description = "Выберите пользователя, которого хотите добавить в доступ к настройкам"
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = AntiMainSelectUserSelectView(self.bot, inter.author, 'settings'))

class AntiMainSelectView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__()
        self.add_item(AntiMainSelect(self.bot, self.author))

class AntiMainSelect(disnake.ui.Select):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        options = [
            disnake.SelectOption(
                label = "Установить параметры",
                description = "Выбрав данную опцию вы сможете установить основные параметры",
                value = "antimainselect_setup",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Добавить пользователя в вайтлист/доступ к настройкам",
                description = "Выбрав данную опцию вы сможете добавить пользователя в вайтлист/доступ к настройкам",
                value = "antimainselect_adduser",
                emoji = "⚠️"
            ),
            disnake.SelectOption(
                label = "Удалить пользователя из вайтлиста/доступа к настройкам",
                description = "Выбрав данную опцию вы сможете удалить пользователя из вайтлиста/доступа к настройкам",
                value = "antimainselect_deleteuser",
                emoji = "⚠️"
            ),
            disnake.SelectOption(
                label = "Закрыть меню",
                description = "Выбрав данную опцию вы сможете закрыть меню",
                value = "antimainselect_exit",
                emoji = "❌"
            )
        ]
        super().__init__(placeholder = "Выберите опцию", min_values = 1, max_values = 1, options = options)

    async def callback(self, inter: disnake.MessageInteraction):

        if self.values[0] == "antimainselect_setup":
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
                description = "Выберите параметр, который хотите изменить"
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainSelectSetupView(self.bot, inter.author))

        if self.values[0] == "antimainselect_delete":
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

            pass

        if self.values[0] == "antimainselect_adduser":
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
                description = "Выберите куда вы хотите добавить пользователя"
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainSelectUserButtons(self.bot, inter.author))

        if self.values[0] == "antimainselect_deleteuser":
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
                description = "Выберите откуда хотите удалить человека"
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainSelectDeleteUser(self.bot, inter.author))

        if self.values[0] == "antimainselect_exit":
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