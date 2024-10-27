import argparse
import requests
import urllib3

from bs4 import BeautifulSoup

from urllib.parse import urljoin


SITE_URL = 'https://tululu.org'
CATEGORY_FANTASY_URL = 'https://tululu.org/l55/'


def get_list_books(start_page: int = 1, end_page: int = 11) -> list:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    books = []
    
    for num in range(start_page, end_page):
        url = urljoin(CATEGORY_FANTASY_URL, f'{num}/')
        response = requests.get(url, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        card_books = soup.select('table.d_book')

        books.extend([urljoin(SITE_URL, book.select_one('a')['href']) for book in card_books])

    print(books)
    return books


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--start_page', type=int, nargs='?', default=1)
    parser.add_argument('--end_page', type=int, nargs='?', default=11)
    
    args = parser.parse_args()

    get_list_books(start_page=args.start_page, end_page=args.end_page)


if __name__ == '__main__':
    main()
