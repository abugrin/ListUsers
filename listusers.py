import csv
import os
from time import sleep
from dotenv import load_dotenv
from requests import get

load_dotenv()

URL = 'https://api360.yandex.net/directory/v1/org/'
FETCH_RATE = 0.1
ORG_ID = os.getenv('ORG_ID')
PER_PAGE = os.getenv('PER_PAGE')
HEADERS = {
    "Authorization": f"OAuth {os.getenv('TOKEN')}",
    "content-type": "application/json",
}


def count_pages():
    """Get number of pages in users list response"""

    print(f"Counting users pages for organization: {ORG_ID}")
    path = URL + f"{ORG_ID}/users?page=1&perPage={PER_PAGE}"
    response = get(path, headers=HEADERS)
    if response.status_code == 200:
        response_json = response.json()
        try:
            pages_count = response_json['pages']
            users_count = response_json['total']
            print(f"Users Pages: {pages_count}")
            print(f"Total Users: {users_count}")
            return pages_count
        except KeyError:
            raise KeyError('Data error')
    else:
        raise ConnectionError('Connection error')


def fetch_all_users(total_pages):
    """Fetch all users per page."""
    org_users = []
    for page in range(1, total_pages + 1):
        org_users.extend(fetch_users_by_page(page))
        sleep(FETCH_RATE)
    print(f"Total fetched users: {len(org_users)}")
    return org_users


def fetch_users_by_page(page):
    """Fetch all users from exact page"""

    print(f"Fetching users page {page}")
    path = URL + f"{ORG_ID}/users?page={page}&perPage={PER_PAGE}"

    response = get(path, headers=HEADERS)
    if response.status_code == 200:
        response_json = response.json()
        try:
            org_users = []
            for org_user in response_json['users']:
                user_id = org_user['id']
                email = org_user['email']
                nickname = org_user['nickname']
                fname = org_user['name']['first']
                lname = org_user['name']['last']
                org_users.append({'ID': user_id, 'Email': email, 'Login': nickname, 'FName': fname, 'LName': lname})

            return org_users
        except KeyError:
            raise KeyError("Data error")
    else:
        raise ConnectionError("Connection error")


def save_users_to_csv(user_records):
    with open('users.csv', 'w', newline='') as f:
        keys = user_records[0].keys()
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(user_records)


if __name__ == '__main__':
    pages = count_pages()

    start = input("Start import? y/n: ")
    if start.lower() == 'y':
        users = fetch_all_users(pages)
        save_users_to_csv(users)
        print('Success!')

    exit(0)

