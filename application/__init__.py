"""
Creates the app
@author: abhin
"""

from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.main_bp)

        return app