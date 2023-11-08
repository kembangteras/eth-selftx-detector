import requests
import time

ETHERSCAN_API_KEY = "YourApiKeyToken"
WALLET_ADDRESS = "0x000000000000000000000000000000000000dEaD"
TX_LIMIT = 50

def fetch_transactions(address):
    url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=txlist"
        f"&address={address}"
        f"&startblock=0&endblock=99999999"
        f"&sort=desc"
        f"&apikey={ETHERSCAN_API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    if data["status"] != "1":
        print("⚠️  Failed to fetch transactions.")
        return []
    return data["result"][:TX_LIMIT]

def detect_self_transfers(transactions):
    print(f"\n🔍 Checking for self-transfers in last {TX_LIMIT} transactions...\n")
    for tx in transactions:
        if tx["from"].lower() == tx["to"].lower():
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx["timeStamp"])))
            print(f"🧾 Tx Hash: {tx['hash']}")
            print(f"    ↳ Time: {timestamp}")
            print(f"    ↳ Amount: {int(tx['value']) / 1e18:.6f} ETH")
            print()

def main():
    txs = fetch_transactions(WALLET_ADDRESS)
    if txs:
        detect_self_transfers(txs)
    else:
        print("No transactions found or API error.")

if __name__ == "__main__":
    main()
