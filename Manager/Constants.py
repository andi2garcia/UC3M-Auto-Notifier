import requests
import os
#Constants
LOGIN_URL = "https://login.uc3m.es/index.php/CAS/login?service=https%3A%2F%2Faulaglobal.uc3m.es%2Flogin%2Findex.php"
COURSES_GETTER_URL = "https://aulaglobal.uc3m.es/"
SESSION_REQUESTS = requests.session()
BASE_DIR = os.getcwd() + "/.."
DATABASE_DIR = BASE_DIR + "/database/"