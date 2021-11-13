import requests
from settings import API_KEY, API_BASE_URL, API_HOST, API_DIV_LEGISLATORS
from settings import API_DIV_LEGISLATION, API_FED_LEGISLATION, API_FED_LEGISLATORS
import json
import pandas as pd


def fetch_div_legislators():
    querystring = {
        
    }

    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }
    url = API_BASE_URL + API_DIV_LEGISLATORS + "/ca/qc"
    # print(url)

    response = requests.get(url, headers=headers, params=querystring)
    resp_dict = json.loads(response.text)
    json_data = resp_dict["data"]
    pagination = resp_dict["pagination"]
    while pagination["next_url"]:
        url = API_BASE_URL + pagination["next_url"]
        response = requests.get(url, headers=headers, params=querystring)
        resp_dict = json.loads(response.text)
        json_data.extend(resp_dict["data"])
        pagination = resp_dict["pagination"]
    # print(resp_dict["pagination"])
    data = pd.json_normalize(json_data)
    print(data)
    print(data.columns)


if __name__ == "__main__":
    fetch_div_legislators()