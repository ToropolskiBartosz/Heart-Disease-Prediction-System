from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__)
    
    from . import views
    app.register_blueprint(views.view)

    return app