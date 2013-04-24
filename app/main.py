from app import app

from controllers import base_view

app.register_blueprint(base_view)