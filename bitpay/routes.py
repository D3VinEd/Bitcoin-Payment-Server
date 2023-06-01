from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from bitpay.services.wallet import Wallet
from bitpay.services.config_manager import ConfigManager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError

router = APIRouter()
security = HTTPBearer()
config = ConfigManager()

class Transaction(BaseModel):
    recipient: str
    amount: float

class User(BaseModel):
    user_id: str

def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, config.read_config("JWT", "secret_key"), algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id:
            return User(user_id=user_id)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.post("/create_key")
def create_key(user: User = Depends(authenticate_user)):
    wallet = Wallet(user.user_id)
    wallet.create_key()
    return {"message": "Key created"}

@router.delete("/delete_key")
def delete_key(user: User = Depends(authenticate_user)):
    wallet = Wallet(user.user_id)
    wallet.delete_key()
    return {"message": "Key deleted"}

@router.get("/get_balance")
def get_balance(user: User = Depends(authenticate_user)):
    wallet = Wallet(user.user_id)
    balance = wallet.get_balance()
    return {"balance": balance}

@router.get("/get_transaction_history")
def get_transaction_history(user: User = Depends(authenticate_user)):
    wallet = Wallet(user.user_id)
    transactions = wallet.get_transaction_history()
    return {"transactions": transactions}

@router.post("/send_transaction")
def send_transaction(user: User = Depends(authenticate_user), transaction: Transaction):
    wallet = Wallet(user.user_id)
    try:
        wallet.send_transaction(transaction.recipient, transaction.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Transaction sent"}

@router.get("/get_transaction_status")
def get_transaction_status(user: User = Depends(authenticate_user), tx_hash: str):
    wallet = Wallet(user.user_id)
    tx_status = wallet.get_transaction_status(tx_hash)
    return {"transaction_status": tx_status}

@router.get("/get_transaction_fee")
def get_transaction_fee(user: User = Depends(authenticate_user), tx_hash: str):
    wallet = Wallet(user.user_id)
    tx_fee = wallet.get_transaction_fee(tx_hash)
    return {"transaction_fee": tx_fee}
