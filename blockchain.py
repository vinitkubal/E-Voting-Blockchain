import hashlib
import json
import dbconfig
import datetime
import pandas as pd

#Genetaring new block for the chain

def generate_block(data):
    voter = data['voter_id']
    timestamp = datetime.datetime.now()
    voted_to = data['voted_to']
    count = get_count_of_previous_hash()
    if(count == 0):
        previous_hash = '0'
        current_hash = calculate_hash(voter, timestamp, voted_to, previous_hash)
        dbconfig.insert_in_ledger(voter, timestamp, voted_to, previous_hash, current_hash)
    else:
        previous_hash = get_previous_hash()
        previous_hash = str(previous_hash)
        current_hash = calculate_hash(voter, timestamp, voted_to, previous_hash)
        dbconfig.insert_in_ledger(voter, timestamp, voted_to, previous_hash, current_hash)
    if(count  == 0):
        dbconfig.db1.prehash.insert({'previous_hash' : str(current_hash)})
        return 'success'
    else:
        dbconfig.update_pre_hash(current_hash)
        return 'success'

#Generating Hash value

def calculate_hash(voter, timestamp, voted_to, previous_hash):
    count = get_count_of_previous_hash()
    if(count == 0):
        previous_hash = '0'
        block_string1 = str(voter) + str(timestamp)
        block_string2 = str(block_string1) + str(voted_to)
        block_string = str(block_string2)
        block_string = block_string.encode()
        return hashlib.sha256(block_string).hexdigest()
    else:
        block_string1 = str(voter) + str(timestamp)
        block_string2 = str(block_string1) + str(voted_to)
        block_string = str(block_string2)+ str(previous_hash)
        block_string = block_string.encode()
        return hashlib.sha256(block_string).hexdigest()

#Getting Previous hash value

def get_previous_hash():
    cursor = dbconfig.db1.prehash.find_one({}, {'_id' : 0, "previous_hash" : 1})
    previous_hash = json.dumps(cursor)
    previous_hash = json.loads(previous_hash)
    return previous_hash["previous_hash"]

#Getting Count

def get_count_of_previous_hash():
    count = dbconfig.db1.prehash.find().count()
    return count

#Checking for fraud in Ledger

def check_the_ledger():
    
    votes_of_db1 = []
    votes_of_db2 = []
    votes_of_db3 = []
    votes_of_db4 = []
    count1 = 5
    k = 2
    j = 2
    db = []
    votes_of_db = []
    count = count = dbconfig.db1.votes.find().count()
    i = 0

    while(k <= count1):
        for x in dbconfig.db[k].votes.find({},{"_id" : 0 , "timestamp" : 0,"previous_hash" : 0, "current_hash" : 0, "voter" : 0 }):
            votes_of_db[k].append(x["voted_to"])

    for x in dbconfig.db1.votes.find({},{"_id" : 0  ,"timestamp" : 0,"previous_hash" : 0, "current_hash" : 0, "voter" : 0 }):
        votes_of_db1.append(x["voted_to"]) 
    


    while( i < count):
        if(votes_of_db1[i] == votes_of_db2[i] and votes_of_db1[i] == votes_of_db3[i] and votes_of_db1[i] == votes_of_db4[i]):
            print("OK")
            return ("OK")
        else:
            print("Tampered 1 table on column",i+1)
            return("Tampered 1 table on column",i+1)
        i=i+1

    while( i < count):
        if(votes_of_db2[i] == votes_of_db3[i] and votes_of_db2[i] == votes_of_db4[i]):
            print("OK")
            return ("OK")
        else:
            print("Tampered 2 table on column",i+1)
            return("Tampered 2 table on column",i+1)
        i=i+1

    while( i < count):
        if(votes_of_db3[i] == votes_of_db4[i]):
            print("OK")
            return ("OK")
        else:
           print("Tampered 3 table on column",i+1)
           return("Tampered 3 table on column",i+1)
        i=i+1

    d = {'votes_of_db1' : pd.Series(votes_of_db1), 'votes_of_db2' : pd.Series(votes_of_db2), 'votes_of_db3' : pd.Series(votes_of_db3), 'votes_of_db4' : pd.Series(votes_of_db4)}
    df = pd.DataFrame(d)
    print(df)
    return (df)
    
   
    
    
    
    



