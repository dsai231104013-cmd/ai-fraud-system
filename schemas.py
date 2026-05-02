from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float

class ChatRequest(BaseModel):
    message: str