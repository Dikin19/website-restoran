from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Config upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB

    # Import routes
    from app.routes.menu import bp as menu_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.order import bp as order_bp
    
    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)

    @app.route("/")
    def home():
        return {"message": "API jalan"}

    return app
