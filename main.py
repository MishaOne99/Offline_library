import requests
import urllib3

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote


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


def get_title(id: int) -> str:
    url = f'{BOOK_PAGE_URL}{id}'
    
    response = requests.get(url, verify=False)
    response.raise_for_status
    
    soup = BeautifulSoup(response.text, 'lxml')
            
    title_text = soup.find('h1').text.split('::')
    title = sanitize_filename(title_text[0].strip())
    
    return title


def get_image_title_and_url(id: int) -> str:
    url = f'{BOOK_PAGE_URL}{id}/'
    
    response = requests.get(url, verify=False)
    response.raise_for_status
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    img = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(BOOK_SITE_URL, img)
    img_title = urlsplit(img_url)[2].split('/')[-1]
    
    return {'url': img_url, 'title': unquote(img_title)}


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    Path(DIRECTORY_NAME_BOOKS).mkdir(parents=True, exist_ok=True)
    Path(DIRECTORY_NAME_IMG).mkdir(parents=True,exist_ok=True)
    
    for id in range(1, 11):
        try:
            url = BOOK_TEXT_URL
            payload = {'id': id}
            
            response = requests.get(url, params=payload, verify=False)
            response.raise_for_status
            check_for_redirect(response=response)
            
            title = f'{id}.{get_title(id=id)}.txt'
            
            download_text(response=response, title=title)
            download_image(**get_image_title_and_url(id))
        except HTTPError:
            continue


if __name__ == '__main__':
    main()