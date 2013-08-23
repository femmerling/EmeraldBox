#! box/bin/python
"""
ignite.py

author: erich@emfeld.com
========================

This file acts as the tornado web server.
It simply wraps the app into a WSGI container of tornado web server.

Configs for port number is available in config.py file.

"""
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from app import app
from config import SERVER_PORT

print "EmeraldBox is now running powered by Tornado Web Server on port " + str(SERVER_PORT) + " ..."

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(SERVER_PORT)
autoreload.start()
IOLoop.instance().start()


# end of file