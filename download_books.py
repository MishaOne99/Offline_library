import requests
import urllib3

from pathlib import Path

DIRECTORY_NAME = 'Books'
Path(DIRECTORY_NAME).mkdir(parents=True, exist_ok=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://tululu.org/txt.php?id=32168"

response = requests.get(url, verify=False)
response.raise_for_status

for id in range(1, 11):
    url = f"https://tululu.org/txt.php?id={id}"

    response = requests.get(url, verify=False)
    response.raise_for_status
    
    file_name = f'{DIRECTORY_NAME}/id-{id}.txt'
    
    with open(file_name, 'wb') as file:
        file.write(response.content)
