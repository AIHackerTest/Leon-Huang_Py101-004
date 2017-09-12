# 01 What is API
从题目说起，CH02的要求是通过向远程服务器发送一条查询请求（request），从而获得当前实时的天气情况

1. PC -----------> request(city, time, date, etc.) -----------> server
2. PC <----------- response(weather, ℃, PM2.5, etc) <---------- server

可以理解为：

- Server 为 PC 的查询预留了一个接口（interface）
- 这个接口对 PC 发过来的 request 消息，有一定的格式要求
- 同时，Server 返回的 response 中，也以特定的格式进行封装
- PC 在收到 response 后，需要对消息进行解析，从而获取具体的信息

那么，这种接口就叫做应用程序接口，Application Programming Interface，**API**。

可以看看 youtube 那个视频

卡片后面推荐了3个天气 API，这三个推荐的 API，我感觉都很差劲，**咬着牙**选了第一个

- 心知天气： 文档对新手不友好，写的很挫，在 Github 里有 DEMO，你 tmd demo 里好歹加一两句注释会死啊
- Weather API：无法注册，一直失败，但他家的文档非常清晰明了，零基础也能看懂，看看人家的文档：

> **API call:**
> 
> api.openweathermap.org/data/2.5/weather?q={city name}
>
> api.openweathermap.org/data/2.5/weather?q={city name},{country code}
> 
> **Parameters:**
> 
> q city name and country code divided by comma, use ISO 3166 country codes
> 
> **Examples of API calls:**
> 
> api.openweathermap.org/data/2.5/weather?q=London
>
> api.openweathermap.org/data/2.5/weather?q=London,uk

- 彩云天气 API：基本上废了，查不了


# 02 选好 API 之后要干嘛？
选好 API 之后，有以下2件事情要完成：

- 如何让 python 程序构造一条 Req 消息
- 如何解析 Server 发回来的 Rsp 消息

