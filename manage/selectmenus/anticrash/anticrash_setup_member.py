import disnake
from disnake.ext import commands
from db.db import Database

db = Database('db/db.db')

class AnticrashMemberSetupView(disnake.ui.View):
    def __init__(self, bot, author, memberid, arg):
        self.bot = bot
        self.author = author
        self.memberid = memberid
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
                await db.set_member_guild_update(self.memberid, type2)

            if self.arg == 'channel_create': 
                await db.set_member_channel_create(self.memberid, type2)

            if self.arg == 'channel_update':
                await db.set_member_channel_update(self.memberid, type2)

            if self.arg == 'channel_delete':
                await db.set_member_channel_delete(self.memberid, type2)

            if self.arg == 'overwrite_create':
                await db.set_member_overwrite_create(self.memberid, type2)
            
            if self.arg == 'overwrite_update':
                await db.set_member_overwrite_update(self.memberid, type2)

            if self.arg == 'overwrite_delete':
                await db.set_member_overwrite_delete(self.memberid, type2)

            if self.arg == 'kick':
                await db.set_member_kick(self.memberid, type2)
            
            if self.arg == 'ban':
                await db.set_member_ban(self.memberid, type2)

            if self.arg == 'unban':
                await db.set_member_unban(self.memberid, type2)
            
            if self.arg == 'member_update':
                await db.set_member_member_update(self.memberid, type2)
            
            if self.arg == 'member_role_update':
                await db.set_member_member_role_update(self.memberid, type2)
            
            if self.arg == 'bot_add':
                await db.set_member_bot_add(self.memberid, type2)

            if self.arg == 'role_create':
                await db.set_member_role_create(self.memberid, type2)

            if self.arg == 'role_update':
                await db.set_member_role_update(self.memberid, type2)

            if self.arg == 'role_delete':
                await db.set_member_role_delete(self.memberid, type2)

            if self.arg == 'webhook_create':
                await db.set_member_webhook_create(self.memberid, type2)

            if self.arg == 'webhook_update':
                await db.set_member_webhook_update(self.memberid, type2)

            if self.arg == 'webhook_delete':
                await db.set_member_webhook_delete(self.memberid, type2)

            if self.arg == 'thread_delete':
                await db.set_member_thread_delete(self.memberid, type2)

            if self.arg == 'give_timeout':
                await db.set_member_timeout_give(self.memberid, type2)

            data = await db.get_anticrashuser(inter.guild.id, self.memberid)

            data = data[0]

            field_names = [
                "guild_update", "channel_create", "channel_update", "channel_delete",
                "kick", "ban", "unban",
                "member_update", "bot_add", "role_create", "role_update",
                "role_delete", "webhook_create", "thread_delete", "give_timeout"
            ]
            
            new_embed = disnake.Embed(
                title="Nuke",
                description=f"Настройки над пользователем <@{self.memberid}>\n```Вы установили параметр {self.arg} на {number}```\n\nТекущие параметры:"
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

            await inter.message.edit(embed=new_embed, view = AnticrashSetupMemberSelectView(self.bot, inter.author, self.memberid))

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
            await db.set_member_guild_update(self.memberid, 'true')

        if self.arg == 'channel_create': 
            await db.set_member_channel_create(self.memberid, 'true')

        if self.arg == 'channel_update':
            await db.set_member_channel_update(self.memberid, 'true')

        if self.arg == 'channel_delete':
            await db.set_member_channel_delete(self.memberid, 'true')

        if self.arg == 'overwrite_create':
            await db.set_member_overwrite_create(self.memberid, 'true')
        
        if self.arg == 'overwrite_update':
            await db.set_member_overwrite_update(self.memberid, 'true')

        if self.arg == 'overwrite_delete':
            await db.set_member_overwrite_delete(self.memberid, 'true')

        if self.arg == 'kick':
            await db.set_member_kick(self.memberid, 'true')
        
        if self.arg == 'ban':
            await db.set_member_ban(self.memberid, 'true')

        if self.arg == 'unban':
            await db.set_member_unban(self.memberid, 'true')
        
        if self.arg == 'member_update':
            await db.set_member_member_update(self.memberid, 'true')
        
        if self.arg == 'member_role_update':
            await db.set_member_member_role_update(self.memberid, 'true')
        
        if self.arg == 'bot_add':
            await db.set_member_bot_add(self.memberid, 'true')

        if self.arg == 'role_create':
            await db.set_member_role_create(self.memberid, 'true')

        if self.arg == 'role_update':
            await db.set_member_role_update(self.memberid, 'true')

        if self.arg == 'role_delete':
            await db.set_member_role_delete(self.memberid, 'true')

        if self.arg == 'webhook_create':
            await db.set_member_webhook_create(self.memberid, 'true')

        if self.arg == 'webhook_update':
            await db.set_member_webhook_update(self.memberid, 'true')

        if self.arg == 'webhook_delete':
            await db.set_member_webhook_delete(self.memberid, 'true')

        if self.arg == 'thread_delete':
            await db.set_member_thread_delete(self.memberid, 'true')

        if self.arg == 'give_timeout':
            await db.set_member_timeout_give(self.memberid, 'true')

        data = await db.get_anticrashuser(inter.guild.id, self.memberid)

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", "give_timeout"
        ]

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Настройки над пользователем <@{self.memberid}>\n```Вы успешно установили параметр {self.arg} на разрешено```\n\nТекущие параметры:"
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
            
        await inter.response.edit_message(embed = embed, view = AnticrashSetupMemberSelectView(self.bot, inter.author, self.memberid))

    @disnake.ui.button(label = "Запретить", style = disnake.ButtonStyle.gray)
    async def deny(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if self.arg == 'guild_update':
            await db.set_member_guild_update(self.memberid, 'false')

        if self.arg == 'channel_create': 
            await db.set_member_channel_create(self.memberid, 'false')

        if self.arg == 'channel_update':
            await db.set_member_channel_update(self.memberid, 'false')

        if self.arg == 'channel_delete':
            await db.set_member_channel_delete(self.memberid, 'false')

        if self.arg == 'overwrite_create':
            await db.set_member_overwrite_create(self.memberid, 'false')
        
        if self.arg == 'overwrite_update':
            await db.set_member_overwrite_update(self.memberid, 'false')

        if self.arg == 'overwrite_delete':
            await db.set_member_overwrite_delete(self.memberid, 'false')

        if self.arg == 'kick':
            await db.set_member_kick(self.memberid, 'false')
        
        if self.arg == 'ban':
            await db.set_member_ban(self.memberid, 'false')

        if self.arg == 'unban':
            await db.set_member_unban(self.memberid, 'false')
        
        if self.arg == 'member_update':
            await db.set_member_member_update(self.memberid, 'false')
        
        if self.arg == 'member_role_update':
            await db.set_member_member_role_update(self.memberid, 'false')
        
        if self.arg == 'bot_add':
            await db.set_member_bot_add(self.memberid, 'false')

        if self.arg == 'role_create':
            await db.set_member_role_create(self.memberid, 'false')

        if self.arg == 'role_update':
            await db.set_member_role_update(self.memberid, 'false')

        if self.arg == 'role_delete':
            await db.set_member_role_delete(self.memberid, 'false')

        if self.arg == 'webhook_create':
            await db.set_member_webhook_create(self.memberid, 'false')

        if self.arg == 'webhook_update':
            await db.set_member_webhook_update(self.memberid, 'false')

        if self.arg == 'webhook_delete':
            await db.set_member_webhook_delete(self.memberid, 'false')

        if self.arg == 'thread_delete':
            await db.set_member_thread_delete(self.memberid, 'false')

        if self.arg == 'give_timeout':
            await db.set_member_timeout_give(self.memberid, 'false')

        data = await db.get_anticrashuser(inter.guild.id, self.memberid)

        data = data[0]

        field_names = [
            "guild_update", "channel_create", "channel_update", "channel_delete",
            "kick", "ban", "unban",
            "member_update", "bot_add", "role_create", "role_update",
            "role_delete", "webhook_create", "thread_delete", 'give_timeout'
        ]

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Настройки над пользователем <@{self.memberid}>\n```Вы успешно установили параметр {self.arg} на запрещено```\n\nТекущие параметры:"
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

        await inter.response.edit_message(embed = embed, view = AnticrashSetupMemberSelectView(self.bot, inter.author, self.memberid))

class AnticrashSetupMemberSelectView(disnake.ui.View):
    def __init__(self, bot, author, memberid):
        self.bot = bot
        self.author = author
        self.memberid = memberid
        super().__init__()
        self.add_item(AnticrashSetupMemberSelect(bot, self.author, self.memberid))

class AnticrashSetupMemberSelect(disnake.ui.Select):
    def __init__(self, bot, author, memberid):
        self.bot = bot
        self.author = author
        self.memberid = memberid

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
                label="Обновление профиля участника",
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
                label = "Выдача таймаута",
                description = "Вы можете разрешить или запретить выдачу таймаута.",
                value = "give_timeout",
                emoji = "🔄"
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
            await inter.response.edit_message(embed = embed, view = AnticrashMemberSetupView(self.bot, inter.author, self.memberid, arg))