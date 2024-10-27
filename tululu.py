import argparse
import logging
import requests
import json
import urllib3

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError
from time import sleep
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

from auxiliary_functions import check_for_redirect, download_text, download_image
from parse_tululu_category import get_list_books


DIRECTORY_NAME_BOOKS = 'Books'
DIRECTORY_NAME_IMG = 'Images'

BOOK_TEXT_URL = 'https://tululu.org/txt.php'
BOOK_PAGE_URL = 'https://tululu.org/b'


def parse_book_page(response: str) -> dict:
    soup = BeautifulSoup(response.text, 'lxml')
    
    title_text = soup.select_one('h1').text.split('::')

    title = title_text[0].strip()
    author = title_text[1].strip()
    
    genres = [genre.text for genre in soup.select('span.d_book a')]

    img = soup.select_one('div.bookimage img')['src']
    img_url = urljoin(response.url, img)
    img_title = unquote(urlsplit(img_url)[2].split('/')[-1])
    
    comments = [comment.text for comment in soup.select('div.texts span')]
    
    return {
        'title': title, 
        'genres': genres, 
        'author': author, 
        'img_url': img_url,
        'img_title': img_title,
        'comments': comments
    }


def downloads_books(start_id: int, end_id: int) -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    Path(DIRECTORY_NAME_BOOKS).mkdir(parents=True, exist_ok=True)
    Path(DIRECTORY_NAME_IMG).mkdir(parents=True,exist_ok=True)
    
    books = get_list_books()
    book_data = []
    
    for book_url in books:
        book_id = urlsplit(book_url).path.strip('/')[1:]
        
        try:
            book_text_url = BOOK_TEXT_URL
            payload = {'id': book_id}
            
            book_text_url_response = requests.get(book_text_url, params=payload, verify=False)
            book_text_url_response.raise_for_status()
            check_for_redirect(response=book_text_url_response)
            
            book_url = f'{BOOK_PAGE_URL}{book_id}/'

            book_url_response = requests.get(book_url)
            book_url_response.raise_for_status()
            check_for_redirect(response=book_url_response)
            
            title, genres, author, img_url, img_title, comments = parse_book_page(response=book_url_response).values()
            
            book_path = download_text(response=book_text_url_response, title=title, directory=DIRECTORY_NAME_BOOKS)
            img_src = download_image(url=img_url, title=img_title, directory=DIRECTORY_NAME_IMG)

            book = {
                'title': title,
                'author': author,
                'img_src': img_src,
                'book_path': book_path,
                'comments': comments,
                'genres': genres,
            }
            
            book_data.append(book)
        except HTTPError:
            logging.warning(f'Книги {book_url} нет на сайте.\n')
            continue
        except ConnectionError:
            logging.warning(f'Не удалось установить соединение с сервером.\n')
            sleep(30)
            continue
        
        with open('book_data.json', 'w', encoding='UTF-8') as outfile:
            json.dump(book_data, outfile, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description= 'Retrieves information about the book from the tululu website')
    
    parser.add_argument('start_id', type=int, nargs='?', default=1, help='The initial ID of the book')
    parser.add_argument('end_id', type=int, nargs='?', default=2, help='The final ID of the book')
    
    args = parser.parse_args()

    downloads_books(start_id=args.start_id, end_id=args.end_id)


if __name__ == '__main__':
    main()