from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json
import os

app = FastAPI(title="Wallet Microservice")

FILE_PATH = "wallets.json"
DEFAULT_BALANCE = 0


def load_data():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)


class WalletResponse(BaseModel):
    user_id: str
    balance: int


class TransactionRequest(BaseModel):
    delta: int = Field(..., description="Change in credits (positive or negative)")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/wallet/{user_id}", response_model=WalletResponse)
def get_wallet(user_id: str):
    data = load_data()

    # auto-create wallet
    if user_id not in data:
        data[user_id] = DEFAULT_BALANCE
        save_data(data)

    return WalletResponse(user_id=user_id, balance=data[user_id])


@app.post("/wallet/{user_id}/transaction", response_model=WalletResponse)
def apply_transaction(user_id: str, body: TransactionRequest):
    data = load_data()

    # create wallet if not exists
    if user_id not in data:
        data[user_id] = DEFAULT_BALANCE

    new_balance = data[user_id] + body.delta

    if new_balance < 0:
        raise HTTPException(
            status_code=400,
            detail="Insufficient credits (balance cannot go below 0)."
        )

    data[user_id] = new_balance
    save_data(data)

    return WalletResponse(user_id=user_id, balance=new_balance)