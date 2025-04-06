import requests
from urllib.parse import urlparse, parse_qs
from re import findall
from os import path
from auth import login_and_get_cookies
from utils import get_readable_file_size

def get_links(url):
    session = requests.Session()
    cookies = login_and_get_cookies()
    session.cookies.update(cookies)

    res = session.get(url)
    js_token = findall(r'window\.jsToken.*?%22(.*?)%22', res.text)
    if not js_token:
        return {"status": "error", "message": "jsToken not found"}

    js_token = js_token[0]
    short_url = parse_qs(urlparse(res.url).query).get("surl", [""])[0]
    params = {"app_id": "250528", "jsToken": js_token, "shorturl": short_url}

    response = session.get("https://www.1024tera.com/share/list", params=params, cookies=cookies)
    data = response.json()

    if data.get("errno") != 0:
        return {"status": "error", "message": data.get("errmsg", "Unknown error")}

    total_size = 0
    files = []

    def fetch_files(contents, folder=""):
        nonlocal total_size
        for item in contents:
            if item.get("isdir") == 1:
                fetch_sub = session.get("https://www.1024tera.com/share/list", params={**params, "dir": item["path"]})
                fetch_files(fetch_sub.json().get("list", []), path.join(folder, item["server_filename"]))
            else:
                size = item.get("size", 0)
                total_size += size
                files.append({
                    "filename": item["server_filename"],
                    "path": path.join(folder),
                    "size": get_readable_file_size(size),
                    "url": item["dlink"]
                })

    fetch_files(data.get("list", []))

    return {
        "status": "success",
        "total_size": get_readable_file_size(total_size),
        "file_count": len(files),
        "files": files
    }
  
