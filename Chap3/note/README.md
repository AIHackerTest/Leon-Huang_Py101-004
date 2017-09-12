# CH3 作业
## Flask 的安装
```shell
pip install flash
装完后

$ export FLASK_APP=hello.py
$ flash run
 * Serving Flask app hello
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
在打开 `http://127.0.0.1:5000` 时，可以看到测试 app 的效果，如显示 hello world 啥的

## 思路分析
1. 首先做一个index页面，这个页面上有一个输入框，几个不同作用的按钮
2. 用户在文本框里输入城市，页面通过调用天气查询的 api 进行查询，如果能正常解析，返回天气，否则，返货「城市名称输入错误」之类的错误提示
3. 历史
4. 帮助

## 步骤分析

### 1. 如何显示一个页面（index.htm）？
如何让 flask 在用户输入网址是就直接显示我们的 index.htm？

使用`render_template()`函数来显示某个页面，页面要求放在一个 templates 文件夹下，so，把 index.htm 放到这个文件夹下面去，先把程序如下修改并测试

```python
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def query():
    return render_template('index.htm')
```

再打开 `http://127.0.0.1:5000` 时，可以正常显示我们的页面了

### 2. 如何将页面文字框的内容传递给 flask？
#### GET or POST
在 flask 文档里专门提到了这一部分
> **GET**
>
>浏览器获取存储在 Server 的页面，打开网页时用 GET 
>
> **POST**
> 
>浏览器告诉 Server 他要向某 URL 发送一些信息，server 需要存储这些信息，但只需要储存一次。HTML的forms标签通常用于向服务器发送信息。发微博，论坛盖楼时用的都是 POST 方法

> **PUT**

>和 POST 类似，但使用 PUT 时，可能需要多次写操作，甚至将内容写入数据库中。下一张如果要写 SQL 数据库的话，应该就要用到 PUT 方法了

<font color="red">**这 tmd 和我有关系么？？**</font>

首先，毫无疑问，肯定要用 flask.request，继续查文档，发现有一段话
> **form**
> 
> A MultiDict with the parsed form data from POST or PUT requests.
> 
> **args**
> 
> A MultiDict with the parsed contents of the query string. (The part in the URL after the question mark). 

#### 先试一把

貌似在 request.form 可以获取过来的数据，但仅仅局限于 POST 和 PUT 请求，并且只能获取 HTML form 里面的内容，因此做一个最简单的 HTML 页面，使用 POST，和 form 两种属性

```html
<header>
</header>
<body>
  <form action="" method="post">
      城市：<input type="text" name="city">
      <input name="query" type="submit" value="查询">
      <input name="history" type="submit" value="历史">
      <input name="help" type="submit" value="帮助">
  </form>
</body>


```

**重点：**`method="post"`以及所有内容包含在`<form> </form>`中

另外，把python程序修改一下

```python
# coding: utf-8

from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    city = None
    if request.method == 'POST':
        if request.form['action'] == u'查询':
            city = request.form["city"]
    return render_template('index.htm', city=city)
```


再试试看，能不能把 city 显示在页面上。

<font color="red"> **运行后，tmd 居然页面没反应** </font>

<font color="red"> **然而，并没有什么卵用** </font>

<font color="red"> **挠头三连** </font>

#### 到底是 TMD 啥问题呢？？？

问题在于，虽然我想把 city 传给 index.htm，但 index 页面的代码中，并没有任何来表达如何显示 city 的声明，继续修改 index.htm。如何让页面显示 city 捏？

Flask 采用 Jinja2 作为 render_template() 的引擎，所以接下来去爬 Jinja2 的文档。

Jinja2里面显示变量的方法很直接，` {{Variable_name}} `就 OK，外面的那对花括号表示 print，里面的那对花括号表示变量，类似于 string.format()方法

> 对上面的 python 代码的最后一行解释一下，有个`city=city`的语句，右边的 city 是在函数中定义的变量，左边的 city 是需要送到页面进行渲染的变量，左边的city变量需要在 index.html 中使用`{{city}}`的方式定义后，才会显示在页面上。

```
在index.htm 中
</form>下面新加一行显示 city 这个变量的声明就 OK 了

{{city}}
```
再跑一遍程序，现在OK了，可以正常显示输入的城市名。证明系统实际上是已经获取到了 city 这个变量，然后让程序进行查询就可以了:-)后续可以创建 N 个变量，都用这种方法 print 出来。

### 3. flask 收到内容后，如何构造 API 进行天气查询？
可以把查询天气的函数直接以`def query_weather(city_name)` 的形式放在脚本中，也可以通过 import 的方式调用，返回的值分别付给路由中函数的变量即可。

获取天气信息中，在最后的`render_template`中把函数返回的变量赋值给 flask 中的变量

```python
weather = None

1. city = get city name by flask
2. weather = query_weather(city) by function

return render_template('index.htm', weather=weather)
# 右边的 weather：调用查询天气函数的返回值
# 左边的 weather：在 Flask 中定义的变量，需要在 HTML 中显示的
```

### 3. 天气查询完毕后，如何将内容显示在页面上？
在 html 页面中进行变量的申明

```html
<body>

<!-- 显示 history[] 变量-->
<!-- Flask 可以使用 if、for 循环等语句-->
	{{ if history }}		<!-- 如果 history 存在的话，进行打印-->
		{{ for h in history }}
			h[0]<br>
			h[1]<br>
			h[2]<br>
		{{ endfor }}
	{{ endif }}

</body>
```

可以在一个简单的页面下声明 N 个变量，会自动打印在 HTML 页面上
