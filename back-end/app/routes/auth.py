from flask import Blueprint, request
from app.controllers.auth import AuthController


bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    return AuthController.login(data)