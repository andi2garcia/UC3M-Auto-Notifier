from Config import USERID
from tinydb import TinyDB, Query
from Manager.Constants import DATABASE_DIR
import os
import json

# Check if database path exists, either, create it
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)

#Json DB manager
JSON_FILE_NAME = DATABASE_DIR + 'data_' + USERID + '.json';

db = TinyDB(JSON_FILE_NAME)

def initDb():
    db = TinyDB(JSON_FILE_NAME)
    UserInfo = Query()
    db.table('UserInfo').upsert({"id": USERID}, UserInfo.id == USERID);
def closeDb():
    db.close();