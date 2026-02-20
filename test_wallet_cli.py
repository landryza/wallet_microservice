import requests

BASE_URL = "http://127.0.0.1:8002"

def get_wallet(user_id: str):
    """REQUEST: GET wallet. RECEIVE: JSON response."""
    r = requests.get(f"{BASE_URL}/wallet/{user_id}")
    print("[RESPONSE STATUS]", r.status_code)
    r.raise_for_status()
    data = r.json()
    print("[RECEIVED JSON]", data)
    return data

def transact(user_id: str, delta: int):
    """REQUEST: POST transaction. RECEIVE: JSON response."""
    r = requests.post(
        f"{BASE_URL}/wallet/{user_id}/transaction",
        json={"delta": delta},
        headers={"Content-Type": "application/json"},
    )
    print("[RESPONSE STATUS]", r.status_code)
    if r.status_code >= 400:
        # show error message from microservice
        try:
            print("[RECEIVED JSON]", r.json())
        except Exception:
            print("[RECEIVED TEXT]", r.text)
        return None

    data = r.json()
    print("[RECEIVED JSON]", data)
    return data

def read_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Please enter a whole number (example: 50).")

def main():
    print("=== Wallet Microservice CLI Test Program ===")
    print("This program talks to the Wallet Microservice via HTTP (requests library).")
    print("No direct imports from the microservice code.\n")

    user_id = input("Enter user_id: ").strip()
    if not user_id:
        user_id = "nawas"

    while True:
        print("\nMenu")
        print("1) View balance")
        print("2) Add credits")
        print("3) Spend credits (take money out)")
        print("4) Quit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            print("\n[REQUEST] GET /wallet/{user_id}")
            get_wallet(user_id)

        elif choice == "2":
            amount = read_int("Enter amount to ADD (positive whole number): ")
            if amount < 0:
                print("Please enter a positive number.")
                continue
            print("\n[REQUEST] POST /wallet/{user_id}/transaction  (delta = +amount)")
            transact(user_id, amount)

        elif choice == "3":
            amount = read_int("Enter amount to SPEND (positive whole number): ")
            if amount < 0:
                print("Please enter a positive number.")
                continue
            print("\n[REQUEST] POST /wallet/{user_id}/transaction  (delta = -amount)")
            transact(user_id, -amount)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()