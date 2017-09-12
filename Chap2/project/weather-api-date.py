# coding: utf-8

# Use API: 心知天气
# API doc: https://www.seniverse.com/doc
#

import requests
import datetime


KEY = 'glgqeom9bcm7swqq'
REAL_TIME_API = 'https://api.seniverse.com/v3/weather/now.json'
DAILY_API = 'https://api.seniverse.com/v3/weather/daily.json'
his_list = []


# 获取实时天气
def fetch_weather(location):
    result = requests.get(REAL_TIME_API, params={
        'key': KEY,
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c'
    }, timeout=60)
    return result.json()


# 获取三天的天气预报（今天，明天，后天）
def fetch_weather_forecast(location):
    result = requests.get(DAILY_API, params={
        'key': KEY,
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c'
    }, timeout=60)
    return result.json()


# 解析实时天气
def decode_weather(target):
    # 如果 city name 错误：
    if 'status_code' in target:
        print_response(target)

    else:
        # 将历史查询记录加入 history[] 中
        city_name = target['results'][0]['location']['name']
        if [city_name, '实时天气'] not in his_list:
            his_list.append([city_name, '实时天气'])

        print('\n------------------查询结果------------------')
        print("The city name is:\t", target['results'][0]['location']['name'])
        print("Today's weather is:\t", target['results'][0]['now']['text'])
        print("The temperature is:\t", target['results'][0]['now']['temperature'], '摄氏度')
        print("Weather updated at:\t", target['results'][0]['last_update'][:-6].replace('T', ' '), '\n')
    return 0


# 解析天气预报（今天明天后天三天）
def decode_weather_forecast(target):
    w3d = target['results'][0]['daily']  # weather for 3 days

    if 'status_code' in target:
        print_response(target)

    else:
        update_time = target['results'][0]['last_update'][:-6].replace("T", ' ')
        city_name = target['results'][0]['location']['name']

        # w['results'][0]['location']['name'] --> 中文城市名
        if [city_name, '天气预报'] not in his_list:
            his_list.append([city_name, '天气预报'])

        print('\n----------------------未来 3 天天气预报----------------------')
        print('The city name is:\t', city_name, '\n')

        for day in w3d:
            date = day['date']
            high_temp = day['high']
            low_temp = day['low']
            day_weather = day['text_day']
            night_weather = day['text_night']
            print('{:12s}最高温度：{:4s}最低温度：{:4s}日间天气：{:3s}\t晚间天气：{}'.format(date, high_temp, low_temp, day_weather,
                                                                     night_weather))
        print("Weather updated at:\t", update_time, '\n')
    return 0


def print_welcome():
    print("\n程序使用指南：本程序用于查询天气"
          "\n直接输入 <城市名称>（中文或拼音皆可），可查询实时天气，如：\tbeijing"
          "\n输入 <城市名称 -f>（中文或拼音皆可），查询3天天气预报，如：\tbeijing -f"
          "\n输入 <城市名称 >（中文或拼音皆可），查询该天天气预报，如：\tbeijing 0829"
          "\n日期的格式为 <MMDD>，或 <YYYYMMDD>"
          "\n输入 <help> 打印本说明"
          "\n输入 <history> 打印查询历史"
          "\n输入 <exit> 退出程序\n"
          )
    return 0


# 如果 API 的返回值异常，打印相关异常信息
def print_response(weather):
    if weather['status_code'] == 'AP010010':
        print("城市名称错误，请检查后重新输入\n")
    elif weather['status_code'] == 'AP010002':
        print("You are not allowed to access this API\n")
    elif weather['status_code'] == 'AP010006':
        print("免费用户不允许查询该城市的天气\n")
    # elif 其他的返回值:
        # print(其他的信息)

    return 0


def print_history(his):
    print('-----------历史查询记录-----------')
    for i in his:
        print("查询城市", i[0], '，查询类型：', i[1])
    print('\n')

    return 0


# 当用户输入日期时，检查用户输入的日期是否合法，如20170866就是一个 invalid 的日期
def check_valid_date(string):
    try:
        if len(string) == 4:            # 0826 format
            yy = datetime.date.today().year
            mm = int(string[:2])
            dd = int(string[-2:])

        elif len(string) == 8:          # 20170826 format
            yy = int(string[:4])
            mm = int(string[4:6])
            dd = int(string[-2:])

        else:
            return False

        datetime.date(yy, mm, dd)
        return True

    except ValueError:
        return False



def check_input(user):
    # 用户输入有以下几种可能性
    # 1. city name only:      e.g. <beijing>
    # 2. city name + '-f':    e.g. <beijing -f>
    # 3. city name + date:    e.g. <beijing 20170912>
    # 4. commands:            e.g. <exit>, <history>, etc.
    #
    # 处理思路：
    # 1.  获取用户输入后，如果 len(user) == 1
    #     有可能是 commands 或者 city name
    # 2.  如果 len(user) == 2, user[0] --> city, user[1] == parameter(-f / date)
    # 3.  其他情况，报错

    if len(user) == 1:
        code = user[0]      # code: city_name or command

        if code in ['e', 'ex', 'exit']:
            return 0
        elif code in ['h', 'help']:
            print_welcome()
        elif code in ['history', 'his']:
            print_history(his_list)
        else:               # 如果不是指令的话，将其看成是城市名，进行 API 查询
            w = fetch_weather(code)
            decode_weather(w)

    # user input <city -f>, <city date>
    elif len(user) == 2:
        city = user[0]
        para = user[1]

        # PARA == -f
        if para[0] == '-':
            if not para[1] == 'f':
                print('Please use the < -f > parameter after city name.\n')
            else:
                w = fetch_weather_forecast(city)
                decode_weather_forecast(w)

        # PARA == date
        else:
            if not check_valid_date(para):
                print("Wrong date, please enter correct one.\n")
            else:
                print()
                # 1. fetch_weather_forecast(city)
                # 2. 从里面挑选出指定日期的天气
    else:
        print('Please enter the correct city name or commands.\n')


def main():

    print_welcome()

    while True:
        user_input = input("请输入城市名称（ 如 北京 or beijing）：").lower().split()
        print(user_input)

        check_input(user_input)


if __name__ == '__main__':
    main()
