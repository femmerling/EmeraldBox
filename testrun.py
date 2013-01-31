#!box/bin/python
from app import app
from config import SERVER_PORT

app.run(debug = True,port=SERVER_PORT)