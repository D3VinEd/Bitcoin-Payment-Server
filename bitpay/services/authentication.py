from functools import wraps
from flask import request, jsonify

# Beispielbenutzerdaten
USERNAME = 'admin'
PASSWORD = 'geheim'

class Auth:
    @staticmethod
    def check_auth(username, password):
        """Überprüft die Authentifizierung."""
        return username == USERNAME and password == PASSWORD

    @staticmethod
    def authenticate():
        """Sendet eine Authentifizierungsaufforderung."""
        return jsonify({'message': 'Authentifizierung erforderlich.'}), 401

    @classmethod
    def auth_required(cls, route_func):
        """Decorator zur Überprüfung der Authentifizierung."""
        @wraps(route_func)
        def decorated_route(*args, **kwargs):
            auth = request.authorization
            if not auth or not cls.check_auth(auth.username, auth.password):
                return cls.authenticate()
            return route_func(*args, **kwargs)
        return decorated_route
