#!/usr/bin/env python
#-*- coding:utf8 -*-

from collections import Iterable,Iterator
import requests

class WeatherIterator(Iterator):#创建迭代器对象
	def __init__(self,cities): 
		self.cities = cities #传入城市
		self.index = 0 #迭代初始值为0
		
	def getweather(self,city): #获取天气数据
		r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city=' + city) #API，传入城市
		data = r.json()['data']['forecast'][0] #解析从APT获取的值
		return '%s: %s, %s ' %(city,data['low'],data['high']) #返回天气值
	
	def next(self): #相当于迭代器的next方法
		if self.index == len(self.cities): #如果迭代完成就抛出异常
			raise StopIteration
		city = self.cities[self.index] #获得一个未迭代过的值
		self.index += 1 #迭代一次加1，并表示对应值已经迭代过了
		return self.getweather(city) #返回一个迭代过的值
	
class WeatherIterable(Iterable): #创建可迭代对象
	def __init__(self,cities):
		self.cities = cities #获取城市列表
	def __iter__(self):
		return WeatherIterator(self.cities) #将城市列表传入迭代器中迭代进行迭代，并返回城市所对应的天气值

if __name__ == '__main__':
	for x WeatherIterable([u'北京',u'上海',u'呼和浩特']): #传入城市列表，且接受天气值的可迭代对象
		print (x) #每获取一个值，就打印一个，不会获取完全部值之后才打印出来
		
	