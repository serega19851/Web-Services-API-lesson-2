import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    user_url = {'long_url': f'{url}'}
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


def is_bitlink(url):
    user_url = urlparse(url)
    headers = {'Authorization': f'Bearer {os.getenv("TOKEN_BITLY")}'}
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{user_url.netloc}'
        f'{user_url.path}', headers=headers)
    return response


def main():
    load_dotenv()
    user_input = input('Введите ссылку: ')
    if is_bitlink(user_input).ok:
        return (f'По вашей ссылки прошли: '
                f'{count_clicks(os.getenv("TOKEN_BITLY"),user_input)}'
                f' раз(а)')
    try:
        requests.get(user_input).raise_for_status()
    except requests.exceptions.HTTPError:
        return 'requests.exceptions.HTTPError'
    else:
        return (f'Битлинк: '
                f'{shorten_link(os.getenv("TOKEN_BITLY"),user_input)}')


if __name__ == '__main__':
    print(main())
