## Python的文件操作
#### 使用open()读取文件内容
```
f = open('file-name', 'w')
```
创建一个名字是**"f"**的文件类对象

第一个参数是文件的路径

第二个参数是操作模式：r-read，w-write，a-append，"r+"读写

#### 推荐使用with关键字来处理文件对象，因为with会自动关闭文件
```
with open("workfile") as f:
	read_data = f.read()
```
#### 常见method
前提：`f`文件对象已经创建完毕

使用`f.read(size)`来读取文件的所有内容，size参数用来指定要读取多少内容，如果不指定size，默认读取全部的内容。

使用`f.readline()`来读取单行，如果返回空字符串，读取到了文件末尾

```
>>> f.readline()
'This is the first line of the file.\n'
>>> f.readline()
'Second line of the file\n'
>>> f.readline()
''
```
可以做一个循环，每一行分别执行`f.readline()`一次。

```
>>> for line in f:
		print(line, end='')
```
如果想把line的内容转换为List，可以直接使用`list(f)`或`f.readlines()`

#### 写文件
`f.write(string)`将内容写入文件，返回值是写入字符的总数

```
>>> f.write("This is a test\n")
15
```
其他类型的对象，需要先转换为str对象（使用`str()函数`）或者byte对象，然后进行写入

```
>>> value = ('the answer', 42)
>>> s = str(value)  			# convert the tuple to string
>>> f.write(s)
18
```

## 本程序的文件read操作
#### 1. readlines()
```
with open(file) as f:
	read_data = f.readlines()
	print(read_data)
输出为：
['北京,晴\n', '海淀,晴\n', ... ]
```
#### 2 for循环 + readline()
```
with open(file) as f:
	for line in f:
		read_data = f.readline()
		print(read_data)
输出为：
吐鲁番,阴

鄯善,晴间多云
```