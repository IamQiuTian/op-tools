#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Test(object):
    def start(self):
        print(self.starting) #打印__enter__返回的值

    def __enter__(self): #执行类的初始化，并把值返回对应的函数方法
        self.starting = "start ing"
        return self
    def __exit__(self,exc_type,exc_val,exc_tb): #定义类结束需要做的动作,并捕获异常
        print("stop ing") #在类的全部代码执行完后执行这段代码 
        #return True #无论是否出现异常，都将执行__exit__中的代码  

with Test() as t:
    t.start() #定义这个类中最开始执行的函数方法
