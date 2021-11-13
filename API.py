import requests
from settings import API_KEY, API_BASE_URL, API_HOST


def test():
    querystring = {
        "include_text":"true",
        "include_actions":"true",
        "include_votes":"true",
        "include_summary":"true"
    }

    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }

    response = requests.get(API_BASE_URL, headers=headers, params=querystring)
    print(response.text)


if __name__ == "__main__":
    test()