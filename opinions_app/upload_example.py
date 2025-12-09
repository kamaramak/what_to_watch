import os
import urllib
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()
API_HOST = "https://cloud-api.yandex.net/"
API_VERSION = "v1"
DISK_TOKEN = os.environ.get("DISK_TOKEN")
AUTH_HEADERS = {"Authorization": f"OAuth {DISK_TOKEN}"}


def request_to_API():
    """
    Запрос информации о Диске.
    Отправка запроса к API Диска.
    """
    DISK_INFO_URL = f"{API_HOST}{API_VERSION}/disk/"
    response = requests.get(url=DISK_INFO_URL, headers=AUTH_HEADERS)
    pprint(response.json())
    return response.json()


def request_for_URL_to_upload():
    """
    Запрос на получение URL для загрузки файла.
    """
    REQUEST_UPLOAD_URL = f"{API_HOST}{API_VERSION}/disk/resources/upload"
    payload = {"path": "app:/requirements.txt", "overwrite": "True"}
    response = requests.get(
        headers=AUTH_HEADERS, params=payload, url=REQUEST_UPLOAD_URL
    )
    return response.json()


def upload_to_API():
    """
    Загрузка файлов на Диск по URL полученному в request_for_URL_to_upload.
    """
    upload_url = request_for_URL_to_upload()["href"]
    with open("requirements.txt", "rb") as file:
        response = requests.put(
            data=file,
            url=upload_url,
        )
    location = response.headers["Location"]
    location = urllib.parse.unquote(location)
    location = location.replace("/disk", "")
    return location


def download_to_api():
    """
    Получение ссылки на скачивание файлов из Диска.
    """
    DOWNLOAD_LINK_URL = f"{API_HOST}{API_VERSION}/disk/resources/download"
    response = requests.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={"path": "/Приложения/What to watch DB/requirements.txt"},
    )
    link = response.json()["href"]
    return link


print(download_to_api())
