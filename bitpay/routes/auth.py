from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from bitpay.services.user import User
auth = AuthJWT()

# Konfiguration von FastAPI
app = FastAPI()

# Registrierung eines neuen Benutzers
@app.post("/register")
def register_user(username: str, password: str):
    User.register(username, password)
    return {"message": "Benutzer erfolgreich registriert"}

# Authentifizierung und Ausstellung eines JWT-Tokens
@app.post("/login")
def login(credentials: HTTPBasicCredentials):
    User.authenticate(credentials)
    access_token = create_access_token(credentials.username)
    return {"access_token": access_token}

# Geschützte Route