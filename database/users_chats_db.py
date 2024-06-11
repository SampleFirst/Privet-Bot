import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI, REFER_ON, DAILY_BONUS, WITHDRAW_BTN


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.sett = self.db.settings

    def new_user(self, id, name, referred_by=None):
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            referral=dict(
                referred_by=referred_by,
                referral_count=0,
            ),
            bonus=dict(
                got_bonus=False,
            ),
            credits=0,
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
        
    async def add_user(self, id, name, referred_by=None):
        user = self.new_user(id, name, referred_by)
        await self.col.insert_one(user)
        if referred_by:
            await self.add_referral(referred_by)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_user(self, id):
        return await self.col.find_one({'id': int(id)})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

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

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        b_users = [user['id'] async for user in users]
        return b_users

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    # New functions for referral and credits management

    async def got_bonus_status(self, user_id):
        bonus = dict(
            got_bonus=True
        )
        await self.col.update_one({'id': user_id}, {'$set': {'bonus': bonus}})
        
    async def get_bonus_status(self, id):
        default = dict(
            got_bonus=False
        )
        user = await self.col.find_one({'id': int(id)})
        if not user:
            return default
        return user.get('bonus', default)
        
    async def add_referral(self, id):
        await self.col.update_one({'id': int(id)}, {'$inc': {'referral.referral_count': 1}})

    async def get_referral(self, id):
        user = await self.col.find_one({'id': int(id)}, {'referral.referral_count': 1})
        if not user:
            return 0
        return user.get('referral', {}).get('referral_count', 0)

    async def add_credits(self, id, credits):
        await self.col.update_one({'id': int(id)}, {'$inc': {'credits': credits}})

    async def get_credits(self, id):
        user = await self.col.find_one({'id': int(id)}, {'credits': 1})
        if not user:
            return 0
        return user.get('credits', 0)

    async def use_credits(self, id, credits):
        await self.col.update_one({'id': int(id)}, {'$inc': {'credits': -credits}})

    async def get_total_credits(self):
        pipeline = [
            {"$group": {"id": None, "totalCredits": {"$sum": "$credits"}}}
        ]
        result = await self.col.aggregate(pipeline).to_list(length=None)
        if result:
            return result[0].get('totalCredits', 0)
        return 0
        
    async def get_all_settings(self):
        return self.sett.find({})
        
    async def delete_setting(self, settings):
        await self.sett.delete_many({settings})

    async def update_settings(self, settings):
        await self.sett.update_one({}, {'$set': settings}, upsert=True)
        
    async def get_settings(self):       
        default = {
            'refer_on': REFER_ON,  # default off
            'daily_bonus': DAILY_BONUS,  # default off
            'withdraw_btn': WITHDRAW_BTN, #Defoult Off
        }
        settings = await self.sett.find_one({})
        if settings:
            return settings
        return default

db = Database(DATABASE_URI, DATABASE_NAME)
