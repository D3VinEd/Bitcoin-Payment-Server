from bit import Key
import redis


class Wallet:
    """
    Wallet class to handle all wallet related operations
    """
    def __init__(self, user_id: str, host='localhost', port=6379, db=0):
        self.user_id = user_id
        self.key = None
        self.redis_db = redis.StrictRedis(host=host, port=port, db=db)

    def create_key(self) -> None:
        """
        Create a new key and store it in the database
        :return:
        """
        self.key = Key()
        self.store_key()

    def delete_key(self) -> None:
        """
        Delete the key from the database
        :return:
        """
        self.redis_db.delete(self.user_id)

    def store_key(self) -> None:
        """
        Store the key in the database
        :return:
        """
        if self.key:
            self.redis_db.set(self.user_id, self.key.to_hex())

    def get_key(self) -> None:
        """
        Get the key from the database
        :return:
        """
        key_hex = self.redis_db.get(self.user_id)
        if key_hex is not None:
            self.key = Key.from_hex(key_hex.decode())
        else:
            self.key = None

    def get_balance(self) -> float:
        """
        Get the balance of the key
        :return:
        """
        if not self.key:
            self.get_key()
        return self.key.get_balance()

    def get_transaction_history(self) -> list:
        """
        Get the transaction history of the key
        :return:
        """
        if not self.key:
            self.get_key()
        return self.key.get_transactions()

    def send_transaction(self, recipient: str, amount: float) -> None:
        """
        Send a transaction from the key
        :param recipient:
        :param amount:
        :return:
        """
        if not self.key:
            self.get_key()
        self.key.send([(recipient, amount, 'btc')])

    def get_transaction(self)-> list:
        """
        Get the transaction history of the key
        :return:
        """
        if not self.key:
            self.get_key()
        return self.key.get_transactions()

    def get_transaction_status(self, tx_hash) -> dict:
        """
        Get the transaction status of the key
        :param tx_hash:
        :return:
        """
        if not self.key:
            self.get_key()
        return self.key.get_transaction(tx_hash)

    def get_transaction_fee(self, tx_hash):
        """
        Get the transaction fee of the key
        :param tx_hash:
        :return:
        """
        if not self.key:
            self.get_key()
        tx = self.get_transaction_status(tx_hash)
        return tx.fee
