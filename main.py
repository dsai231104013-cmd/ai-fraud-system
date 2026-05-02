from fastapi import FastAPI
import requests

from shared.schemas import Transaction, ChatRequest
from shared.config import FRAUD_SERVICE_URL, CHATBOT_SERVICE_URL
from logs.logger import log

app = FastAPI()

# ---------------- FRAUD ROUTE ----------------
@app.post("/fraud")
def fraud(tx: Transaction):
    try:
        log(f"Gateway -> Fraud request: {tx.amount}")

        res = requests.post(
            FRAUD_SERVICE_URL,
            json=tx.dict(),
            timeout=5
        )

        log(f"Gateway -> Fraud response: {res.json()}")
        return res.json()

    except Exception as e:
        log(f"Gateway ERROR (fraud): {str(e)}")
        return {"error": "Fraud service failed"}

# ---------------- CHAT ROUTE ----------------
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        log(f"Gateway -> Chat request: {req.message}")

        res = requests.post(
            CHATBOT_SERVICE_URL,
            json=req.dict(),
            timeout=5
        )

        log(f"Gateway -> Chat response: {res.json()}")
        return res.json()

    except Exception as e:
        log(f"Gateway ERROR (chat): {str(e)}")
        return {"error": "Chat service failed"}