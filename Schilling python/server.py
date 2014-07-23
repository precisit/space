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


class TestjsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')

class DeltaVHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        
        #indata.firstStage.wetMass #From meeting
        response = {}
        try:
            response['dVtot'], response['Approximations'] = mainschilling.deltaV(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class TmixHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["Tmix"], response['Approximations'] = mainschilling.Tmix(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class RocketCapabilityHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["mp"], response['Approximations'] = mainschilling.mpSolver(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/testjs",TestjsHandler),
    (r"/deltaV",DeltaVHandler),
    (r"/Tmix",TmixHandler),
    (r"/rocketCapability",RocketCapabilityHandler)

], autoreload=True)

#TODO: https on prod
application.listen(8020)
tornado.ioloop.IOLoop.instance().start()
