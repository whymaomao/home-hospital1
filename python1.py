import tornado.ioloop
import tornado.web
import os.path
import random
import tornado.httpserver
import tornado.options
import redis
import time
import struct
import json


import pymongo


from tornado.options import define, options
define("port",default = 8888, help = "run on the given port",type = int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r"/",MainHandler),(r"/hello",HelloHandler)]
		settings = dict(
		template_path=os.path.join(os.path.dirname(__file__),"templates"),																																																																																																																																																																																															
		static_path = os.path.join(os.path.dirname(__file__),"static"),
																																																																									debug = True,)	
		conn = pymongo.MongoClient("localhost",27017)
		self.db = conn["hospital"]
		tornado.web.Application.__init__(self,handlers,**settings)
	
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("myindex.html")
		
	def post(self):
		print(self.get_argument("name"))
		print(self.get_argument("password"))

class HelloHandler(tornado.web.RequestHandler):
	
	def get(self):
		self.render("hello.html")
		
	def post(self):
		list1 = []
		name = self.get_argument("name")
		password = self.get_argument("password")
		conn=self.application.db.info
		conn1 = self.application.db.data
		r = redis.Redis(host='localhost',port = 6379,db = 0)
		word_doc = conn.find_one({"name":name})
		user = conn1.find_one({"name":name})
		if word_doc:
			del word_doc["_id"]
			history = word_doc["history"]
			sex = word_doc["sex"]
			age = word_doc["age"]
			
			temperature = user["temp"]
			high_pressure = user["h_pressure"]
			low_pressure = user["l_pressure"]
			heart_rate = user["h_rate"]
			
			if conn1.find().count() > 7:
				
				print (conn1.find().count())
				for doc in conn1.find({"name":name}).sort([("time",-1)]).limit(7):
					list1.append(doc["temp"])
					print(list1)
			list1.reverse()

																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																														
		else:
			self.set_status(404)
		self.render("hello.html",name1 = name,sex1 = sex,age1 = age,history1 = history,password1 = password,tempe = temperature,h_pressure = high_pressure, l_pressure = low_pressure, h_rate = heart_rate,data1 = list1)
		

if __name__=="__main__":
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

