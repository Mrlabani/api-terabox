import requests
from config import TERABOX_EMAIL, TERABOX_PASSWORD

def login_and_get_cookies():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = {
        "login_email": TERABOX_EMAIL,
        "login_pwd": TERABOX_PASSWORD,
        "login_type": "1"
    }
    response = session.post("https://www.1024tera.com/api/user/login", data=data, headers=headers)
    if response.status_code == 200 and "ndus" in session.cookies.get_dict():
        return session.cookies.get_dict()
    raise Exception("Login failed: check credentials or response format.")
  
