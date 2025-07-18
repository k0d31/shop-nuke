import disnake

from disnake.ext import commands, tasks
from db.db import Database

db = Database('db/db.db')

class TakeFromAnti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id

        if custom_id == 'accept_restore':
            data_settings = await db.get_infomainsettings(inter.guild.id)

            if inter.author.id not in [int(user_id) for user_id in data_settings[6].split(',')]:
                return await inter.response.send_message('Вы не можете доставать пользователя из антикраша.', ephemeral=True)

            roles_data = await db.get_quarantinedroles(inter.message.id)
            user_data = await db.get_quarantineuser(inter.message.id)

            if not roles_data:
                await inter.response.send_message("Роли не найдены в базе данных.", ephemeral=True)
                return

            if not user_data:
                await inter.response.send_message("Пользователь не найден в базе данных.", ephemeral=True)
                return

            user = inter.guild.get_member(user_data[0])

            role_ids = roles_data[0].split(',')
            roles = []
            for role_id in role_ids:
                try:
                    role = inter.guild.get_role(int(role_id))
                    if role:
                        roles.append(role)
                except ValueError:
                    continue

            if not roles:
                await inter.response.send_message("Не удалось найти роли для восстановления.", ephemeral=True)
                return

            try:
                await user.edit(roles=roles)
                embed = inter.message.embeds[0].add_field(name="Достал из карантина", value=f"{inter.author.mention}", inline=False)
                await inter.response.edit_message(embed=embed, view=None)
                await db.delete_user_from_quarantine(inter.message.id, user.id)
            except Exception as e:
                await inter.response.send_message(f"Ошибка при восстановлении ролей: {e}", ephemeral=True)

        if custom_id == 'deny_restore':
            data_settings = await db.get_infomainsettings(inter.guild.id)

            if inter.author.id not in [int(user_id) for user_id in data_settings[6].split(',')]:
                return await inter.response.send_message('Вы не можете доставать пользователя из антикраша.',
                                                         ephemeral=True)

            user_data = await db.get_quarantineuser(inter.message.id)

            if not user_data:
                await inter.response.send_message("Пользователь не найден в базе данных.", ephemeral=True)
                return

            user = inter.get_member(user_data[0])

            await db.delete_user_from_quarantine(inter.message.id, user.id)

            try:
                embed = inter.message.embeds[0].add_field(name="Отклонил восстановление", value=f"{inter.author.mention}", inline=False)
                await inter.response.edit_message(embed=embed, view=None)
            except Exception as e:
                await inter.response.send_message(f"Ошибка при восстановлении ролей: {e}", ephemeral=True)


def setup(bot):
    bot.add_cog(TakeFromAnti(bot))
