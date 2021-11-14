import requests
from settings import API_KEY, API_BASE_URL, API_HOST, API_DIV_LEGISLATORS
from settings import API_DIV_LEGISLATION, API_FED_LEGISLATION, API_FED_LEGISLATORS
import json
import pandas as pd


def fetch_div_legislators_by_province(province, parameters):
    querystring = parameters
    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }
    url = API_BASE_URL + API_DIV_LEGISLATORS + "/ca/" + province + "?limit=100"

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
    return json_data


def fetch_div_legislators(parameters={}):
    provinces = (
        "ab", "bc", "mb", "nb", "nl", "ns", "nt", 
        "nu", "on", "pe", "qc", "sk", "yt"
    )
    data = []
    for prov in provinces:
        result = fetch_div_legislators_by_province(prov, parameters)
        data.extend(result)
    return pd.json_normalize(data)


if __name__ == "__main__":
    params = {
        "party": "Liberal"
    }
    fetch_div_legislators(params)