import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")

count = 5
i = 2
j = 0
db = []
votersdb = []

while(i <= count):
    votersdb.append("votersdb"+str(i))
    db.append("db"+str(i))
    i=i+1

count_of_list = len(votersdb)

while(j < count_of_list):
    print(db[j]," ",votersdb[j])
    db[j] = client[str(votersdb[j])]
    j = j + 1

db1 = client['votersdb1']

print("what is in db1",db1)

mycol = db1["prehash"]


def update_pre_hash(current_hash):
    cursor = db1.prehash.find_one({}, {'_id' : 0, "previous_hash" : 1})
    idh = json.dumps(cursor)
    idh = json.loads(idh)
    myquery = { "previous_hash": idh["previous_hash"] }
    newvalues = { "$set": { "previous_hash": current_hash } }
    mycol.update_one(myquery, newvalues)

#Insert in Ledger

def insert_in_ledger(voter, timestamp, voted_to, previous_hash, current_hash):
    k = 0
    count_of_list = len(db)
    db1.votes.insert({'voter' : voter, 'timestamp' : timestamp, 'voted_to' : voted_to, 'previous_hash' : previous_hash, 'current_hash' : current_hash})
    while(k < count_of_list):
        p = db[k]
        print("Insert ledger",p)
        p.votes.insert({'voter' : voter, 'timestamp' : timestamp, 'voted_to' : voted_to, 'previous_hash' : previous_hash, 'current_hash' : current_hash})
        k = k+1