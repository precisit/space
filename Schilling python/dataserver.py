import tornado.ioloop
import tornado.web
import tornado.escape
import json
import urllib
import mainschilling

"""
Ett enkelt program dar man kan skriva in data i tva textboxar.
Datan i dessa tva skickas med en POST-request som hanteras i DataHandler.

Detta program kan anvandas som en grund till att mata in data till 
delta-v-programmet.

"""


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('dataform.html')  # Renderar formularet
        self.set_header("Content-Type", "application/json; utf-8")

class DataHandler(tornado.web.RequestHandler):
    def post(self):
        self.render('calc.html')    # Renderar en testsida 
        params = self.request.arguments # Parametrarna fran formularet
        res = mainschilling.deltaV(params)
        print res
        
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/calc", DataHandler),
])

application.listen(8020)
tornado.ioloop.IOLoop.instance().start()