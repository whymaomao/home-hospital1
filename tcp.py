import threading
import socket
import time
import string
import redis
import time
import pymongo

ISOTIMEFORMAT = '%Y-%m-%d %X'
r = redis.Redis(host='localhost',port = 6379,db = 0)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
conn = pymongo.MongoClient("localhost",27017)
db = conn.hospital
data = db.data
s.bind(('0.0.0.0',8087))
s.listen(5)
print('Waiting for connection...')

def tcplink(sock,addr):
	print('Accept new connection from %s:%s...' % addr)
	sock.send(b'Welcome!')
	while True:
		data = sock.recv(1024)
		timenow = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
		
		if not data or data.decode('utf-8') == 'exit':
			break;
		temp1 = ord(data[0:1].decode('utf-8'))
		temp2 = ord(data[1:2].decode('utf-8'))
		high_pressure = ord(data[2:3].decode('utf-8'))
		low_pressure = ord(data[3:4].decode('utf-8'))
		heart_rate = ord(data[4:5].decode('utf-8'))
		print(temp1)
		print(temp2)
		print(high_pressure)
		print(low_pressure)
		print(heart_rate)
		
		temp = temp1+temp2/100 
		r.hset("data","temp",temp)
		r.hset("data","h_pressure",high_pressure)
		r.hset("data","l_pressure",low_pressure)
		r.hset("data","heart_rate",heart_rate)

		
		temperature = float(bytes(r.hget("data" ,"temp")).decode("ascii"))
		high_pressure = int(bytes(r.hget("data","h_pressure")).decode("ascii"))
		low_pressure = int((r.hget("data","l_pressure")).decode("ascii"))
		heart_rate = int((r.hget("data","heart_rate")).decode("ascii"))
		data.insert({"name":name,"temp":temperature,"h_pressure":high_pressure,"l_pressure":low_pressure,"h_rate":heart_rate,"time":(int)(time.time())})
		print (temp)
	
		time.sleep(1)
		
	sock.close()
	print('Connection closed')

while True:
	sock,addr = s.accept()
	t = threading.Thread(target = tcplink, args=(sock,addr))
	t.start()

