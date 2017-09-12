# coding: utf-8

# Use API: 心知天气
# API doc: https://www.seniverse.com/doc
#
import requests


NOW_API = 'https://api.seniverse.com/v3/weather/now.json'
FORE_API = 'https://api.seniverse.com/v3/weather/daily.json'
KEY = 'glgqeom9bcm7swqq'
his_list = []
command_set = ('e', 'ex', 'exit', 'h', 'help', 'his', 'history')


# 从 Server 获取实时天气
def fetch_weather(location, api_type):
    result = requests.get(
        api_type,
        params={
            'key': KEY,
            'location': location,
            'language': 'zh-Hans',
            'unit': 'c'
        },
        timeout=60)
    return result.json()


# 解析实时天气
def decode_weather(target):
    print('\n------------------查询结果------------------')
    print("The city name is:\t", target['results'][0]['location']['name'])
    print("Today's weather is:\t", target['results'][0]['now']['text'])
    print("The temperature is:\t", target['results'][0]['now']['temperature'], '摄氏度')
    print("Weather updated at:\t", target['results'][0]['last_update'][:-6].replace(
        'T', ' '), '\n')
    return 0


# 解析天气预报（今天明天后天三天）
def decode_weather_forecast(target):
    w3d = target['results'][0]['daily']  # weather for 3 days

    update_time = target['results'][0]['last_update'][:-6].replace("T", ' ')
    city_name = target['results'][0]['location']['name']
    print('\n----------------------天气预报----------------------')
    print('The city name is:\t', city_name, '\n')
    for day in w3d:
        date = day['date']
        high_temp = day['high']
        low_temp = day['low']
        day_weather = day['text_day']
        night_weather = day['text_night']
        print('{d:12s}最高温度：{h:4s}最低温度：{l:4s}日间天气：{dw:3s}\t晚间天气：{nw}'.format(
            d=date, h=high_temp, l=low_temp, dw=day_weather, nw=night_weather))

    print("Weather updated at:\t", update_time, '\n')
    return 0


def history_append(weather, query_type_string):
    city = weather['results'][0]['location']['name']
    if [city, query_type_string] not in his_list:
        his_list.append([city, query_type_string])
    return 0


def welcome():
    print("\n程序使用指南：本程序用于查询天气"
          "\n直接输入 <城市名称>（中文或拼音皆可），可查询实时天气，如：\tbeijing"
          "\n输入 <城市名称 -f>（中文或拼音皆可），查询3天天气预报，如：\tbeijing -f"
          "\n输入 <help> 打印本说明"
          "\n输入 <history> 打印查询历史"
          "\n输入 <exit> 退出程序\n")
    return 0


def print_response(weather, city):
    if weather['status_code'] == 'AP010010':
        print("城市名称错误，请检查后重新输入\n")
    elif weather['status_code'] == 'AP010002':
        print("You are not allowed to access this API\n")
    elif weather['status_code'] == 'AP010006':
        print("免费用户不允许查询 %s 的天气" % city.upper(), '\n')

    return 0


def print_history(his):
    print('-----------历史查询记录-----------')
    for i in his:
        print("查询城市", i[0], '，查询类型：', i[1])
    print('\n')

    return 0


def print_result(weather, city_name, type_value):
    # type_value == 1 ---> 实时天气查询
    # type_value == 2 ---> 3天内天气预报
    if 'status_code' in weather:
        print_response(weather, city_name)
    elif type_value == 1:
        decode_weather(weather)
        history_append(weather, '实时天气查询')
        return 0
    elif type_value == 2:
        decode_weather_forecast(weather)
        history_append(weather, '三天内天气预报')
        return 0
    else:
        return None


def commands(cmd):
    if cmd in ['e', 'ex', 'exit']:
        exit(0)
    if cmd in ['h', 'help']:
        welcome()
    if cmd in ['history', 'his']:
        print_history(his_list)
    return 0


def main():

    welcome()

    while True:
        user_input = input("请输入城市名称（ 如 北京 or beijing）：").lower().split()
        # city name only:   user_input[0] --> city name
        # city -f:          user_input[0] --> city name, user_input[1] --> 'f'

        city = user_input[0]
        # user enter a command
        if city in command_set:
            commands(city)

        # user enter a single city name
        elif len(user_input) == 1 and city not in command_set:
            # 非指令 --> 城市名称
            w = fetch_weather(city, NOW_API)
            print_result(w, city, 1)

        # 输入 beijing -f
        elif len(user_input) == 2:
            para = user_input[1]

            if not para == '-f':
                print("Make sure you use the < -f > parameter after the city name!\n")

            # 使用了 -f 参数
            else:
                w = fetch_weather(city, FORE_API)
                print_result(w, city, 2)
        else:
            print("无法识别命令，请输入<city_name> 或 <city_name -f >\n")


if __name__ == '__main__':
    main()
