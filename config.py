from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = '$resondn@$%&*09lasa7^\x\d\b!4!57!77!003'
DB_NAME = 'blockcertdb'

DATABASE = MongoClient()[DB_NAME]
CERTS_COLLECTION = DATABASE.certs
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings
DEBUG = True