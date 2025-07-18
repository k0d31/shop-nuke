import disnake
from disnake.ext import commands
from db.db import Database

db = Database('db/db.db')

class AnticrashRoleSetupView(disnake.ui.View):
    def __init__(self, bot, author, roleid, arg):
        self.bot = bot
        self.author = author
        self.roleid = roleid
        self.arg = arg
        super().__init__(timeout = None)

    @disnake.ui.button(label="Установить число", style=disnake.ButtonStyle.gray)
    async def set_count(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author != self.author:
            embed = disnake.Embed(
                title="Nuke",
                description=f"{inter.author.mention}, зайка, ты не можешь использовать не свое меню."
            )
            embed.set_author(name=inter.guild.name, icon_url=inter.guild.icon.url if inter.guild.icon else None)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.set_footer(text=f"Нажал - {inter.author}", icon_url=inter.author.display_avatar.url)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = disnake.Embed(
            title="Nuke",
            description="Отправьте в чат число, которое хотите установить."
        )
        await inter.response.send_message(embed=embed, ephemeral=True)

        def check(m):
            return m.author == inter.author and m.channel == inter.channel and m.content.isdigit()

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            number = int(msg.content)
            type2 = str(number)

            if self.arg == 'guild_update':
                await db.set_role_guild_update(self.roleid, type2)

            if self.arg == 'channel_create': 
                await db.set_role_channel_create(self.roleid, type2)

            if self.arg == 'channel_update':
                await db.set_role_channel_update(self.roleid, type2)

            if self.arg == 'channel_delete':
                await db.set_role_channel_delete(self.roleid, type2)

            if self.arg == 'overwrite_create':
                await db.set_role_overwrite_create(self.roleid, type2)
            
            if self.arg == 'overwrite_update':
                await db.set_role_overwrite_update(self.roleid, type2)

            if self.arg == 'overwrite_delete':
                await db.set_role_overwrite_delete(self.roleid, type2)

            if self.arg == 'kick':
                await db.set_role_kick(self.roleid, type2)
            
            if self.arg == 'ban':
                await db.set_role_ban(self.roleid, type2)

            if self.arg == 'unban':
                await db.set_role_unban(self.roleid, type2)
            
            if self.arg == 'member_update':
                await db.set_role_member_update(self.roleid, type2)
            
            if self.arg == 'member_role_update':
                await db.set_role_member_role_update(self.roleid, type2)
            
            if self.arg == 'bot_add':
                await db.set_role_bot_add(self.roleid, type2)

            if self.arg == 'role_create':
                await db.set_role_role_create(self.roleid, type2)

            if self.arg == 'role_update':
                await db.set_role_role_update(self.roleid, type2)

            if self.arg == 'role_delete':
                await db.set_role_role_delete(self.roleid, type2)

            if self.arg == 'webhook_create':
                await db.set_role_webhook_create(self.roleid, type2)

            if self.arg == 'webhook_update':
                await db.set_role_webhook_update(self.roleid, type2)

            if self.arg == 'webhook_delete':
                await db.set_role_webhook_delete(self.roleid, type2)

            if self.arg == 'thread_delete':
                await db.set_role_thread_delete(self.roleid, type2)

            if self.arg == 'give_timeout':
                await db.set_role_timeout_give(self.roleid, type2)

            data = await db.get_anticrashrole(inter.guild.id, self.roleid)

            data = data[0]

            field_names = [
                "guild_update", "channel_create", "channel_update", "channel_delete",
                "kick", "ban", "unban",
                "member_update", "bot_add", "role_create", "role_update",
                "role_delete", "webhook_create", "thread_delete", "give_timeout"
            ]
            
            new_embed = disnake.Embed(
                title="Nuke",
                description=f"Настройки над ролью <@&{self.roleid}>\n```Вы установили параметр {self.arg} на {number}```\n\nТекущие параметры:"
            )

            for i, key in enumerate(field_names, start=2):
                value = data[i]
                if value == 'true':
                    status = "`Разрешено`"
                elif value == 'false':
                    status = "`Запрещено`"
                else:
                    status = f"`{value}`"
                
                new_embed.add_field(name=key, value=status, inline=True)

            await inter.message.edit(embed=new_embed, view = AnticrashSetupRoleSelectView(self.bot, inter.author, self.roleid))

            await msg.delete()
        except:
            pass


    @disnake.ui.button(label = "Разрешить", style = disnake.ButtonStyle.gray)
    async def allow(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
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
        
        if self.arg == 'guild_update':
            await db.set_role_guild_update(self.roleid, 'true')

        if self.arg == 'channel_create': 
            await db.set_role_channel_create(self.roleid, 'true')

        if self.arg == 'channel_update':
            await db.set_role_channel_update(self.roleid, 'true')

        if self.arg == 'channel_delete':
            await db.set_role_channel_delete(self.roleid, 'true')

        if self.arg == 'overwrite_create':
            await db.set_role_overwrite_create(self.roleid, 'true')
        
        if self.arg == 'overwrite_update':
            await db.set_role_overwrite_update(self.roleid, 'true')

        if self.arg == 'overwrite_delete':
            await db.set_role_overwrite_delete(self.roleid, 'true')

        if self.arg == 'kick':
            await db.set_role_kick(self.roleid, 'true')
        
        if self.arg == 'ban':
            await db.set_role_ban(self.roleid, 'true')

        if self.arg == 'unban':
            await db.set_role_unban(self.roleid, 'true')
        
        if self.arg == 'member_update':
            await db.set_role_member_update(self.roleid, 'true')
        
        if self.arg == 'member_role_update':
            await db.set_role_member_role_update(self.roleid, 'true')
        
        if self.arg == 'bot_add':
            await db.set_role_bot_add(self.roleid, 'true')

        if self.arg == 'role_create':
            await db.set_role_role_create(self.roleid, 'true')

        if self.arg == 'role_update':
            await db.set_role_role_update(self.roleid, 'true')

        if self.arg == 'role_delete':
            await db.set_role_role_delete(self.roleid, 'true')

        if self.arg == 'webhook_create':
            await db.set_role_webhook_create(self.roleid, 'true')

        if self.arg == 'webhook_update':
            await db.set_role_webhook_update(self.roleid, 'true')

        if self.arg == 'webhook_delete':
            await db.set_role_webhook_delete(self.roleid, 'true')

        if self.arg == 'thread_delete':
            await db.set_role_thread_delete(self.roleid, 'true')

        if self.arg == 'give_timeout':
            await db.set_role_timeout_give(self.roleid, 'true')

        data = await db.get_anticrashrole(inter.guild.id, self.roleid)

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", "give_timeout"
        ]

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Настройки над ролью <@&{self.roleid}>\n```Вы успешно установили параметр {self.arg} на разрешено```\n\nТекущие параметры:"
        )

        for i, key in enumerate(field_names, start=2):
            value = data[i]
            if value == 'true':
                status = "`Разрешено`"
            elif value == 'false':
                status = "`Запрещено`"
            else:
                status = f"`{value}`"
            
            embed.add_field(name=key, value=status, inline=True)
            
        await inter.response.edit_message(embed = embed, view = AnticrashSetupRoleSelectView(self.bot, inter.author, self.roleid))

    @disnake.ui.button(label = "Запретить", style = disnake.ButtonStyle.gray)
    async def deny(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.arg == 'guild_update':
            await db.set_role_guild_update(self.roleid, 'false')

        if self.arg == 'channel_create': 
            await db.set_role_channel_create(self.roleid, 'false')

        if self.arg == 'channel_update':
            await db.set_role_channel_update(self.roleid, 'false')

        if self.arg == 'channel_delete':
            await db.set_role_channel_delete(self.roleid, 'false')

        if self.arg == 'overwrite_create':
            await db.set_role_overwrite_create(self.roleid, 'false')
        
        if self.arg == 'overwrite_update':
            await db.set_role_overwrite_update(self.roleid, 'false')

        if self.arg == 'overwrite_delete':
            await db.set_role_overwrite_delete(self.roleid, 'false')

        if self.arg == 'kick':
            await db.set_role_kick(self.roleid, 'false')
        
        if self.arg == 'ban':
            await db.set_role_ban(self.roleid, 'false')

        if self.arg == 'unban':
            await db.set_role_unban(self.roleid, 'false')
        
        if self.arg == 'member_update':
            await db.set_role_member_update(self.roleid, 'false')
        
        if self.arg == 'member_role_update':
            await db.set_role_member_role_update(self.roleid, 'false')
        
        if self.arg == 'bot_add':
            await db.set_role_bot_add(self.roleid, 'false')

        if self.arg == 'role_create':
            await db.set_role_role_create(self.roleid, 'false')

        if self.arg == 'role_update':
            await db.set_role_role_update(self.roleid, 'false')

        if self.arg == 'role_delete':
            await db.set_role_role_delete(self.roleid, 'false')

        if self.arg == 'webhook_create':
            await db.set_role_webhook_create(self.roleid, 'false')

        if self.arg == 'webhook_update':
            await db.set_role_webhook_update(self.roleid, 'false')

        if self.arg == 'webhook_delete':
            await db.set_role_webhook_delete(self.roleid, 'false')

        if self.arg == 'thread_delete':
            await db.set_role_thread_delete(self.roleid, 'false')

        if self.arg == 'give_timeout':
            await db.set_role_timeout_give(self.roleid, 'false')

        data = await db.get_anticrashrole(inter.guild.id, self.roleid)

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", "give_timeout"
        ]

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Настройки над ролью <@&{self.roleid}>\n```Вы успешно установили параметр {self.arg} на запрещено```\n\nТекущие параметры:"
        )

        for i, key in enumerate(field_names, start=2):
            value = data[i]
            if value == 'true':
                status = "`Разрешено`"
            elif value == 'false':
                status = "`Запрещено`"
            else:
                status = f"`{value}`"
            
            embed.add_field(name=key, value=status, inline=True)

        await inter.response.edit_message(embed = embed, view = AnticrashSetupRoleSelectView(self.bot, inter.author, self.roleid))

