import disnake
from disnake.ext import commands
from db.db import Database

db = Database("db/db.db")

class AntiMainPersonalLinkModal(disnake.ui.Modal):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        components = [
            disnake.ui.TextInput(
                label = "Персональное приглашение на сервер",
                placeholder = "Укажите приглашение в формате - 'pimp'",
                style = disnake.TextInputStyle.paragraph,
                custom_id = 'personalinvite',
                max_length = 30
            )
        ]
        super().__init__(title = "Персональное приглашение на сервер", components = components)

    async def callback(self, inter: disnake.ModalInteraction):
        personallink = inter.text_values["personalinvite"]

        await db.set_guildvanityurl(inter.guild.id, personallink)

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Вы успешно установили персональную ссылку сервера {personallink}"
        )
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        await inter.response.edit_message(embed = embed)

class AntiMainChannelSelectView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiMainChannelSelect(bot, author, arg))

class AntiMainChannelSelect(disnake.ui.ChannelSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(placeholder = "Выберите канал", min_values = 1, max_values = 1, custom_id = "antimainselect_setup_channel")

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'antimainselect_setup_channel':
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
            
            if self.arg == 'warnings':
                channelid = inter.values[0]
                await db.set_channelwarnings(inter.guild.id, channelid)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = f'Вы успешно установили канал для отправки предупреждений <#{channelid}>\nНиже указаны текущие параметры'
                )

                data = await db.get_infomainsettings(inter.guild.id)

                if data[1] == 0:
                    embed.add_field(name = "Роль бустера", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль бустера", value = f"<@&{data[1]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[2] == 0:
                    embed.add_field(name = "Роль карантин", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль каратин", value = f"<@&{data[2]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[3] == 0:
                    embed.add_field(name = "Канал для отправки предупреждений", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки предупреждений", value = f"<#{data[3]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[4] == 0:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = f"<#{data[4]}>", inline = False)
                
                #---------------------------------------------------------------------------------------#

                if data[5] == 'NULL':
                    embed.add_field(name = "Персональное приглашение на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Персональное приглашение на сервер", value = f"{data[5]}", inline = False)

                if data[6] == '0':
                    embed.add_field(name = "Пользователи добавленные в белый список", value = "Их нету", inline = False)
                else:
                    whitelist_list = data[6].split(',')
                    whitelist_mentions = ', '.join(f'<@{user_id}>' for user_id in whitelist_list)
                    embed.add_field(name="Пользователи добавленные в белый список", value=whitelist_mentions, inline=False)

                if data[7] == '0':
                    embed.add_field(name = "Пользователи имеющие доступ к настройкам", value = "Их нету", inline = False)
                else:
                    hasaccess_list = data[7].split(',')
                    hasaccess_mentions = ', '.join(f'<@{user_id}>' for user_id in hasaccess_list)
                    embed.add_field(name="Пользователи имеющие доступ к настройкам", value=hasaccess_mentions, inline=False)

                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)

            if self.arg == 'quarantine':
                channelid = inter.values[0]
                await db.set_channelquarantine(inter.guild.id, channelid)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = f'Вы успешно установили канал для карантина <#{channelid}>\nНиже указаны текущие параметры'
                )

                data = await db.get_infomainsettings(inter.guild.id)

                if data[1] == 0:
                    embed.add_field(name = "Роль бустера", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль бустера", value = f"<@&{data[1]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[2] == 0:
                    embed.add_field(name = "Роль карантин", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль каратин", value = f"<@&{data[2]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[3] == 0:
                    embed.add_field(name = "Канал для отправки предупреждений", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки предупреждений", value = f"<#{data[3]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[4] == 0:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = f"<#{data[4]}>", inline = False)
                
                #---------------------------------------------------------------------------------------#

                if data[5] == 'NULL':
                    embed.add_field(name = "Персональное приглашение на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Персональное приглашение на сервер", value = f"{data[5]}", inline = False)

                if data[6] == '0':
                    embed.add_field(name = "Пользователи добавленные в белый список", value = "Их нету", inline = False)
                else:
                    whitelist_list = data[6].split(',')
                    whitelist_mentions = ', '.join(f'<@{user_id}>' for user_id in whitelist_list)
                    embed.add_field(name="Пользователи добавленные в белый список", value=whitelist_mentions, inline=False)

                if data[7] == '0':
                    embed.add_field(name = "Пользователи имеющие доступ к настройкам", value = "Их нету", inline = False)
                else:
                    hasaccess_list = data[7].split(',')
                    hasaccess_mentions = ', '.join(f'<@{user_id}>' for user_id in hasaccess_list)
                    embed.add_field(name="Пользователи имеющие доступ к настройкам", value=hasaccess_mentions, inline=False)

                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)


class AntiMainRoleSelectView(disnake.ui.View):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__()
        self.add_item(AntiMainRoleSelect(bot, author, arg))

class AntiMainRoleSelect(disnake.ui.RoleSelect):
    def __init__(self, bot, author, arg):
        self.bot = bot
        self.author = author
        self.arg = arg
        super().__init__(placeholder = "Выберите роль", min_values = 1, max_values = 1, custom_id = "antimainselect_setup_role")

    async def callback(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'antimainselect_setup_role':
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

            if self.arg == 'rolebooster':
                selected_role_id = inter.values[0]
                await db.set_rolebooster(inter.guild.id, selected_role_id)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = f'Вы успешно установили роль бустера <@&{selected_role_id}>\nНиже указаны текущие параметры'
                )

                data = await db.get_infomainsettings(inter.guild.id)

                if data[1] == 0:
                    embed.add_field(name = "Роль бустера", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль бустера", value = f"<@&{data[1]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[2] == 0:
                    embed.add_field(name = "Роль карантин", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль каратин", value = f"<@&{data[2]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[3] == 0:
                    embed.add_field(name = "Канал для отправки предупреждений", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки предупреждений", value = f"<#{data[3]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[4] == 0:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = f"<#{data[4]}>", inline = False)
                
                #---------------------------------------------------------------------------------------#

                if data[5] == 'NULL':
                    embed.add_field(name = "Персональное приглашение на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Персональное приглашение на сервер", value = f"{data[5]}", inline = False)

                if data[6] == '0':
                    embed.add_field(name = "Пользователи добавленные в белый список", value = "Их нету", inline = False)
                else:
                    whitelist_list = data[6].split(',')
                    whitelist_mentions = ', '.join(f'<@{user_id}>' for user_id in whitelist_list)
                    embed.add_field(name="Пользователи добавленные в белый список", value=whitelist_mentions, inline=False)

                if data[7] == '0':
                    embed.add_field(name = "Пользователи имеющие доступ к настройкам", value = "Их нету", inline = False)
                else:
                    hasaccess_list = data[7].split(',')
                    hasaccess_mentions = ', '.join(f'<@{user_id}>' for user_id in hasaccess_list)
                    embed.add_field(name="Пользователи имеющие доступ к настройкам", value=hasaccess_mentions, inline=False)

                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)

            if self.arg == 'rolequarantine':
                selected_role_id = inter.values[0]
                await db.set_rolequarantine(inter.guild.id, selected_role_id)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = f'Вы успешно установили роль карантин <@&{selected_role_id}>\nНиже указаны текущие параметры'
                )

                data = await db.get_infomainsettings(inter.guild.id)

                if data[1] == 0:
                    embed.add_field(name = "Роль бустера", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль бустера", value = f"<@&{data[1]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[2] == 0:
                    embed.add_field(name = "Роль карантин", value = "Не установлена", inline = False)
                else:
                    embed.add_field(name = "Роль каратин", value = f"<@&{data[2]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[3] == 0:
                    embed.add_field(name = "Канал для отправки предупреждений", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки предупреждений", value = f"<#{data[3]}>", inline = False)

                #---------------------------------------------------------------------------------------#

                if data[4] == 0:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для отправки попавших в карантин", value = f"<#{data[4]}>", inline = False)
                
                #---------------------------------------------------------------------------------------#

                if data[5] == 'NULL':
                    embed.add_field(name = "Персональное приглашение на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Персональное приглашение на сервер", value = f"{data[5]}", inline = False)

                if data[6] == '0':
                    embed.add_field(name = "Пользователи добавленные в белый список", value = "Их нету", inline = False)
                else:
                    whitelist_list = data[6].split(',')
                    whitelist_mentions = ', '.join(f'<@{user_id}>' for user_id in whitelist_list)
                    embed.add_field(name="Пользователи добавленные в белый список", value=whitelist_mentions, inline=False)

                if data[7] == '0':
                    embed.add_field(name = "Пользователи имеющие доступ к настройкам", value = "Их нету", inline = False)
                else:
                    hasaccess_list = data[7].split(',')
                    hasaccess_mentions = ', '.join(f'<@{user_id}>' for user_id in hasaccess_list)
                    embed.add_field(name="Пользователи имеющие доступ к настройкам", value=hasaccess_mentions, inline=False)

                    embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                    embed.set_thumbnail(url = inter.author.display_avatar)
                    embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
                    await inter.response.edit_message(embed = embed, view = None)
    
class AntiMainSelectSetupView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__()
        self.add_item(AntiMainSelectSetup(bot, author))

class AntiMainSelectSetup(disnake.ui.Select):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        options = [
            disnake.SelectOption(
                label = "Роль бустера",
                description = "Нажав на данную опцию вы можете установить айди роли бустера",
                value = "antimainselect_setup_rolebooster",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Роль карантин",
                description = "Нажав на данную опцию вы можете установить айди роли карантин",
                value = "antimainselect_setup_rolequarantine",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Канал для отправки предупреждений",
                description = "Нажав на данную опцию вы можете установить канал для отправки предупреждений",
                value = "antimainselect_setup_channelwarnings",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Канал для отправки попавших в карантин",
                description = "Нажав на данную опцию вы можете установить канал для отправки попавших в карантин",
                value = "antimainselect_setup_channelquarantine",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Персональное приглашение на сервер",
                description = "Нажав на данную опцию вы можете установить персональное приглашение на сервер",
                value = "antimainselect_setup_personalinvite",
                emoji = "🔧"
            )
        ]
        super().__init__(placeholder = "Выберите опцию.", min_values = 1, max_values = 1, options = options)

    async def callback(self, inter: disnake.MessageInteraction):

        if self.values[0] == 'antimainselect_setup_rolebooster':
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
                description = "Выберите ниже роль, которую хотите установить как роль бустера.",
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainRoleSelectView(self.bot, inter.author, 'rolebooster'))

        if self.values[0] == 'antimainselect_setup_rolequarantine':
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
                description = "Выберите ниже роль, которую хотите установить как роль карантин.",
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainRoleSelectView(self.bot, inter.author, 'rolequarantine'))

        if self.values[0] == 'antimainselect_setup_channelwarnings':
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
                description = "Выберите ниже канал, который хотите установить как канал для предупреждений.",
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainChannelSelectView(self.bot, inter.author, 'warnings'))

        if self.values[0] == 'antimainselect_setup_channelquarantine':
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
                description = "Выберите ниже канал, который хотите установить как канал для предупреждений.",
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f'Использовал - {inter.author}', icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainChannelSelectView(self.bot, inter.author, 'quarantine'))

        if self.values[0] == 'antimainselect_setup_personalinvite':
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
            
            await inter.response.send_modal(AntiMainPersonalLinkModal(self.bot, inter.author))