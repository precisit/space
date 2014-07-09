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
        response = mainschilling.deltaV(indata)
        response["Tmix"] = mainschilling.Tmix(indata)
        response["mp"] = mainschilling.mpSolver(indata)
        print(response)
        self.write(json.dumps(response))

# for further testing of the REST-APIs
class TestjsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/add", AddHandler),
    (r"/subtract", SubtractHandler),
    (r"/test", TestHandler),
    (r"/testjs",TestjsHandler)
], autoreload=True)

#TODO: https on prod
application.listen(8010)
tornado.ioloop.IOLoop.instance().start()
