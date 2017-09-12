# coding: utf-8

def generate_dict(file):
    weather_dict = {}

    with open(file) as f:
        for line in f:
            # 字符串分割，先用strip()干掉'\n'，再用split(',')，调整成 --> ['北京', '晴']格式
            data = line.strip().split(',')
            weather_dict[data[0]] = data[1]
    '''
    这里可以做一个判断，是否有重复的城市名称，选择更新后面的天气
        if data[0] in weather_dict:
            weather_dict.update(data[0] = data[1])

    我直接采用第一次出现城市的数据
    '''
    return weather_dict


def history_print(history_list):
    if len(history_list) == 0:
        print("暂无查询记录\n")
    else:
        print("您的查询记录为：")
        print("----城市--------天气----")

        for i in range(len(history_list)):
            print("%6s    %6s" % (history_list[i][0], history_list[i][1]))
        print('\n')
    return 0


def welcome():
    print('-------------------------------\n'
          "本程序用来查询各城市天气\n"
          "输入『help』查看帮助\n"
          "输入『history』查看查询历史纪录\n"
          "输入『exit』退出程序\n"
          '-------------------------------\n')
    return 0


def main():
    file = '../resource/weather_info.txt'
    history = []

    welcome()
    weather_dict = generate_dict(file)

    while True:
        user = input("请输入城市名称或指令：").strip()

        if user in weather_dict:
            # 历史纪录中删除重复项，以第一次查询为准
            # 否则还要动态调整 history[] 的顺序，太tmd麻烦了......
            if [user, weather_dict[user]] not in history:
                history.append([user, weather_dict[user]])
            print(user, " 的天气为：", weather_dict[user], '\n')

        elif user.lower() in ['help', 'h']:
            welcome()

        elif user.lower() in ['history', 'his']:
            history_print(history)

        elif user.lower() in ['exit', 'exi', 'ex', 'e']:
            history_print(history)
            break

        else:
            print("城市名称无法识别！！\n")
    return 0


if __name__ == "__main__":
    main()
