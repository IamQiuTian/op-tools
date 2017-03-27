#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import select
import time

class PoolTimeServer(object):
    std_mask = select.POLLERR | select.POLLHUP | select.POLLNVAL  #关心的错误事件
	
    def __init__(self,sock):
        self.master_sock = sock #获取socket
        self.all_socks = {self.master_sock.fileno():self.master_sock} #存储所有的socket，KEY是文件描述符，value是对应的套接字
        self.buffers = {} #key是文件描述符，value是客户端发来的数据
        self.p = select.poll() #获取poll对象,作用是注册其关心的事件
        self.watch_read(self.master_sock.fileno()) #获取所有的文件描述符
    
    def watch_read(self,fd):
        self.p.register(fd,select.POLLIN | self.std_mask) #向poll注册文件描述符，其关心的事件是读取
		
    def watch_write(self,fd):
         self.p.register(fd,select.POLLOUT| self.std_mask) #向poll注册文件描述符，其关心的事件是写入
    
    def watch_both(self,fd):
         self.p.register(fd,select.POLLOUT | select.POLLIN | self.std_mask) #向poll注册文件描述符，其关心的事件是读取和写入
    
    def fd2socket(self,fd):
        return self.all_socks[fd] #返回文件描述符对应的套接字
		
    def new_conn(self,c_sock):
        fd = c_sock.fileno() #获取客户端套接字的文件描述符
        self.all_socks[c_sock.fileno()] = c_sock #KEY是文件描述符，value是对应的客户端套接字
        self.buffers[fd] = "Welcome!\n" #保存要给每个客户端发送的数据
        self.watch_both(fd) #使用 watch_both函数向poll注册客户端套接字
		
    def close_out(self,fd):
        self.fd2socket(fd).close() #关闭套接字
        self.p.unregister(fd) #注销文件描述符，不在关系任何事件
        del self.buffers[fd] #清除此客户端需要发送的数据
        del self.all_socks[fd] #清除此客户端的套接字
		
    def read_event(self,fd):
        data = self.fd2socket(fd).recv(1024)
        if not data: #如果数据为空就执行close_out方法
            self.close_out(fd)
        else:
            self.buffers[fd] += data #接收客户端发送的数据至字典中
            self.watch_both(fd) #关心读取和写入事件
			
    def write_event(self,fd):
        if not self.buffers[fd]: #如果文件描述符不存在的话
            self.watch_read(fd) #关心读事件
            return
        byte_send = self.fd2socket(fd).send('[%s] %s' % (time.ctime(),self.buffers[fd])) #向客户端发送数据,并获取发送的字节数
        self.buffers[fd] = self.buffers[fd][byte_send:] #取后面未发送的数据
        if not self.buffers[fd]: #如果发送的数据已空
            self.watch_read(fd) #就继续关系读事件
			
    def error_event(self,fd):
        self.close_out(fd)
		
    def mainloop(self):
        while True:
            result = self.p.poll() #当文件描述符发生其关心的事件，就向下执行，否则向下执行，也就是不进入循环
            for fd,event in result: #fd是文件描述符，event是事件
                if fd == self.master_sock.fileno(): #如果文件描述符是服务端socket的文件描述符，代表有新客户端连接
                    cli_sock,cli_addr = self.fd2socket(fd).accept() #就接收客户端连接
                    cli_sock.setblocking(False) #将客户端套接字设为非阻塞状态
                    self.new_conn(cli_sock) #给new_conn函数返回客户端套接字
                elif event & select.POLLIN: #如果是读事件
                    self.read_event(fd)
                elif event & select.POLLOUT: #如果是写事件
                    self.write_event(fd)
                else: #既不是读也不是写，那就是错误事件
                    self.error_event(fd)
					
if __name__ == '__main__':
#绑定服务端套接字
    host = ''
    port = 12345
    addr = (host,port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(addr)
    s.listen(1)
    s.setblocking(False) #设置服务端套接字为非阻塞状态
    pts = PoolTimeServer(s)
    pts.mainloop()