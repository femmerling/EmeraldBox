#! box/bin/python
"""
greeny.py

author: erich@emfeld.com
========================

This file acts as the gunicorn web server.
It simply puts the app into the worker to be served.
Configs for port number is available in config.py file.

"""
from app import app


# end of file