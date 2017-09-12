# coding: utf-8

file = '../resource/15.txt'
weather_dict = {}

'''
with open(file) as f:
    data = f.readlines()        # data --> List

# Output is:
# ['北京,晴\n', '海淀,晴\n', '朝阳,晴\n', '顺义,晴\n', '怀柔,晴\n',
# '通州,晴\n', '昌平,晴\n', '延庆,晴\n', '丰台,晴\n', '石景山,晴\n',
# '大兴,晴\n', '房山,晴\n', '密云,晴\n', '门头沟,晴\n', '平谷,晴']
    for i in data:
        i = i.strip().split(',')
        print(i)                # data --> 15 small lists

# ===============================================================
'''
# f = open(file, 'r')

with open(file) as f:
    for line in f:
    # 字符串分割，先用strip()干掉'\n'，再用split(',')，调整成 --> ['北京', '晴']格式
        data = line.strip().split(',')
        weather_dict[data[0]] = data[1]

print(weather_dict)

'''
# ===============================================================

with open(file) as f:
    data = f.read()         # data --> str
    print(type(data))              
    data = data.split()     # data --> 例1中的输出，是一个很长的List
    print(data)

    for i in data:
        info = i.split(',')   # 变成15个短list了
        weather_dict[info[0]] = info[1]

print(weather_dict)
'''