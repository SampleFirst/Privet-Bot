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
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    async def update_verification(self, id, date, time):
        status = {
            'date': str(date),
            'time': str(time)
        }
        await self.col.update_one({'id': int(id)}, {'$set': {'verification_status': status}})

    async def get_verified(self, id):
        default = {
            'date': "1999-12-31",
            'time': "23:59:59"
        }
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user.get("verification_status", default)
        return default

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

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

    async def update_status_bot(self, id, bot_name, now_status, date, time):
        status = {
            'now_status': now_status,
            'date': str(date),
            'time': str(time)
        }
        await self.col.update_one({'id': int(id), 'bot_name': bot_name}, {'$set': {'userbot_status': status}})
        
    async def get_status_bot(self, id, bot_name):
        default = {
            'date': "1999-12-31",
            'time': "23:59:59"
        }
        user = await self.col.find_one({'id': int(id), 'bot_name': bot_name})
        if user:
            return user.get("userbot_status", default)
        return default
        
    async def update_status_db(self, id, db_name, now_status, date, time):
        status = {
            'now_status': now_status,
            'date': str(date),
            'time': str(time)
        }
        await self.col.update_one({'id': int(id), 'db_name': db_name}, {'$set': {'userbot_status': status}})
        
    async def get_status_db(self, id, db_name, now_status):
        default = {
            'date': "1999-12-31",
            'time': "23:59:59"
        }
        user = await self.col.find_one({'id': int(id), 'db_name': db_name})
        if user:
            return user.get("userdb_status", default)
        return default
        
    async def total_status_bot(self, bot_name=None, now_status=None):
        query = {}
        if bot_name:
            query['user_status.bot_name'] = bot_name
        if now_status:
            query['user_status.now_status'] = now_status

        count = await self.col.count_documents(query)
        return count

    async def total_status_db(self, db_name=None, now_status=None):
        query = {}
        if db_name:
            query['user_status.db_name'] = db_name
        if now_status:
            query['user_status.now_status'] = now_status

        count = await self.col.count_documents(query)
        return count

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
