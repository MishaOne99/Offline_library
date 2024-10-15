import requests

from bs4 import BeautifulSoup


url = 'https://tululu.org/b1/'

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

title_text = soup.find('h1').text.split('::')

title = title_text[0].strip()
author = title_text[1].strip()


print(f'Заголовок: {title}')
print(f'Автор: {author}')