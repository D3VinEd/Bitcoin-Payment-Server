from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from bitpay.services.wallet import Wallet

router = APIRouter()

class Transaction(BaseModel):
    recipient: str
    amount: float

class User(BaseModel):
    user_id: str

@router.post("/create_key")
def create_key(user: User):
    wallet = Wallet(user.user_id)
    wallet.create_key()
    return {"message": "Key created"}

@router.delete("/delete_key")
def delete_key(user: User):
    wallet = Wallet(user.user_id)
    wallet.delete_key()
    return {"message": "Key deleted"}

@router.get("/get_balance")
def get_balance(user: User):
    wallet = Wallet(user.user_id)
    balance = wallet.get_balance()
    return {"balance": balance}

@router.get("/get_transaction_history")
def get_transaction_history(user: User):
    wallet = Wallet(user.user_id)
    transactions = wallet.get_transaction_history()
    return {"transactions": transactions}

@router.post("/send_transaction")
def send_transaction(user: User, transaction: Transaction):
    wallet = Wallet(user.user_id)
    try:
        wallet.send_transaction(transaction.recipient, transaction.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Transaction sent"}

@router.get("/get_transaction_status")
def get_transaction_status(user: User, tx_hash: str):
    wallet = Wallet(user.user_id)
    tx_status = wallet.get_transaction_status(tx_hash)
    return {"transaction_status": tx_status}

@router.get("/get_transaction_fee")
def get_transaction_fee(user: User, tx_hash: str):
    wallet = Wallet(user.user_id)
    tx_fee = wallet.get_transaction_fee(tx_hash)
    return {"transaction_fee": tx_fee}
