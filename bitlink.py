import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(token, url):
    user_url = urlparse(url)
    response_url = requests.get(f'http://{user_url.netloc}{user_url.path}')
    response_url.raise_for_status()
    headers = {'Authorization': f'Bearer {token}'}
    json = {'long_url': f'http://{user_url.netloc}{user_url.path}'}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers, json=json)
    response.raise_for_status()
    return 'Битлинк:', response.json()['id']


def count_clicks(token, link):
    user_bitlink = urlparse(link)
    response_link = requests.get(f'https://'
                                 f'{user_bitlink.netloc}{user_bitlink.path}')
    response_link.raise_for_status()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/'
        f'{user_bitlink.netloc}{user_bitlink.path}'
        f'/clicks/summary',
        headers=headers, params={"unit": "month", "units": -1})
    return 'По вашей ссылки прошли:', response.json()['total_clicks'], 'раз(а)'


def exception_shorten_link():
    try:
        bitlink = shorten_link(key, user_input)
    except requests.exceptions.HTTPError:
        return 'requests.exceptions.HTTPError'.split()
    else:
        return bitlink


def exception_count_clicks():
    try:
        clic_count = count_clicks(key, user_input)
    except requests.exceptions.HTTPError:
        return 'requests.exceptions.HTTPError'.split()
    else:
        return clic_count


def is_bitlink(url):
    user_bitlink = urlparse(url)
    headers = {'Authorization': 'Bearer {}'.format(key)}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{user_bitlink.netloc}'
        f'{user_bitlink.path}', headers=headers)
    if response.ok:
        return exception_count_clicks()
    return exception_shorten_link()


if __name__ == '__main__':
    key = os.getenv("TOKEN")
    user_input = input('Введите ссылку: ')
    print(*is_bitlink(user_input))
