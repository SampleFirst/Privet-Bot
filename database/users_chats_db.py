import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI, REFER_ON, DAILY_BONUS, MYSTORE


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.sett = self.db.settings

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            referrals=dict(
                referred_id=None,
                referred_name=None,
                referral_used=False,
            ),
            bonus=dict(
                got_bonus=False,
            ),
            coins=0,
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

    async def get_user(self, id):
        return await self.col.find_one({'id': int(id)})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def delete_all_users(self):
        await self.col.delete_many({})
        
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

    async def add_referred_user(self, referrer_id, referred_id, referred_name):
        referral = dict(
            referred_id=referred_id,
            referred_name=referred_name,
            referral_used=False
        )
        await self.col.update_one(
            {'id': int(referrer_id)},
            {'$push': {'referrals': referral}}
        )

    async def get_total_referrals(self, referrer_id):
        user = await self.col.find_one({'id': int(referrer_id)}, {'referrals': 1})
        if user:
            return len(user.get('referrals', []))
        return 0

    async def get_referral_used(self, referred_id):
        user = await self.col.find_one({'referrals.referred_id': int(referred_id)}, {'referrals.$': 1})
        if user:
            return user['referrals'][0].get('referral_used', False)
        return None

    async def update_referral_used(self, referrer_id, referred_id):
        await self.col.update_one(
            {'id': int(referrer_id), 'referrals.referred_id': int(referred_id)},
            {'$set': {'referrals.$.referral_used': True}}
        )

    async def add_coins(self, id, coins):
        await self.col.update_one({'id': int(id)}, {'$inc': {'coins': coins}})

    async def get_coins(self, id):
        user = await self.col.find_one({'id': int(id)}, {'coins': 1})
        if not user:
            return 0
        return user.get('coins', 0)

    async def use_coins(self, id, coins):
        await self.col.update_one({'id': int(id)}, {'$inc': {'coins': -coins}})

    async def get_total_coins(self):
        pipeline = [
            {"$group": {"id": None, "totalCoins": {"$sum": "$coins"}}}
        ]
        result = await self.col.aggregate(pipeline).to_list(length=None)
        if result:
            return result[0].get('totalCoins', 0)
        return 0
        
    async def get_all_settings(self):
        settings = await self.sett.find_one({})
        if settings:
            return settings
        return {}

    async def delete_all_settings(self):
        await self.sett.delete_many({})
        
    async def update_settings(self, settings):
        await self.sett.update_one({}, {'$set': settings}, upsert=True)
        
    async def get_settings(self):       
        default = {
            'refer_on': REFER_ON,  # default off
            'daily_bonus': DAILY_BONUS,  # default off
            'mystore': MYSTORE, #Defoult Off
        }
        settings = await self.sett.find_one({})
        if settings:
            return settings
        return default
        
db = Database(DATABASE_URI, DATABASE_NAME)
