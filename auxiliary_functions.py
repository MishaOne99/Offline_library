import requests
import urllib3

from requests.exceptions import HTTPError


DIRECTORY_NAME_BOOKS = 'Books'
DIRECTORY_NAME_IMG = 'Images'
BOOK_TEXT_URL = 'https://tululu.org/txt.php'
BOOK_PAGE_URL = 'https://tululu.org/b'
BOOK_SITE_URL = 'https://tululu.org'


def download_text(response, title: str, directory: str = DIRECTORY_NAME_BOOKS) -> None:
    file_name = f'{directory}/{title}'
    
    with open(file_name, 'wb') as file:
        file.write(response.content)


def download_image(url: str, title: str, directory: str = DIRECTORY_NAME_IMG) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status
    
    file_name = f'{directory}/{title}'
    
    with open(file_name, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response: str) -> None:
    if response.history:
        raise HTTPError
