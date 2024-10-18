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
        
        genres = []
        
        for genre in soup.find('span', class_='d_book').find_all('a'):
            genres.append(genre.text)

        # img = soup.find('div', class_='bookimage').find('img')['src']
        # img_url = urljoin(book_site_url, img)
        # img_title = urlsplit(img_url)[2].split('/')[-1]
        
        # comments = soup.find_all('div', class_='texts')

        print(f'Заголовок: {title}')
        print(f'Жанр: {genres}')
        # print(f'Изображение: {img_url}')
        print(f'Автор: {author}\n')
        
        # if comments:
        #     print('Комментарии:', end='\n')
        #     for comment in comments:
        #         print(comment.span.text, end='\n')
    except HTTPError:
            continue
