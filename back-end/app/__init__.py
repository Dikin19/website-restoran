from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.menu import menu_bp
    from app.routes.auth_routes import bp as auth_bp
    
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return {"message": "API jalan"}

    return app
