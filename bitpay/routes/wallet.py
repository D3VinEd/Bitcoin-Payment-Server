from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from bitpay.services.wallet import Wallet
from bitpay.services.config_manager import ConfigManager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError


class Transaction(BaseModel):
    recipient: str
    amount: float


class User(BaseModel):
    user_id: str


router = APIRouter()
security = HTTPBearer()
config = ConfigManager()


def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Authenticate the user
    :param credentials:
    :return:
    """
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
def create_key(user: User = Depends(authenticate_user)) -> dict:
    """
    Create a new key for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    wallet.create_key()
    return {"message": "Key created"}


@router.delete("/delete_key")
def delete_key(user: User = Depends(authenticate_user)) -> dict:
    """
    Delete the key for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    wallet.delete_key()
    return {"message": "Key deleted"}


@router.get("/get_balance")
def get_balance(user: User = Depends(authenticate_user)) -> dict:
    """
    Get the balance for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    balance = wallet.get_balance()
    return {"balance": balance}


@router.get("/get_transaction_history")
def get_transaction_history(user: User = Depends(authenticate_user)) -> dict:
    """
    Get the transaction history for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    transactions = wallet.get_transaction_history()
    return {"transactions": transactions}


@router.post("/send_transaction")
def send_transaction(transaction: Transaction, user: User = Depends(authenticate_user)):
    """
    Send a transaction for the user
    :param transaction:
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    try:
        wallet.send_transaction(transaction.recipient, transaction.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Transaction sent"}


@router.get("/get_transaction_status")
def get_transaction_status(tx_hash: str, user: User = Depends(authenticate_user)):
    """
    Get the transaction status for the user
    :param tx_hash:
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    tx_status = wallet.get_transaction_status(tx_hash)
    return {"transaction_status": tx_status}


@router.get("/get_transaction_fee")
def get_transaction_fee(tx_hash: str, user: User = Depends(authenticate_user)):
    """
    Get the transaction fee for the user
    :param tx_hash:
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    tx_fee = wallet.get_transaction_fee(tx_hash)
    return {"transaction_fee": tx_fee}
