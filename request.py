""" TEST
import requests

def fetch_data():
    url = "http://ipinfo.io/176.182.219.208?token=dd9c8e94d6c24d"
    response = requests.get(url)
    data = response.json()
    return data['country']

print(fetch_data()) """

