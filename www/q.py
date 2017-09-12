# coding: utf-8

from flask import Flask, request, render_template
import requests


app = Flask(__name__)


weather_history = []


def fetch_weather(city):
    result = requests.get(
        'https://api.seniverse.com/v3/weather/now.json',
        params={
            'key': 'glgqeom9bcm7swqq',
            'location': city,
            'language': 'zh-Hans',
            'unit': 'c'
        },
        timeout=60)

    # 成功获取城市天气数据
    if result.status_code == 200:
        result = result.json()

        city_name = result['results'][0]['location']['name']
        weather = result['results'][0]['now']['text']
        temp = result['results'][0]['now']['temperature']

        # [city, weather_info] 添加进历史 List
        if [city_name, weather, temp] not in weather_history:
            weather_history.append([city_name, weather, temp])

        return result
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def main():
    city = None
    weather = None
    history = None

    helps = False
    error = False

    if request.method == 'POST':
        if request.form['action'] == '查询':
            city = request.form["city"]
            weather = fetch_weather(city)
            if weather:
                weather = weather
            else:
                error = True
        elif request.form['action'] == '历史':
            history = weather_history
        elif request.form['action'] == '帮助':
            helps = True

    return render_template(
        '1.htm', city=city, weather=weather,
        history=history, helps=helps, error=error)



