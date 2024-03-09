import os
from dotenv import load_dotenv
import time
import requests
import json
from nacl.signing import SigningKey
import base64

# Load environment variables from .env file
load_dotenv()

# Get these from your .env file
ORDERLY_KEY = os.getenv("ORDERLY_KEY")
ORDERLY_SECRET = os.getenv("ORDERLY_SECRET")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Base URL for the Orderly API
BASE_URL = "https://api-evm.orderly.org"

# Function to generate the signature
def generate_signature(message):
    sk = SigningKey(ORDERLY_SECRET, encoder=base64.urlsafe_b64decode)
    signature = sk.sign(message.encode())
    return base64.urlsafe_b64encode(signature.signature).decode()

# Function to send a request to the Orderly API
def send_request(method, path, data=None):
    timestamp = str(int(time.time() * 1000))
    message = timestamp + method.upper() + path
    if data is not None:
        message += json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "orderly-account-id": ACCOUNT_ID,
        "orderly-key": ORDERLY_KEY,
        "orderly-signature": generate_signature(message),
        "orderly-timestamp": timestamp
    }
    url = BASE_URL + path
    if method.lower() == "get":
        response = requests.get(url, headers=headers)
    elif method.lower() == "post":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Function to get the current market price
def get_market_price(symbol):
    orderbook = send_request("get", f"/v1/orderbook/{symbol}")
    # Assuming the market price is the last bid price
    market_price = orderbook["bids"][-1]["price"]
    return market_price

# Function to create an order
def create_order(symbol, size, side):
    market_price = get_market_price(symbol)
    # Adjust the price to ensure the bot is a maker
    maker_price = market_price - 0.01
    data = {
        "symbol": symbol,
        "order_type": "LIMIT",
        "order_price": maker_price,
        "order_quantity": size,
        "side": side
    }
    return send_request("post", "/v1/order", data)

# Main function
def main():
    symbol = input("Enter the pair you want to trade: ")
    size = float(input("Enter the trade size in USDC: "))
    while True:
        # Create a BUY order
        order = create_order(symbol, size, "BUY")
        print(f"Created BUY order: {order}")
        # Create a SELL order of the same size to close the position
        close_order = create_order(symbol, size, "SELL")
        print(f"Created SELL order to close position: {close_order}")
        # Wait 5 seconds before opening another one
        time.sleep(5)

if __name__ == "__main__":
    main()
