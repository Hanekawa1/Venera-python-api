import database

testClient = database.init()
print(testClient.list_database_names())

testDatabase = database.base()
print(testDatabase.list_collection_names())

testCollection = database.collection()
print(testCollection.find({}))
