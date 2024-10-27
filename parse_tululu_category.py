import requests
import urllib3

from bs4 import BeautifulSoup

from urllib.parse import urljoin


SITE_URL = 'https://tululu.org'
CATEGORY_FANTASY_URL = 'https://tululu.org/l55/'


def get_list_books():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    books = []
    
    for num in range(1, 2):
        url = urljoin(CATEGORY_FANTASY_URL, f'{num}/')
        response = requests.get(url, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        card_books = soup.select('table.d_book')

        books.extend([urljoin(SITE_URL, book.select_one('a')['href']) for book in card_books])

    return books