# 03 构造 MVP
## 3.1如何让 Python 构造 Req 消息
[ API的官方文档 ](https://www.seniverse.com/doc)

[Github 托管 DEMO ](https://github.com/seniverse/seniverse-api-demos/tree/master/python)

## 3.2 使用 requests 模块发送请求
### What is requests
requests 是 python 提供的一个标准库，通过它，python 可以向服务器发送 HTTP 请求
### 如何使用 requests
先安装，`pip install requests`或者在 Anaconda 中图形界面安装

再 import 就可以了

```python
import requests
```

## 3.3 如何构造 Req

厂商的 SB DEMO文档里有一段，直接抄过来，然后在想办法弄懂各个字段的意思吧，你 tmd 好歹写点注释啊

```python
import requests

def fetchWeather(location):
    result = requests.get(API, params={
        'key': KEY,
        'location': location,
        'language': LANGUAGE,
        'unit': UNIT
    }, timeout=1)
    return result.text
    
# API: API 的地址， 貌似有两个地址，一个是实时的，一个是天气预报 
#      https://api.seniverse.com/v3/weather/daily.json，某天的天气
#      https://api.seniverse.com/v3/weather/now.json，实时天气
#      这两个 SB 地址不要问我怎么知道的
# key: 注册后，会有一个 API 密钥
# location: 应该就是位置了，中文/拼音
# language: 中文直接填 zh-Hans
# unit: c or f，表示华氏度 or 摄氏度
# timeout: 不知道干嘛用的，页面无介绍
```

我先测试一把

```python
import requests

def fetchWeather(location):
    result = requests.get('https://api.seniverse.com/v3/weather/now.json', params={
        'key': ‘glgqeom9bcm7swqq’,
        'location': location,
        'language': ‘zh-Hans’,
        'unit': ’c’
    }, timeout=60)
    return result.text

print(fetchWeather(’beijing’))
```
返回结果为一坨一坨的东西

```python
{"results":[{"location":{"id":"WX4FBXXFKE4F","name":"北京","country":"CN","path":"北京,北京,中国","timezone":"Asia/Shanghai","timezone_offset":"+08:00"},"now":{"text":"多云","code":"4","temperature":"28"},"last_update":"2017-08-21T23:45:00+08:00"}]}

```

# 4 JSON 消息的解析

## 4.1 什么是 JSON

JSON 是一种数据格式，它的结构基于 Python 中的 dict 和 list

[JSON 介绍文档](http://www.json.org/json-zh.html)

[Python 如何解析 JSON](https://docs.python.org/3/library/json.html) 

[Request 中如何处理 JSON](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content)

```python
{"results": [ { "location": { "id":"WX4FBXXFKE4F",
                              "name":"北京",
                              "country":"CN",
                              "path":"北京,北京,中国",
                              "timezone":"Asia/Shanghai",
                              "timezone_offset":"+08:00"
                            },
                 "now":     { "text":"多云",
                              "code":"4",
                              "temperature":"28"
                            },
                 "last_update":"2017-08-21T23:45:00+08:00"
                }
             ]
}

```
既然返回的是 JSON，那么上面代码中，函数的返回值就不要 text 了，直接让函数返回 JSON 好了

```python
		# return result.text
		return result.json()
```

## 4.2 JSON的解析

可以发现，返回的结果是一个 dict，key=results, value=[.........]

```python
print(type(w['results']), len(w['results']))
>>> <class 'list'> 1
```
List 的长度是1，不太好处理，不过既然它是 List，而里面又是一个不折不扣的字典，那就直接去里面的元素好了

```python
print(type(w['results'][0]), len(w['results'][0]))
>>> <class 'dict'> 3

print(w['results'][0])
>>> {'now': {'text': '雷阵雨', 'temperature': '28', 'code': '11'}, 'location': {'timezone': 'Asia/Shanghai', 'name': '北京', 'id': 'WX4FBXXFKE4F', 'path': '北京,北京,中国', 'country': 'CN', 'timezone_offset': '+08:00'}, 'last_update': '2017-08-22T16:40:00+08:00'}
```
哈哈哈，tmd，字典来了吧

```python
print(w['results'][0]['now'])
>>> {'text': '雷阵雨', 'temperature': '28', 'code': '11'}

for k, v in w['results'][0]['now'].items():
    print(k, v)
>>> text 雷阵雨
>>> temperature 28
>>> code 11

print(w['results'][0]['location'])
>>> {'timezone': 'Asia/Shanghai', 'name': '北京', 'id': 'WX4FBXXFKE4F', 'path': '北京,北京,中国', 'country': 'CN', 'timezone_offset': '+08:00'}

for k, v in w['results'][0]['location'].items():
    print(k, v)
>>> timezone Asia/Shanghai
>>> name 北京
>>> id WX4FBXXFKE4F
>>> path 北京,北京,中国
>>> country CN
>>> timezone_offset +08:00

print(w['results'][0]['last_update'])
>>> 2017-08-22T16:40:00+08:00
```
***

# 测试MVP

***

```python
# coding: utf-8

import requests
import json

def fetchWeather(location):
    result = requests.get('https://api.seniverse.com/v3/weather/now.json', params={
        'key': 'glgqeom9bcm7swqq',
        'location': location,
        'language': 'zh-Hans',
        'unit': 'c'
    }, timeout=60)
    return result.json()

user_location = 'beijing'
w = fetchWeather(user_location)
print('\n------------------查询结果------------------')
print("The city name is:\t",   w['results'][0]['location']['name'])
print("Today's weather is:\t", w['results'][0]['now']['text'])
print("The temperature is:\t", w['results'][0]['now']['temperature'], '摄氏度')
print("Weather updated at:\t", w['results'][0]['last_update'][:-6].replace('T', ' '))
```
执行结果

```bash
$ python weather-api.py
------------------查询结果------------------
The city name is:	 北京
Today's weather is:	 雷阵雨
The temperature is:	 27 摄氏度
Weather updated at:	 2017-08-22 17:50:00

```
