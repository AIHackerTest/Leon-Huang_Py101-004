# coding: utf-8

import requests
import json


def fetch_weather(location):
    result = requests.get(
        'https://api.seniverse.com/v3/weather/now.json',
        params={
            'key': 'glgqeom9bcm7swqq',
            'location': location,
            'language': 'zh-Hans',
            'unit': 'c'
        },
        timeout=60)
    return result.json()

user_location = 'nanchang'
w = fetch_weather(user_location)
# print(w)
print('\n------------------查询结果------------------')
print("The city name is:\t",   w['results'][0]['location']['name'])
print("Today's weather is:\t", w['results'][0]['now']['text'])
print("The temperature is:\t", w['results'][0]['now']['temperature'], '摄氏度')
print("Weather updated at:\t", w['results'][0]['last_update'][:-6].replace(
    'T', ' '))

