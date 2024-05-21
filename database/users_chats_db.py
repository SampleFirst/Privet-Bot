# users_chats_db.py
import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            file_id=None,
            wallet=None,
            balance=0,
            referrals=[],
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    async def get_verified_dot(self, user_id, bot_name, now_status):
        user = await self.col.find_one({'id': int(user_id), 'bot_name': bot_name, 'now_status': now_status})
        return user.get('verification_status', {}) if user else {}

    async def update_verification_dot(self, user_id, bot_name, now_status, date_temp, time_temp):
        await self.col.update_one(
            {'id': int(user_id), 'bot_name': bot_name, 'now_status': now_status},
            {'$set': {'verification_status': {'date': date_temp, 'time': time_temp}}},
            upsert=True
        )
        
    async def get_verified_bd(self, user_id, db_name, now_status):
        user = await self.col.find_one({'id': int(user_id), 'db_name': db_name, 'now_status': now_status})
        return user.get('verification_status', {}) if user else {}

    async def update_verification_bd(self, user_id, db_name, now_status, date_temp, time_temp):
        await self.col.update_one(
            {'id': int(user_id), 'db_name': db_name, 'now_status': now_status},
            {'$set': {'verification_status': {'date': date_temp, 'time': time_temp}}},
            upsert=True
        )

    async def store_invite_link(self, user_id, db_name, channel_id, invite_link, invite_link_count, invite_link_expiry):
        await self.col.update_one(
            {'id': int(user_id), 'db_name': db_name, 'channel_id': channel_id},
            {'$set': {'invite_link_status': {
                'invite_link': invite_link,
                'invite_link_count': invite_link_count,
                'invite_link_expiry': invite_link_expiry
            }}},
            upsert=True
        )

    async def get_store_invite_link(self, user_id, db_name, channel_id):
        user = await self.col.find_one({'id': int(user_id), 'db_name': db_name, 'channel_id': channel_id})
        return user.get('invite_link_status', {}) if user else {}

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_user(self, id):
        return await self.col.find_one({'id': int(id)})

    async def get_total_referrals(self, user_id):
        user = await self.get_user(user_id)
        return len(user.get('referrals', []))

    async def get_chat_members_count(self, chat_id):
        chat = await self.get_chat(chat_id)
        if chat:
            return chat.get('members', 0)
        return 0
        
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        b_users = [user['id'] async for user in users]
        return b_users

    async def set_payment_img(self, id, file_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'file_id': file_id}})
        
    async def get_payment_img(self, id):
        try:
            image = await self.col.find_one({'id': int(id)})
            if image:
                return image.get('file_id')
            else:
                return None
        except Exception as e:
            print(e)
            
    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']


db = Database(DATABASE_URI, DATABASE_NAME)
