from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import vcloud
from vcloud_settings import settings

status_store = {}
progress_store = {}
 
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '0.0.1',
                     'last_build':  date.today().isoformat() }
        self.write(response)
 
class BoostHandler(tornado.web.RequestHandler):
    def get(self, id):
        if id in status_store:
            progress_val = progress_store[id]
            status_val = status_store[id]
            if status_val == "Complete":
                del progress_store[id]
                del status_store[id]
            response = { 'id': id,
                        'status': status_val,
                        'progress': progress_val }
        else:
            status_val="Starting"
            status_store[id]="Starting"
            progress_val="0"
            progress_store[id]="0"
            boost_thread = vcloud.boost("Boost Thread", id, settings, status_store, progress_store)
            boost_thread.start()
            response = { 'id': id,
                        'status': status_val,
                        'progress': progress_val }
        self.write(response)

class DeboostHandler(tornado.web.RequestHandler):
    def get(self, id):
        if id in status_store:
            progress_val = progress_store[id]
            status_val = status_store[id]
            if status_val == "Complete":
                del progress_store[id]
                del status_store[id]
            response = { 'id': id,
                        'status': status_val,
                        'progress': progress_val }
        else:
            status_val="Starting"
            status_store[id]="Starting"
            progress_val="0"
            progress_store[id]="0"
            boost_thread = vcloud.deboost("Deboost Thread", id, settings, status_store, progress_store)
            boost_thread.start()
            response = { 'id': id,
                        'status': status_val,
                        'progress': progress_val }
        self.write(response)

 
application = tornado.web.Application([
    (r"/boost/([a-z0-9-]+)", BoostHandler),
    (r"/deboost/([a-z0-9-]+)", DeboostHandler),
    (r"/version", VersionHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()