class AnticrashSetupRoleSelectView(disnake.ui.View):
    def __init__(self, bot, author, roleid):
        self.bot = bot
        self.author = author
        self.roleid = roleid
        super().__init__()
        self.add_item(AnticrashSetupRoleSelect(bot, self.author, self.roleid))

class AnticrashSetupRoleSelect(disnake.ui.Select):
    def __init__(self, bot, author, roleid):
        self.bot = bot
        self.author = author
        self.roleid = roleid

        options = [
            disnake.SelectOption(
                label="Обновление настроек сервера",
                description="Настроив данный параметр, вы можете разрешить либо запретить обновлять настройки сервера.",
                value="guild_update",
                emoji="⚙️"
            ),
            disnake.SelectOption(
                label="Создание канала",
                description="Вы можете разрешить или запретить создание новых каналов на сервере.",
                value="channel_create",
                emoji="📁"
            ),
            disnake.SelectOption(
                label="Обновление канала",
                description="Настройки канала будут обновлены автоматически.",
                value="channel_update",
                emoji="🔄"
            ),
            disnake.SelectOption(
                label="Удаление канала",
                description="Вы можете разрешить или запретить удаление каналов на сервере.",
                value="channel_delete",
                emoji="🗑️"
            ),
            disnake.SelectOption(
                label="Выгнать участника",
                description="Настройте возможность выгонять участников с сервера.",
                value="kick",
                emoji="🚪"
            ),
            disnake.SelectOption(
                label="Забанить участника",
                description="Вы можете разрешить или запретить бан участников на сервере.",
                value="ban",
                emoji="🔨"
            ),
            disnake.SelectOption(
                label="Разбанить участника",
                description="Настройте возможность разбанивать участников на сервере.",
                value="unban",
                emoji="🔓"
            ),
            disnake.SelectOption(
                label="Обновление участника",
                description="Вы можете разрешить или запретить обновление участников.",
                value="member_update",
                emoji="📝"
            ),
            disnake.SelectOption(
                label="Добавление бота",
                description="Разрешите или запретите добавление ботов на сервер.",
                value="bot_add",
                emoji="🤖"
            ),
            disnake.SelectOption(
                label="Создание роли",
                description="Вы можете разрешить или запретить создание новых ролей на сервере.",
                value="role_create",
                emoji="🔧"
            ),
            disnake.SelectOption(
                label="Обновление роли",
                description="Настройки роли будут обновлены автоматически.",
                value="role_update",
                emoji="🔄"
            ),
            disnake.SelectOption(
                label="Удаление роли",
                description="Вы можете разрешить или запретить удаление ролей на сервере.",
                value="role_delete",
                emoji="🗑️"
            ),
            disnake.SelectOption(
                label="Создание вебхука",
                description="Настройте возможность создания новых вебхуков.",
                value="webhook_create",
                emoji="📝"
            ),
            disnake.SelectOption(
                label="Удаление треда",
                description="Вы можете разрешить или запретить удаление тредов на сервере.",
                value="thread_delete",
                emoji="🗑️"
            ),
            disnake.SelectOption(
                label="Выдача таймаута",
                description="Вы можете разрешить или запретить выдачу таймаута.",
                value="give_timeout",
                emoji="🔄"
            ),
            disnake.SelectOption(
                label="Закрыть",
                description="Эта опция позволяет удалить сообщение.",
                value="delete",
                emoji="❌"
            ),
        ]
        super().__init__(placeholder = "Выберите необходимую настройку", min_values = 1, max_values = 1, options = options)

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
        
        if self.values[0] == 'delete':
            await inter.message.delete()
        else:    
            arg = inter.values[0]

            embed = disnake.Embed(
                title = "Nuke",
                description = "Выберите значение под данный параметр."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Нажал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AnticrashRoleSetupView(self.bot, inter.author, self.roleid, arg))