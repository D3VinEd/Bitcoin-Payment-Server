from fastapi import HTTPException, APIRouter, Depends
from bitpay.services.wallet import Wallet
from fastapi.security import OAuth2PasswordBearer
from bitpay.services.authentication import Auth
from bitpay.models import Transaction, User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/create_key")
def create_key(user: User = Depends(Auth.auth_required)) -> dict:
    """
    Create a new key for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    keys = wallet.create_keys()
    print("router create_key")
    print(keys)
    wallet.store_keys(keys)
    return {"hex_keys": [key.to_hex() for key in keys]}


@router.delete("/delete_key")
def delete_key(user: User = Depends(Auth.auth_required)) -> dict:
    """
    Delete the key for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    wallet.delete_key()
    return {"message": "Key deleted"}


@router.get("/get_balance")
def get_balance(user: User = Depends(Auth.auth_required)) -> dict:
    """
    Get the balance for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    balance = wallet.get_balance()
    return {"balance": balance}


@router.get("/get_transaction_history")
def get_transaction_history(user: User = Depends(Auth.auth_required)) -> dict:
    """
    Get the transaction history for the user
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    transactions = wallet.get_transaction_history()
    return {"transactions": transactions}


@router.post("/send_transaction")
def send_transaction(transaction: Transaction, user: User = Depends(Auth.auth_required)):
    """
    Send a transaction for the user
    :param transaction:
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    try:
        wallet.send_transaction(transaction.recipient, transaction.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Transaction sent"}


@router.get("/get_transaction_status")
def get_transaction_status(tx_hash: str, user: User = Depends(Auth.auth_required)):
    """
    Get the transaction status for the user
    :param tx_hash:
    :param user:
    :return:
    """
    wallet = Wallet(user.username)
    tx_status = wallet.get_transaction_status(tx_hash)
    return {"transaction_status": tx_status}


@router.get("/get_transaction_fee")
def get_transaction_fee(tx_hash: str, user: User = Depends(Auth.auth_required)):
    """
    Get the transaction fee for the user
    :param tx_hash:
    :param user:
    :return:
    """
    wallet = Wallet(user.user_id)
    tx_fee = wallet.get_transaction_fee(tx_hash)
    return {"transaction_fee": tx_fee}
