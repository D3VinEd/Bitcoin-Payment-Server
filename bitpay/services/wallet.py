from bit import Key
from bitpay.services.redis import RedisHandler


class Wallet:
    """
    Wallet class to handle all wallet related operations
    """
    def __init__(self, username: str):
        self.username = username
        self.redis = RedisHandler()
        self.keys = self.get_or_create_keys()

    def get_or_create_keys(self) -> list:
        """
        Get existing keys from the database or create new ones if not found
        :return: List of Key objects
        """
        key_hex_list = self.redis.get_keys(self.username)
        if key_hex_list:
            return [Key.from_hex(key_hex) for key_hex in key_hex_list]
        else:
            keys = self.create_keys()
            self.store_keys(keys)
            return keys

    def create_keys(self, num_keys: int = 1) -> list:
        """
        Create new keys
        :param num_keys: Number of keys to create
        :return: List of Key objects
        """
        keys = [Key() for _ in range(num_keys)]
        return keys

    def delete_keys(self) -> None:
        """
        Delete all keys from the database
        """
        self.redis.delete_keys(self.username)

    def store_keys(self, keys: list) -> None:
        """
        Store the keys in the database
        :param keys: List of Key objects
        """
        key_hex_list = [key.to_hex() for key in keys]
        self.redis.store_keys(self.username, key_hex_list)

    def get_balance(self) -> dict:
        """
        Get the balance of all keys
        :return: Dictionary mapping keys to their balances
        """
        balances = {}
        for key in self.keys:
            balances[key.address] = key.get_balance('btc')
        return balances

    def get_transaction_history(self) -> list:
        """
        Get the transaction history of all keys.

        :return: List of transactions
        """
        # Initialisiere eine leere Liste, um die Transaktionen zu speichern.
        transactions = []

        # Gehe durch jeden Schlüssel in self.keys
        for key in self.keys:
            # Ruft die Transaktionen für den aktuellen Schlüssel ab
            # und fügt sie der Liste der Transaktionen hinzu.
            transactions.extend(key.get_transactions())

        # Gibt die Liste der Transaktionen zurück.
        return transactions

    def send_transaction(self, recipient: str, amount: float, key_index: int = 0) -> None:
        """
        Send a transaction from a specific key
        :param recipient: Recipient address
        :param amount: Amount to send
        :param key_index: Index of the key to use
        """
        key = self.get_key(key_index)
        key.send([(recipient, amount, 'btc')])

    def get_transaction_status(self, tx_hash) -> dict:
        """
        Get the transaction status of the key
        :param tx_hash: Transaction hash
        :return: Transaction status as a dictionary
        """
        tx_list = []
        for key in self.keys:
            tx_status = key.get_transaction(tx_hash)
            if tx_status:
                tx_status['key'] = key.address
        return {}

    def get_transaction_fee(self, tx_hash):
        """
        Get the transaction fee of the key
        :param tx_hash: Transaction hash
        :return: Transaction fee
        """
        tx_status = self.get_transaction_status(tx_hash)
        return tx_status.get('fee', 0)

    def get_key(self, key_index: int = 0) -> Key:
        """
        Get a specific key by index
        :param key_index: Index of the key
        :return: Key object
        """
        if key_index < len(self.keys):
            return self.keys[key_index]
        else:
            raise IndexError('Key index out of range')

    def get_keys(self) -> list:
        """
        Get all keys
        :return: List of Key objects
        """
        return self.keys
