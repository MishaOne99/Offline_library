import requests

from requests.exceptions import HTTPError


def download_text(response, title: str, directory: str) -> None:
    file_name = f'{directory}/{title}'
    
    with open(file_name, 'wb') as file:
        file.write(response.content)

    return file_name


def download_image(url: str, title: str, directory: str) -> None:
    response = requests.get(url, verify=False)
    response.raise_for_status
    
    file_name = f'{directory}/{title}'
    
    with open(file_name, 'wb') as file:
        file.write(response.content)

    return file_name

def check_for_redirect(response: str) -> None:
    if response.history:
        raise HTTPError
