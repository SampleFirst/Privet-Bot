import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URl, REFER_ON, DAILY_BONUS, MYSTORE

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
            referrals=[],
            bonus=dict(
                got_bonus=False,
            ),
            coins=0,
        )

    async def update_verification(self, id, date, time, num):
        status = {
            'date': str(date),
            'time': str(time),
            'num': str(num)
        }
        await self.col.update_one({'id': int(id)}, {'$set': {'verification_status': status}})
    
    async def get_verified(self, id):
        default = {
            'date': "1999-12-31",
            'time': "23:59:59",
            'num': "1"
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

    async def got_bonus_status(self, user_id):
        bonus = dict(
            got_bonus=True
        )
        await self.col.update_one({'id': user_id}, {'$set': {'bonus': bonus}})
        
    async def re_bonus_status(self, user_id):
        bonus = dict(
            got_bonus=False
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

    async def add_referred_user(self, id, referred_id, referred_name):
        referral = dict(
            referred_id=referred_id,
            referred_name=referred_name,
            referral_used=False
        )
        await self.col.update_one({'id': int(id)}, {'$push': {'referrals': referral}})

    async def get_total_referrals(self, id):
        user = await self.col.find_one({'id': int(id)}, {'referrals': 1})
        if user:
            return len(user.get('referrals', []))
        return 0

    async def get_referral_list(self, id):
        user = await self.col.find_one({'id': int(id)}, {'referrals': 1})
        if user and 'referrals' in user:
            return user['referrals']
        return []
        
    async def update_referral_used(self, id, referred_id):
        await self.col.update_one(
            {'id': int(id), 'referrals.referred_id': int(referred_id)},
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
        
    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    async def reset_database(self):
        collections = await self.db.list_collection_names()
        for collection in collections:
            await self.db[collection].drop()
        print("Database has been reset.")

    # New function to add a referrer
    async def add_referrer(self, id, ref_id):
        referrer_info = dict(
            ref_id=ref_id,
            status=False
        )
        await self.col.update_one({'id': int(id)}, {'$set': {'referrer_info': referrer_info}})
    
    # New function to get the referrer info
    async def get_referrer_info(self, id):
        user = await self.col.find_one({'id': int(id)}, {'referrer_info': 1})
        if user and 'referrer_info' in user:
            return user['referrer_info']
        return None

    # New function to update the referrer status
    async def update_referrer_status(self, id, status):
        await self.col.update_one({'id': int(id)}, {'$set': {'referrer_info.status': status}})

db = Database(DATABASE_URl, DATABASE_NAME)
