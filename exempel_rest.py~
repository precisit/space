import tornado.ioloop
import tornado.web
import tornado.log
import logging
import json

log = logging.getLogger("tornado.general")
tornado.log.enable_pretty_logging();

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('pong')

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        indata = json.loads(self.request.body) #Load JSON that was POSTED
        response = {}
        response["summa"] = indata["tal1"] + indata["tal2"] #Berakna summan
        self.write(json.dumps(response))

class SubtractHandler(tornado.web.RequestHandler):
    def post(self):
        indata = json.loads(self.request.body) #Load JSON that was POSTED
        response = {}
        response["summa"] = indata["tal1"] - indata["tal2"] #Berakna summan
        self.write(json.dumps(response))

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/add", AddHandler),
    (r"/subtract", SubtractHandler)
], autoreload=True)

#TODO: https on prod
application.listen(8040)
tornado.ioloop.IOLoop.instance().start()
