#! box/bin/python
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from app import app

# change the next value for the port being used on your deployment
server_port = 5000

print "EmeraldBox is now running powered by Tornado Web Server on port " + str(server_port) + " ..."

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(server_port)
autoreload.start()
IOLoop.instance().start()