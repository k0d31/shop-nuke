import aiosqlite

class Database:
    def __init__(self, dbname):
        self.dbname = dbname

    async def init_db(self):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                query = '''
                    CREATE TABLE IF NOT EXISTS anticrashrole_settings (
                        guildid INTEGER,
                        roleid INTEGER PRIMARY KEY,
                        guild_update TEXT,
                        channel_create TEXT,
                        channel_update TEXT,
                        channel_delete TEXT,
                        kick TEXT,
                        ban TEXT,
                        unban TEXT,
                        member_update TEXT,
                        bot_add TEXT,
                        role_create TEXT,
                        role_update TEXT,
                        role_delete TEXT,
                        webhook_create TEXT,
                        thread_delete TEXT,
                        give_timeout TEXT
                    );

                    CREATE TABLE IF NOT EXISTS anticrashuser_settings (
                        guildid INTEGER,
                        memberid INTEGER PRIMARY KEY,
                        guild_update TEXT,
                        channel_create TEXT,
                        channel_update TEXT,
                        channel_delete TEXT,
                        kick TEXT,
                        ban TEXT,
                        unban TEXT,
                        member_update TEXT,
                        bot_add TEXT,
                        role_create TEXT,
                        role_update TEXT,
                        role_delete TEXT,
                        webhook_create TEXT,
                        thread_delete TEXT,
                        give_timeout TEXT
                    );

                    CREATE TABLE IF NOT EXISTS mainanti_settings(
                        guildid INTEGER PRIMARY KEY,
                        role_booster INTEGER,
                        role_localban INTEGER,
                        channel_pred INTEGER,
                        channel_ban INTEGER,
                        guildvanityurl TEXT,
                        whitelist TEXT,
                        hasaccess TEXT
                    );

                    CREATE TABLE IF NOT EXISTS mainnuke_settings(
                        guildid INTEGER PRIMARY KEY,
                        channel_log INTEGER,
                        time_nuke INTEGER,
                        enabled INTEGER
                    );

                    CREATE TABLE IF NOT EXISTS quarantined_users(
                        message_id INTEGER,
                        userid INTEGER PRIMARY KEY,
                        roles TEXT
                    );

                '''
                await cursor.executescript(query)
                await db.commit()
            
