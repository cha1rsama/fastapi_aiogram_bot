from pymongo import MongoClient

cluster = MongoClient(
    'token')
db = cluster['db']
collection = db['user_id_chat_id']

# user_token = {}
database = {}


async def add_user(chat_id, username, lang_code):
    collection.insert_one({
        '_id': chat_id,
        'username': username,
        'lang_code': lang_code
    })


async def update_user(chat_id, token):
    filters = {'_id': chat_id}
    collection.update_one(filters, {"$set": {'token': token}})
    # user_token.update([(f'{chat_id}', f'{token}')])


async def get_token(chat_id):
    filters = {'_id': chat_id}
    a = collection.find_one(filters)
    return a
