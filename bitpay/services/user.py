import redis
import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

# Verbindung zur Redis-Datenbank herstellen
redis_db = redis.Redis(host='localhost', port=6379, db=0)

class User:
    @staticmethod
    def register(username: str, password: str):
        # Überprüfen, ob der Benutzer bereits existiert
        if redis_db.get(username):
            raise HTTPException(status_code=409, detail="Benutzername bereits vergeben")

        # Passwort hashen
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Benutzer in der Redis-Datenbank speichern
        redis_db.set(username, hashed_password)

    @staticmethod
    def authenticate(credentials: HTTPBasicCredentials, secret_key: str):
        username = credentials.username
        password = credentials.password.encode()

        # Benutzerdaten aus der Redis-Datenbank abrufen
        hashed_password = redis_db.get(username)
        if not hashed_password or not bcrypt.checkpw(password, hashed_password):
            raise HTTPException(status_code=401, detail="Ungültige Anmeldedaten")

        # Authentifizierung erfolgreich, JWT-Token erstellen
        access_token = create_access_token(username, secret_key)
        return access_token

    @staticmethod
    def get_user(username: str):
        # Benutzer aus der Redis-Datenbank abrufen
        hashed_password = redis_db.get(username)
        if not hashed_password:
            raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
        return {"username": username}

    @staticmethod
    def create_access_token(username: str, secret_key: str, expires_in_minutes: int = 30):
        payload = {"sub": username}
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
