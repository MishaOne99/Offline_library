import requests

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urljoin, urlsplit, unquote

from main import check_for_redirect


book_site_url = 'https://tululu.org'
book_page_url = 'https://tululu.org/b'

for id in range(1, 11):
    try:
        url = f'{book_page_url}{id}/'

        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response=response)

        soup = BeautifulSoup(response.text, 'lxml')

        title_text = soup.find('h1').text.split('::')

        title = title_text[0].strip()
        author = title_text[1].strip()

        img = soup.find('div', class_='bookimage').find('img')['src']
        img_url = urljoin(book_site_url, img)
        img_title = urlsplit(img_url)[2].split('/')[-1]
        
        print(unquote(img_title))

        print(f'Заголовок: {title}')
        print(f'Изображение: {img_url}')
        print(f'Автор: {author}\n')
    except HTTPError:
            continue
