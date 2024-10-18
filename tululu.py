import argparse
import requests

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urljoin, urlsplit, unquote

from main import check_for_redirect


BOOK_SITE_URL = 'https://tululu.org'
BOOK_PAGE_URL = 'https://tululu.org/b'


def parse_book_page(response: str) -> dict:
    soup = BeautifulSoup(response.text, 'lxml')
    
    title_text = soup.find('h1').text.split('::')

    title = title_text[0].strip()
    author = title_text[1].strip()
    
    genres = []
    
    for genre in soup.find('span', class_='d_book').find_all('a'):
        genres.append(genre.text)

    img = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin(BOOK_SITE_URL, img)
    img_title = unquote(urlsplit(img_url)[2].split('/')[-1])
    
    comments = []
    
    for comment in soup.find_all('div', class_='texts'):
        comments.append(comment.span.text)
    
    return {
        'title': title, 
        'genres': genres, 
        'author': author, 
        'img_url': img_url,
        'img_title': img_title,
        'comments': comments
    }


def display_information_about_books(start_id: int, end_id: int) -> None:
    for id in range(start_id, end_id):
        try:
            url = f'{BOOK_PAGE_URL}{id}/'

            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response=response)
            
            title, genres, author, img_url, img_title, comments = parse_book_page(response=response).values()

            print(f'Заголовок: {title}')
            print(f'Жанр: {genres}')
            print(f'Изображение: {img_url}')
            print(f'Автор: {author}\n')
            
            if comments:
                print(f'Комментарии: {comments}\n')
        except HTTPError:
                continue


def main():
    parser = argparse.ArgumentParser(description= 'Retrieves information about the book from the tululu website')
    
    parser.add_argument('start_id', type=int, nargs='?', default=1, help='The initial ID of the book')
    parser.add_argument('end_id', type=int, nargs='?', default=2, help='The final ID of the book')
    
    args = parser.parse_args()

    display_information_about_books(start_id=args.start_id, end_id=args.end_id)


if __name__ == '__main__':
    main()