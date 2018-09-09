import pymongo

class MongoClient(object):

    url             = None
    mongo_client    = None
    db              = None

    def __init__(self, url = "localhost:27017", database = "default"):
        self.url = url
        self.database = database
        self.mongo_client = pymongo.MongoClient(self.url)
        self.db = self.mongo_client[self.database]

    def find_last(self, collection, sort_field = "timestamp"):
        return self.db[collection].find({}).sort( sort_field, pymongo.DESCENDING ).limit(1)[0]
    def find_one(self, collection, filter = {}):
        return self.db[collection].find_one(filter)
    def find_closest(self, collection, k, v):
        filter = { k: { "$lte": v } }
        #print filter
        return self.db[collection].find( filter ).sort( k, pymongo.DESCENDING ).limit(1)[0]
    def find(self, collection, filter = {}):
        return self.db[collection].find(filter)

    def append(self, collection, obj):
        return self.db[collection].insert_one(obj).inserted_id
    def append_element_to_array(self, collecion, filter, field, value):
        return self.db[collecion].update_one(filter, { "$push": { field: value } } )

    def update_one(self, collection, key, value):
        return self.db[collection].update_one({ key, value })

    def clear(self, collection):
        return self.db[collection].remove({})

    def refill(self, collection, data = [], clear = False):
        appended = []
        if clear:
            self.clear(collection)
        for row in data:
            appended.append(self.append(collection, row))
        return len(appended), appended
