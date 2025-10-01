import csv
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any, Dict, List, Tuple

# Wallet addresses to fetch balances for
WALLET_ADDRESSES = [
    "eth|9Bc3fD09Fa9B41c4FE553D260c467363cfe02aCF",
    "eth|Ce74B68cd1e9786F4BD3b9f7152D6151695A0bA5",
    "eth|4e0CD6A94a839F3D9a6F21013A4B0b8E1C8A51ee",
    "eth|525b8736346f2caCdaEF4Cb5ADc8c363cD686328",
    "eth|011b28dE014c2C7aA20F74B6770943e580fda44A",
    "client|64f8caf887fd8551315d8509",
    "eth|65a48cB6522fE413b4CA8934A05b49B0ad9a0273",
    "eth|5CA0CA28FA41f0708Bc012932627d3F357dE6a63",
    "eth|978BB9ec5AF287EBff8f5C3BeC2568EED56aE4a9",
    "eth|FAad688C3F47b94D2e87e5ad82227253e6620B14",
    "eth|c8d3905caA0470c0de6453f6fadd1e992c5b6514",
    "eth|7DA43D52ecCE61928D0E400f91B334588e5e4147",
    "client|68cc5c76ff0d8c0bf890f3cb",
    "eth|E7DFA9CeCdD6f13Dbe31ea9Ed0880FFFF05Dab42",
    "client|67a3ca6ab4ab0eda1efce911",
    "eth|a2bBbE535c45b2b16E2B6B565340c348d6196e14",
    "eth|3ae1c40d40Bdc0f7C0880304322DAAC5bFa5fFdb",
    "client|66a3f1f7d245c20ec2f3f702",
    "eth|aA3572e4D2f404B990EfF523dbDB429F84d443CC",
    "eth|b418939E1648e802CAddDcC0D322276b705Cd71d",
    "eth|202CC786aC010bCcDce466C83B0D21199CDddC4E",
    "eth|332096d4C25077dAd45671df1e039C8e14B0A821",
    "eth|B1cA4D8a56e809362c1De802796890435A6193Fa",
    "eth|380AaB389FD374F16BC23187ac629b985Bbf1174",
    "eth|91Ab910C6971eB39FC1ff92A8A126e5da25373AF",
    "eth|089018e67E35BeAAb3F7c28cb0d64dBA04D9268F",
    "eth|525bF629BAD144834270ff8F6798Cc18959b3F7C",
    "eth|35F2eD4185Bb583a5985308b2640adFBcb60AaDa",
    "eth|2f7c7e2D248d8784fC186A5Cd2d5aD0e4E6dAE1f",
    "eth|A1dbe677cfd899827b4e6450B4463bDC7a7C0A6d",
    "eth|6f808c9BA88a4d059EEA6B3f64F3E14C28842741",
    "eth|061c0fF56daFaAC0BCb78999E59deba36aAB5703",
    "eth|d8cA0104E71fB8DF6a142fD27F10F8F20A3d2529",
]

# Tokens to fetch
TOKENS = ["GALA", "GUSDC", "GUSDT"]

# API endpoint
API_URL = "https://gateway-mainnet.galachain.com/api/asset/token-contract/FetchBalances"


def fetch_balance(owner: str, token: str) -> Tuple[str, str, str]:
    """Fetch balance for a single owner and token. Returns (owner, token, balance)."""
    payload = {
        "owner": owner,
        "collection": token,
        "category": "Unit",
        "additionalKey": "none",
        "type": "none",
    }
    
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.getcode() == 200:
                result = json.loads(response.read().decode("utf-8"))
                if result.get("Status") == 1 and result.get("Data"):
                    balance = str(result["Data"][0].get("quantity", "0"))
                    return (owner, token, balance)
    except Exception:
        pass
    return (owner, token, "0")


def main():
    """Fetch all balances and save to CSV using concurrent requests."""
    print("Fetching balances from GalaChain (concurrent)...")
    
    # Create all tasks (owner, token) pairs
    tasks = []
    for owner in WALLET_ADDRESSES:
        for token in TOKENS:
            tasks.append((owner, token))
    
    print(f"Total requests: {len(tasks)}")
    
    # Use ThreadPoolExecutor for concurrent requests
    results = {}
    completed = 0
    lock = Lock()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(fetch_balance, owner, token): (owner, token) 
                         for owner, token in tasks}
        
        # Process completed tasks
        for future in as_completed(future_to_task):
            owner, token, balance = future.result()
            
            # Store result
            if owner not in results:
                results[owner] = {}
            results[owner][token] = balance
            
            # Progress update
            with lock:
                completed += 1
                if completed % 10 == 0 or completed == len(tasks):
                    print(f"Progress: {completed}/{len(tasks)} requests completed")
    
    # Convert results to list format
    all_balances = []
    for owner in WALLET_ADDRESSES:
        row = {"owner": owner}
        for token in TOKENS:
            row[token] = results.get(owner, {}).get(token, "0")
        all_balances.append(row)
    
    # Write to CSV
    with open("balances.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["owner"] + TOKENS)
        writer.writeheader()
        writer.writerows(all_balances)
    
    print(f"\nSaved {len(all_balances)} rows to balances.csv")


if __name__ == "__main__":
    main()


