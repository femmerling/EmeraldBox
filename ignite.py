#! box/bin/python
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

import tornado.autoreload

#app.run(debug=True)
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(2901)
tornado.autoreload.start()
IOLoop.instance().start()