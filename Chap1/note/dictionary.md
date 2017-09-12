~ 用于存放个人教程，建议使用 Jupyter Notebook 编写。

## 解题思路
#### 1. 读取txt文件的内容，将内容以字典的形式保存


## Dict相关知识
#### 为什么要使用dict？ 

Dict可以更高效进行数据的查询，和list相比，效率更高

#### Dict和List的比较

- List通过index来访问，如List[i]，Dict通过KVP(Key Value Pair)来访问。要访问List中的某个元素，必须知道它的index，否则就只能遍历；而要访问Dict中的元素，只需要通过dict(key)即可，不需要遍历整个Dict。
- List的值随时可以修改，如list[i]=0，Dict的KVP不能修改，只能删掉再重加

#### Dict的创建
```
>>> tel = {'jack': 4098, 'sape': 4139}
```

或者这样创建：

```
>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'jack': 4098, 'guido': 4127}
```
or

```
>>> dict(sape=4139, guido=4127, jack=4098)
{'sape': 4139, 'jack': 4098, 'guido': 4127}
```

#### Dict的常见操作
```
len(dict)		# 字典的长度
dict[key]		# 字典中某个key对应的value
d[key] = value	# 设置key的值
del d[key]		# 删除某个KVP
key in d		# True or False
key not in d	# True or False
iter(d)			# 返回dict的地址
```

#### Dict的常见Method
```
clear()				# 清除字典中所有的元素, a.clear()
copy()				# 复制一个字典, b = a.copy()
get(key[, default])	# 返回key的值, a.get('key')
items()				# 遍历字典中所有的KVP
keys()				# 遍历字典中所有的key
values()			# 遍历字典中所有的value

pop(key[, default]) # 如果key在字典中，移除它，并返回该key的值。
					# 如果key不在字典中，返回default的值
popitem()			# 随机删除Dict中一个KVP
setdefault(key[, default])
					# 如果key存在，返回其值；如果不存在，将key=default插入dict 
update([other]) 	# 将KVP插入现有的dict中，会覆盖现有key的值
					# d.update(red=1, blue=2).

```


