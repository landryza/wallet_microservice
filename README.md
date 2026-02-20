# Wallet Microservice

## Description
The Wallet Microservice manages a user's credit balance. It allows other applications (main programs or microservices) to retrieve a user's wallet balance and apply transactions such as adding or subtracting credits.

If a wallet does not exist for a user, it is automatically created with a default balance of 0.

---

# Endpoints

# 1. Health Check
GET /health

Used to verify that the microservice is running.

Example Request:
GET /health

Example Response:
{
  "ok": true
}

---

# 2. Get Wallet Balance
GET /wallet/{user_id}

Retrieves the wallet balance for a given user.  
If the wallet does not exist, it will be created automatically.

Example Request:
GET /wallet/nawas

Example Response:
{
  "user_id": "nawas",
  "balance": 0
}

---

# 3. Apply Transaction
POST /wallet/{user_id}/transaction

Applies a transaction to the user's wallet.  
- Positive value = add credits  
- Negative value = subtract credits  

Balance cannot go below 0.

Example Request:
POST /wallet/nawas/transaction

Body:
{
  "delta": 50
}

Example Response:
{
  "user_id": "nawas",
  "balance": 50
}

Error Example:
{
  "detail": "Insufficient credits (balance cannot go below 0)."
}

---

# Communication Contract

# Requesting Data
To request data from the Wallet Microservice:

1. Send an HTTP request to the appropriate endpoint.
2. Include the user_id in the URL.
3. For transactions, include a JSON body with the "delta" value.

Example (Python):
import requests

response = requests.get("http://127.0.0.1:8002/wallet/nawas")
print(response.json())

---

# Receiving Data
The microservice responds with JSON data.

Example response format:
{
  "user_id": "nawas",
  "balance": 50
}

Example handling in Python:
data = response.json()
print("User:", data["user_id"])
print("Balance:", data["balance"])

---

## UML Sequence Diagram

Main Program        Wallet Microservice        Database
     |                      |                     |
     |---- GET /wallet ---->|                     |
     |                      |---- Query --------->|
     |                      |<--- Result ---------|
     |<--- JSON Response ---|                     |
     |                      |                     |
     |---- POST /transaction -------------------->|
     |                      |---- Update -------->|
     |                      |<--- Success --------|
     |<--- JSON Response ---|                     |

---

# How to Run the Microservice

1. Install dependencies:
pip install -r requirements.txt

2. Start the server:
uvicorn main:app --reload --port 8002

3. Open in browser:
http://127.0.0.1:8002/docs

---

# Test Program Example

import requests

BASE = "http://127.0.0.1:8002"

# Get wallet
r = requests.get(f"{BASE}/wallet/nawas")
print("Wallet:", r.json())

# Add credits
r = requests.post(f"{BASE}/wallet/nawas/transaction", json={"delta": 100})
print("After adding:", r.json())

# Subtract credits
r = requests.post(f"{BASE}/wallet/nawas/transaction", json={"delta": -30})
print("After spending:", r.json())

---

## Notes
- All communication is done using JSON over HTTP.
- Wallets are automatically created when first accessed.
- Negative balances are not allowed.
