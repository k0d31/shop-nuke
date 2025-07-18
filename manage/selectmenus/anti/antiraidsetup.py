import disnake
from disnake.ext import commands
from db.db import Database

db = Database("db/db.db")

class AntiRaidChannelSelectView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__()
        self.add_item(AntiRaidChannelSelect(bot, author))

class AntiRaidChannelSelect(disnake.ui.ChannelSelect):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__(placeholder = "Выберите канал для логов", min_values = 1, max_values = 1)

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
        
        channel = inter.values[0]
        await db.set_channel_nuke_logs(inter.guild.id, channel)
        embed = disnake.Embed(
            title = "Nuke",
            description = f"Теперь канал для логов - <#{channel}>"
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = None)


class AntiRaidSetupTimeModal(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        components = [
            disnake.ui.TextInput(
                label = "Время в днях",
                placeholder = "Укажите время в днях",
                style = disnake.TextInputStyle.short,
                custom_id = 'time',
                min_length = 1,
                max_length = 2,
            )
        ]
        super().__init__(title = "Настройка времени антирейда", components = components)

    async def callback(self, inter: disnake.ModalInteraction):
        time = inter.text_values["time"]

        await db.set_time_nuke(inter.guild.id, time)

        embed = disnake.Embed(
            title = "Nuke",
            description = f"Теперь аккаунт для входа на сервер, должен быть в дискорде более {time} дней."
        )
        embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
        embed.set_thumbnail(url = inter.author.display_avatar)
        embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
        await inter.response.edit_message(embed = embed, view = None)

class AntiRaidSetupView(disnake.ui.View):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        super().__init__()
        self.add_item(AntiRaidSetup(bot, author))

class AntiRaidSetup(disnake.ui.Select):
    def __init__(self, bot, author):
        self.bot = bot
        self.author = author
        options = [
            disnake.SelectOption(
                label = "Включить/Выключить антирейд",
                description = "Выбрав данную опцию вы сможете включить или выключить антирейд",
                value = "antiraid_setup",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Установить время",
                description = "Выбрав данную опцию вы можете установить время, сколько аккаунт человека должен быть в дискорде.",
                value = "antiraid_setup_time",
                emoji = "⏰"
            ),
            disnake.SelectOption(
                label = "Установить канал для логов",
                description = "Выбрав данную опцию вы можете установить канал для логов",
                value = "antiraid_setup_channel",
                emoji = "📝"
            ),
            disnake.SelectOption(
                label = "Выход",
                description = "Выбрав данную опцию вы удалите данное сообщение",
                value = "antiexit_setup",
                emoji = "❌"
            )
        ]
        super().__init__(placeholder = "Выберите опцию", min_values = 1, max_values = 1, options = options)

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "antiraid_setup":
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
            
            data = await db.get_antiraid(inter.guild.id)
            
            if data[1] == 0:
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = "Настройки не завершены до конца, включение является невозможным."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return
            
            if data[2] == 0: 
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = "Настройки не завершены до конца, включение является невозможным."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.send_message(embed = embed, ephemeral = True)
                return

            if data[3] == 1:
                await db.set_server_antinuke_off(inter.guild.id)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = "Система антирейда была выключена."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)
            else:
                await db.set_server_antinuke_on(inter.guild.id)
                embed = disnake.Embed(
                    title = 'Nuke',
                    description = "Система антирейда была включена."
                )
                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = None)


        if self.values[0] == "antiraid_setup_time":
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
            
            await inter.response.send_modal(AntiRaidSetupTimeModal(self.bot))

        if self.values[0] == "antiraid_setup_channel":
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
                description = "Выберите канал для логов"
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiRaidChannelSelectView(self.bot, inter.author))

        if self.values[0] == "antiexit_setup":
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