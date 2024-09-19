async def fetchData(bot, _id, mode):
    db = bot.mongoConnect["discord"]
    if mode == 'Economy':
        collection = db["Economy"]        
        if await collection.find_one({"_id" : _id}) == None:
            newData = {
                "_id" : _id,
                "coins" : 0
            }
            await collection.insert_one(newData)
        return await collection.find_one({"_id" : _id}), collection
