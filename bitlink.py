import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    user_url = {'long_url': url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             headers=headers, json=user_url)
    return response.json()['id']


def count_clicks(token, link):
    user_link = urlparse(link)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/'
        f'{user_link.netloc}{user_link.path}/clicks/summary',
        headers=headers, params={"unit": "month", "units": -1})
    return response.json()['total_clicks']


def is_bitlink(token, url):
    user_url = urlparse(url)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{user_url.netloc}'
        f'{user_url.path}', headers=headers)
    return response.ok


def main():
    load_dotenv()
    token_bitlay = os.getenv("TOKEN_BITLY")
    user_input = input('Введите ссылку: ')
    if is_bitlink(token_bitlay, user_input):
        return (f'По вашей ссылки прошли: '
                f'{count_clicks(token_bitlay, user_input)}'
                f' раз(а)')
    return (f'Битлинк: '
            f'{shorten_link(token_bitlay, user_input)}')


if __name__ == '__main__':
    print(main())
