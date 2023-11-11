from . import config
from flask import Flask
from flask_bootstrap import Bootstrap5
from .views import views
from models.celular import views as v

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    Bootstrap5(app)

    app.register_blueprint(views)
   
    return app