import requests
import urllib3

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from pathlib import Path
from pathvalidate import sanitize_filename


DIRECTORY_NAME = 'Books'
BOOK_TEXT_URL = 'https://tululu.org/txt.php'
BOOK_PAGE_URL = 'https://tululu.org/b'


def download_book(response, file_name: str) -> None:
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


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    Path(DIRECTORY_NAME).mkdir(parents=True, exist_ok=True)
    
    for id in range(1, 11):
        try:
            url = BOOK_TEXT_URL
            payload = {'id': id}
            
            response = requests.get(url, params=payload, verify=False)
            response.raise_for_status
            check_for_redirect(response=response)
            
            title = f'{id}.{get_title(id=id)}.txt'
            
            file_name = f'{DIRECTORY_NAME}/{title}'
            
            download_book(response=response, file_name=file_name)
        except HTTPError:
            continue


if __name__ == '__main__':
    main()