# --------------------------------------------------------GET--------------------------------------------------------

    async def get_infomainsettings(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM mainanti_settings WHERE guildid = ?", (guildid,))
                return await cursor.fetchone()

    async def get_user_in_whitelist(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT whitelist FROM mainanti_settings WHERE guildid = ?", (guildid,))
                return await cursor.fetchone()
            
    async def get_antiraid(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM mainnuke_settings WHERE guildid = ?", (guildid,))
                return await cursor.fetchone()

    async def get_anticrashuser(self, guildid, memberid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM anticrashuser_settings WHERE guildid = ? AND memberid = ?", (guildid, memberid))
                return await cursor.fetchall()
            
    async def get_anticrashrole(self, guildid, roleid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM anticrashrole_settings WHERE guildid = ? AND roleid = ?", (guildid, roleid))
                return await cursor.fetchall()
            
    async def get_anticrashroles(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM anticrashrole_settings WHERE guildid = ?", (guildid,))
                return await cursor.fetchall()
            
    async def get_anticrashusers(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM anticrashuser_settings WHERE guildid = ?", (guildid,))
                return await cursor.fetchall()
            
    async def get_userinquarantine(self, message_id, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM quarantined_users WHERE message_id = ? AND userid = ?", (message_id, userid))
                return await cursor.fetchone()
            
    async def get_quarantinedroles(self, message_id):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT roles FROM quarantined_users WHERE message_id = ?", (message_id, ))
                return await cursor.fetchone()

    async def get_quarantineuser(self, message_id):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT userid FROM quarantined_users WHERE message_id = ?", (message_id,))
                return await cursor.fetchone()
            
# -----------------------------------------------------REMOVE--------------------------------------------------------

    async def delete_from_whitelist(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT whitelist FROM mainanti_settings WHERE guildid = ?", (guildid,))
                row = await cursor.fetchone()
                if row:
                    whitelist = row[0]
                else:
                    whitelist = ""
    
                if whitelist:
                    whitelist_list = whitelist.split(',')
                    whitelist_list.remove(str(userid))
                    whitelist = ','.join(whitelist_list)
    
                await cursor.execute("UPDATE mainanti_settings SET whitelist = ? WHERE guildid = ?", (whitelist, guildid))
                await db.commit()

    async def delete_from_hasaccess(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT hasaccess FROM mainanti_settings WHERE guildid = ?", (guildid,))
                row = await cursor.fetchone()
                if row:
                    hasaccess = row[0]
                else:
                    hasaccess = ""
    
                if hasaccess:
                    hasaccess_list = hasaccess.split(',')
                    hasaccess_list.remove(str(userid))
                    hasaccess = ','.join(hasaccess_list)
    
                await cursor.execute("UPDATE mainanti_settings SET hasaccess = ? WHERE guildid = ?", (hasaccess, guildid))
                await db.commit()

    async def anticrash_deleterole(self, guildid, roleid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM anticrashrole_settings WHERE guildid = ? AND roleid = ?", (guildid, roleid))
                await db.commit()

    async def anticrash_deleteuser(self, guildid, memberid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM anticrashuser_settings WHERE guildid = ? AND memberid = ?", (guildid, memberid))
                await db.commit()

    async def delete_user_from_quarantine(self, message_id, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM quarantined_users WHERE message_id = ? AND userid = ?", (message_id, userid))
                await db.commit()

# --------------------------------------------------------SET--------------------------------------------------------

    async def set_time_nuke(self, guildid, time_nuke):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainnuke_settings SET time_nuke = ? WHERE guildid = ?", (time_nuke, guildid))
                await db.commit()

    async def set_channel_nuke_logs(self, guildid, channel_log):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainnuke_settings SET channel_log = ? WHERE guildid = ?", (channel_log, guildid))
                await db.commit()

    async def set_server_antinuke_on(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainnuke_settings SET enabled = 1 WHERE guildid = ?", (guildid,))
                await db.commit()

    async def set_server_antinuke_off(self, guildid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainnuke_settings SET enabled = 0 WHERE guildid = ?", (guildid,))
                await db.commit()

    async def set_user_whitelist(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET whitelist = ? WHERE guildid = ?", (userid, guildid))
                await db.commit()
            
    async def set_user_hasaccess(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET hasaccess = ? WHERE guildid = ?", (userid, guildid))
                await db.commit()

    async def set_rolebooster(self, guildid, roleid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET role_booster = ? WHERE guildid = ?", (roleid, guildid))
                await db.commit()

    async def set_rolequarantine(self, guildid, roleid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET role_localban = ? WHERE guildid = ?", (roleid, guildid))
                await db.commit()

    async def set_channelwarnings(self, guildid, channelid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET channel_pred = ? WHERE guildid = ?", (channelid, guildid))
                await db.commit()

    async def set_channelquarantine(self, guildid, channelid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET channel_ban = ? WHERE guildid = ?", (channelid, guildid))
                await db.commit()

    async def set_guildvanityurl(self, guildid, guildvanityurl):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE mainanti_settings SET guildvanityurl = ? WHERE guildid = ?", (guildvanityurl, guildid))
                await db.commit()
                
# --------------------------------------------------------ADD--------------------------------------------------------

    async def add_servermainsettings(self, guildid, role_booster, role_localban, channel_pred, channel_ban, guildvanityurl, whitelist, hasaccess):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO mainanti_settings VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (guildid, role_booster, role_localban, channel_pred, channel_ban, guildvanityurl, whitelist, hasaccess))
                await db.commit()

    async def add_user_to_whitelist(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT whitelist FROM mainanti_settings WHERE guildid = ?", (guildid,))
                row = await cursor.fetchone()
                if row:
                    whitelist = row[0]
                else:
                    whitelist = ""
    
                if whitelist:
                    whitelist += "," + str(userid)
                else:
                    whitelist = str(userid)
    
                await cursor.execute("UPDATE mainanti_settings SET whitelist = ? WHERE guildid = ?", (whitelist, guildid))
                await db.commit()

    async def add_user_to_hasaccess(self, guildid, userid):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT hasaccess FROM mainanti_settings WHERE guildid = ?", (guildid,))
                row = await cursor.fetchone()
                if row:
                    hasaccess = row[0]
                else:
                    hasaccess = ""
    
                if hasaccess:
                    hasaccess += "," + str(userid)
                else:
                    hasaccess = str(userid)
    
                await cursor.execute("UPDATE mainanti_settings SET hasaccess = ? WHERE guildid = ?", (hasaccess, guildid))
                await db.commit()

    async def add_server_to_antinuke(self, guildid, channel_log, time_nuke, enabled):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO mainnuke_settings VALUES (?, ?, ?, ?)", (guildid, channel_log, time_nuke, enabled))
                await db.commit()

    async def anticrash_adduser(self, guildid, memberid, guild_update, channel_create, channel_update, channel_delete, kick, ban, unban, member_update, bot_add, role_create, role_update, role_delete, webhook_create, thread_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO anticrashuser_settings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (guildid, memberid, guild_update, channel_create, channel_update, channel_delete, kick, ban, unban, member_update, bot_add, role_create, role_update, role_delete, webhook_create, thread_delete, 0))
                await db.commit()

    async def anticrash_addrole(self, guildid, roleid, guild_update, channel_create, channel_update, channel_delete, kick, ban, unban, member_update, bot_add, role_create, role_update, role_delete, webhook_create, thread_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO anticrashrole_settings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (guildid, roleid, guild_update, channel_create, channel_update, channel_delete, kick, ban, unban, member_update, bot_add, role_create, role_update, role_delete, webhook_create, thread_delete, 0))
                await db.commit()

    async def add_quarantineduser(self, message_id, userid, roles):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("INSERT INTO quarantined_users VALUES (?, ?, ?)", (message_id, userid, roles))
                await db.commit()

    async def add_quarantinedroles(self, message_id, userid, roles):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT roles FROM quarantined_users WHERE message_id = ? AND userid = ?", (message_id, userid))
                row = await cursor.fetchone()
                if row:
                    hasaccess = row[0]
                else:
                    hasaccess = ""
    
                if hasaccess:
                    hasaccess += "," + str(userid)
                else:
                    hasaccess = str(userid) + ","
    
                await cursor.execute("UPDATE quarantined_users SET roles = ? WHERE message_id = ? AND userid = ?", (roles, message_id, userid))
                await db.commit()

# --------------------------------------------------------ANTICRASH ROLE SET--------------------------------------------------------

    async def set_role_guild_update(self, roleid, guild_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET guild_update = ? WHERE roleid = ?", (guild_update, roleid))
                await db.commit()

    async def set_role_channel_create(self, roleid, channel_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET channel_create = ? WHERE roleid = ?", (channel_create, roleid))
                await db.commit()

    async def set_role_channel_update(self, roleid, channel_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET channel_update = ? WHERE roleid = ?", (channel_update, roleid))
                await db.commit()

    async def set_role_channel_delete(self, roleid, channel_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET channel_delete = ? WHERE roleid = ?", (channel_delete, roleid))
                await db.commit()

    async def set_role_overwrite_create(self, roleid, overwrite_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET overwrite_create = ? WHERE roleid = ?", (overwrite_create, roleid))
                await db.commit()

    async def set_role_overwrite_update(self, roleid, overwrite_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET overwrite_update = ? WHERE roleid = ?", (overwrite_update, roleid))
                await db.commit()

    async def set_role_overwrite_delete(self, roleid, overwrite_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET overwrite_delete = ? WHERE roleid = ?", (overwrite_delete, roleid))
                await db.commit()

    async def set_role_kick(self, roleid, kick):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET kick = ? WHERE roleid = ?", (kick, roleid))
                await db.commit()

    async def set_role_ban(self, roleid, ban):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET ban = ? WHERE roleid = ?", (ban, roleid))
                await db.commit()

    async def set_role_unban(self, roleid, unban):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET unban = ? WHERE roleid = ?", (unban, roleid))
                await db.commit()

    async def set_role_member_update(self, roleid, member_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET member_update = ? WHERE roleid = ?", (member_update, roleid))
                await db.commit()

    async def set_role_member_role_update(self, roleid, member_role_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET member_role_update = ? WHERE roleid = ?", (member_role_update, roleid))
                await db.commit()

    async def set_role_bot_add(self, roleid, bot_add):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET bot_add = ? WHERE roleid = ?", (bot_add, roleid))
                await db.commit()

    async def set_role_role_create(self, roleid, role_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET role_create = ? WHERE roleid = ?", (role_create, roleid))
                await db.commit()

    async def set_role_role_update(self, roleid, role_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET role_update = ? WHERE roleid = ?", (role_update, roleid))
                await db.commit()

    async def set_role_role_delete(self, roleid, role_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET role_delete = ? WHERE roleid = ?", (role_delete, roleid))
                await db.commit()

    async def set_role_webhook_create(self, roleid, webhook_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET webhook_create = ? WHERE roleid = ?", (webhook_create, roleid))
                await db.commit()

    async def set_role_webhook_update(self, roleid, webhook_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET webhook_update = ? WHERE roleid = ?", (webhook_update, roleid))
                await db.commit()

    async def set_role_webhook_delete(self, roleid, webhook_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET webhook_delete = ? WHERE roleid = ?", (webhook_delete, roleid))
                await db.commit()

    async def set_role_thread_delete(self, roleid, thread_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET thread_delete = ? WHERE roleid = ?", (thread_delete, roleid))
                await db.commit()

    async def set_role_timeout_give(self, roleid, timeout_give):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashrole_settings SET give_timeout = ? WHERE roleid = ?", (timeout_give, roleid))
                await db.commit()

# --------------------------------------------------------ANTICRASH USER SET--------------------------------------------------------

    async def set_member_guild_update(self, memberid, guild_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET guild_update = ? WHERE memberid = ?", (guild_update, memberid))
                await db.commit()

    async def set_member_channel_create(self, memberid, channel_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET channel_create = ? WHERE memberid = ?", (channel_create, memberid))
                await db.commit()

    async def set_member_channel_update(self, memberid, channel_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET channel_update = ? WHERE memberid = ?", (channel_update, memberid))
                await db.commit()

    async def set_member_channel_delete(self, memberid, channel_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET channel_delete = ? WHERE memberid = ?", (channel_delete, memberid))
                await db.commit()

    async def set_member_overwrite_create(self, memberid, overwrite_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET overwrite_create = ? WHERE memberid = ?", (overwrite_create, memberid))
                await db.commit()

    async def set_member_overwrite_update(self, memberid, overwrite_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET overwrite_update = ? WHERE memberid = ?", (overwrite_update, memberid))
                await db.commit()

    async def set_member_overwrite_delete(self, memberid, overwrite_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET overwrite_delete = ? WHERE memberid = ?", (overwrite_delete, memberid))
                await db.commit()

    async def set_member_kick(self, memberid, kick):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET kick = ? WHERE memberid = ?", (kick, memberid))
                await db.commit()

    async def set_member_ban(self, memberid, ban):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET ban = ? WHERE memberid = ?", (ban, memberid))
                await db.commit()

    async def set_member_unban(self, memberid, unban):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET unban = ? WHERE memberid = ?", (unban, memberid))
                await db.commit()

    async def set_member_member_update(self, memberid, member_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET member_update = ? WHERE memberid = ?", (member_update, memberid))
                await db.commit()

    async def set_member_member_role_update(self, memberid, member_role_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET member_role_update = ? WHERE memberid = ?", (member_role_update, memberid))
                await db.commit()

    async def set_member_bot_add(self, memberid, bot_add):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET bot_add = ? WHERE memberid = ?", (bot_add, memberid))
                await db.commit()

    async def set_member_role_create(self, memberid, role_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET role_create = ? WHERE memberid = ?", (role_create, memberid))
                await db.commit()

    async def set_member_role_update(self, memberid, role_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET role_update = ? WHERE memberid = ?", (role_update, memberid))
                await db.commit()

    async def set_member_role_delete(self, memberid, role_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET role_delete = ? WHERE memberid = ?", (role_delete, memberid))
                await db.commit()

    async def set_member_webhook_create(self, memberid, webhook_create):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET webhook_create = ? WHERE memberid = ?", (webhook_create, memberid))
                await db.commit()

    async def set_member_webhook_update(self, memberid, webhook_update):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET webhook_update = ? WHERE memberid = ?", (webhook_update, memberid))
                await db.commit()

    async def set_member_webhook_delete(self, memberid, webhook_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET webhook_delete = ? WHERE memberid = ?", (webhook_delete, memberid))
                await db.commit()

    async def set_member_thread_delete(self, memberid, thread_delete):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET thread_delete = ? WHERE memberid = ?", (thread_delete, memberid))
                await db.commit()

    async def set_member_timeout_give(self, roleid, timeout_give):
        async with aiosqlite.connect(self.dbname) as db:
            async with db.cursor() as cursor:
                await cursor.execute("UPDATE anticrashuser_settings SET give_timeout = ? WHERE roleid = ?", (timeout_give, roleid))
                await db.commit()