import tornado.ioloop
import tornado.web
import tornado.log
import logging
import json
import mainrocketsim
import imp
import sys
sys.path.append('C:/Github/space/Schilling python/')
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

class AtmoPressureHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["pressure"], response['altitude'] = mainrocketsim.pressure(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class AtmoDensityHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["density"], response['altitude'] = mainrocketsim.density(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class AtmoTempHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["temperature"], response['altitude'] = mainrocketsim.temp(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))
class RocketSimHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            response["position"], response['velocity'], response['time'], response['deltaV'], response['draglosses'],response['gravitylosses'], response['thrust'],response['drag'],response['pitchangle'] = mainrocketsim.RocketSimulator(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/testjs",TestjsHandler),
    (r"/deltaV",DeltaVHandler),
    (r"/Tmix",TmixHandler),
    (r"/rocketCapability",RocketCapabilityHandler),
    (r"/atmoPressure",AtmoPressureHandler),
    (r"/atmoDensity",AtmoDensityHandler),
    (r"/atmoTemp",AtmoTempHandler),
    (r"/rocketSim", RocketSimHandler)

], autoreload=True)

#TODO: https on prod
application.listen(8000)
tornado.ioloop.IOLoop.instance().start()
