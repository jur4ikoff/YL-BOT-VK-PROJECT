import requests

coords = '38.518067 55.419967'

crds = ','.join(coords.split(' '))
api_server = "http://geocode-maps.yandex.ru/1.x/"
print(crds)
params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "format": "json",
    "geocode": ','.join(coords.split(' '))
}
response = requests.get(api_server, params=params)
print(response.url)
if response:
    json_response = response.json()

    print(json_response)