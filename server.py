import tornado.ioloop
import tornado.web
import tornado.log
import logging
import json
import imp
import sys
sys.path.append('C:/Github/space/Schilling python/')
sys.path.append('C:/Github/space/propellant/')
sys.path.append('C:/Github/space/simulation2/RESTAPIs/')
import mainschilling
import propellantfunc
import mainrocketsim


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
            response["position"], response['velocity'], response['time'], response['deltaV'], response['draglosses'],response['gravitylosses'], response['thrust'],response['drag'],response['downrange'] = mainrocketsim.RocketSimulator(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class OMRloxkerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxker"
            response["OMR"] = propellantfunc.OMR(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class AFTloxkerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxker"
            response["AFT"] = propellantfunc.AFT(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class GMWloxkerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxker"
            response["GMW"] = propellantfunc.GMW(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class SHRloxkerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxker"
            response["SHR"] = propellantfunc.SHR(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class OMRloxmethHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxmeth"
            response["OMR"] = propellantfunc.OMR(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class AFTloxmethHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxmeth"
            response["AFT"] = propellantfunc.AFT(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class GMWloxmethHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxmeth"
            response["GMW"] = propellantfunc.GMW(indata)
        except KeyError, e:
            raise tornado.web.HTTPError(400,'Not enough input data -- missing: "%s"' % str(e))
        self.write(json.dumps(response))

class SHRloxmethHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*") #allow requests from other domains than self

    def post(self):
        indata = json.loads(self.request.body)
        response = {}
        try:
            indata["fuel"] = "loxmeth"
            response["SHR"] = propellantfunc.SHR(indata)
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
    (r"/rocketSim", RocketSimHandler),
    (r"/OMR/loxker", OMRloxkerHandler),
    (r"/AFT/loxker", AFTloxkerHandler),
    (r"/GMW/loxker", GMWloxkerHandler),
    (r"/SHR/loxker", SHRloxkerHandler),
    (r"/OMR/loxmeth", OMRloxmethHandler),
    (r"/AFT/loxmeth", AFTloxmethHandler),
    (r"/GMW/loxmeth", GMWloxmethHandler),
    (r"/SHR/loxmeth", SHRloxmethHandler)
    

], autoreload=True)

#TODO: https on prod
application.listen(8000)
tornado.ioloop.IOLoop.instance().start()
