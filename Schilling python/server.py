import tornado.ioloop
import tornado.web
import tornado.log
import logging
import json
import mainschilling

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

#For testing of delta-V calculations
class TestHandler(tornado.web.RequestHandler):
    def post(self):
        indata = self.request.body
<<<<<<< HEAD
        response = mainschilling.deltaV(indata)
=======
        response = {}
        response["Tmix"] = mainschilling.Tmix(indata)
>>>>>>> 2e2d24ccea6204ff81b255474e6ba87d5461414e
        print(response)
        self.write(json.dumps(response))

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/add", AddHandler),
    (r"/subtract", SubtractHandler),
    (r"/test", TestHandler)
], autoreload=True)

#TODO: https on prod
<<<<<<< HEAD
application.listen(8010)
=======
application.listen(8020)
>>>>>>> 2e2d24ccea6204ff81b255474e6ba87d5461414e
tornado.ioloop.IOLoop.instance().start()