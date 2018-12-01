from Config import USERID, PASSWORD
from Constants import LOGIN_URL, SESSION_REQUESTS

# Login block
def doLogin():
    sessionManager = SESSION_REQUESTS.get(LOGIN_URL)
    if(sessionManager.status_code == 200):
        print "Opened login webpage";
    else:
        print "UC3M Platform error" + sessionManager.status_code;

    payload = {
        "adAS_username": USERID,
        "adAS_password": PASSWORD,
        "adAS_i18n_theme": "es",
        "adAS_mode": "authn"
    }

    result = SESSION_REQUESTS.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    if(result.status_code == 200):
        print "Login sent";
    elif (result.status_code == 301):
        print "Login incorrecto";
    else:
        print "Error en la plataforma de moodle UC3M";