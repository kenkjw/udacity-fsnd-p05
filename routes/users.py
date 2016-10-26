from flask import Blueprint

users_bp = Blueprint('users', __name__)


@users_bp.route('/login')
def login():
    """Log the user out."""
    return 'login'


@users_bp.route('/token')
def token():
    return 'token'


@users_bp.route('/logout')
def logout():
    """Log the user out."""
    return 'logout'