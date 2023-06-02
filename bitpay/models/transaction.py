from pydantic import BaseModel


class Transaction(BaseModel):
    recipient: str
    amount: float
