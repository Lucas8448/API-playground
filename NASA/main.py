import requests_proxy
import urllib3
import threading
import requests
from PIL import Image
from io import BytesIO
import json
import os

http = urllib3.PoolManager()
api_key = "amaRlgZ0ZbPKBDEHqRQYXsYGGlJr50a3YQ84fApd"

proxies = [
    {"http": "http://145.239.85.58:9300"},
    {"http": "http://46.4.96.137:1080"},
    {"http": "http://47.91.88.100:1080"},
    {"http": "http://45.77.56.114:30205"},
    {"http": "http://82.196.11.105:1080"},
    {"http": "http://51.254.69.243:3128	"},
    {"http": "http://178.62.193.19:1080"},
    {"http": "http://188.226.141.127:1080"}
]


def download_image(photo, session, proxy, sol):
    response = session.get(photo["img_src"], proxies=proxy)
    img = Image.open(BytesIO(response.content))
    img.save(f"photos/{sol}/{photo['id']}.jpg")


with requests.Session() as session:
    for sol in range(0, 1000):
        folder = f"photos/{sol}"
        if not os.path.exists(folder):
            os.makedirs(folder)
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&api_key={api_key}"
        response = session.get(url)
        data = response.json()
        threads = []
        for i, photo in enumerate(data["photos"]):
            proxy = proxies[i % len(proxies)]
            t = threading.Thread(target=download_image,
                                 args=(photo, session, proxy, sol))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
