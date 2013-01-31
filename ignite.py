#! box/bin/python
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from app import app
from config import SERVER_PORT

print "EmeraldBox is now running powered by Tornado Web Server on port " + str(SERVER_PORT) + " ..."

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(server_port)
autoreload.start()
IOLoop.instance().start()