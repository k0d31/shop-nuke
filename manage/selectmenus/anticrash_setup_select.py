import disnake
from disnake.ext import commands
from db.db import Database
from manage.selectmenus.anti.antimain_select import AntiMainSelectView
from manage.selectmenus.anti.antiraidsetup import AntiRaidSetupView
from manage.selectmenus.anticrash.anticrash_setup import AntiCrashSetupSelectView6

db = Database("db/db.db")

class AntiCrashSetupSelectView(disnake.ui.View):
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
                label = "Настройка антикраш системы",
                description = "Выбрав данную опцию вы сможете настроить антикраш систему",
                value = "anticrash_setup",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Настройка антирейд системы",
                description = "Выбрав данную опцию вы сможете настроить антирейд систему",
                value = "antiraid_setup",
                emoji = "🔧"
            ),
            disnake.SelectOption(
                label = "Настройка основных настроек",
                description = "Выбрав данную опцию вы сможете настроить основные настройки",
                value = "antimain_setup",
                emoji = "🔧"
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

        if self.values[0] == "anticrash_setup":
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
                description = "Выберите необходимое действие."
            )
            embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
            embed.set_thumbnail(url = inter.author.display_avatar)
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiCrashSetupSelectView6(self.bot, inter.author))

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

            if data:
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Ниже указаны установленные сейчас параметры."
                )

                if data[1] == 0:
                    embed.add_field(name = "Канал для логов", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для логов", value = f"<#{data[1]}>", inline = False)

                if data[2] == 0:
                    embed.add_field(name = "Время(в днях) для входа на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Время(в днях) для входа на сервер", value = f"{data[2]}", inline = False)

                if data[3] == 0:
                    embed.add_field(name = "Включена?", value = "Нет", inline = False)
                else:
                    embed.add_field(name = "Включена?", value = "Да", inline = False)

                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = AntiRaidSetupView(self.bot, inter.author))
            else:
                await db.add_server_to_antinuke(inter.guild.id, 0, 0, 0)
                data2 = await db.get_antiraid(inter.guild.id)
                embed = disnake.Embed(
                    title = "Nuke",
                    description = "Ниже указаны установленные сейчас параметры."
                )

                if data2[1] == 0:
                    embed.add_field(name = "Канал для логов", value = "Не установлен", inline = False)
                else:
                    embed.add_field(name = "Канал для логов", value = f"<#{data2[1]}>", inline = False)

                if data2[2] == 0:
                    embed.add_field(name = "Время(в днях) для входа на сервер", value = "Не установлено", inline = False)
                else:
                    embed.add_field(name = "Время(в днях) для входа на сервер", value = f"{data2[2]}", inline = False)

                if data2[3] == 0:
                    embed.add_field(name = "Включена?", value = "Нет", inline = False)
                else:
                    embed.add_field(name = "Включена?", value = "Да", inline = False)

                embed.set_author(name = inter.guild.name, icon_url = inter.guild.icon)
                embed.set_thumbnail(url = inter.author.display_avatar)
                embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
                await inter.response.edit_message(embed = embed, view = AntiRaidSetupView(self.bot, inter.author))

        if self.values[0] == "antimain_setup":
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
            
            data = await db.get_infomainsettings(inter.guild.id)

            embed = disnake.Embed(
                title = "Nuke",
                description = "Ниже указаны параметры которые установлены сейчас."
            )

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
            embed.set_footer(text = f"Использовал - {inter.author}", icon_url = inter.author.display_avatar)
            await inter.response.edit_message(embed = embed, view = AntiMainSelectView(self.bot, inter.author))
        
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