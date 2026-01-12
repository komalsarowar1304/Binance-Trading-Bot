import logging
from binance.client import Client
from binance.enums import *

# API Credentials from your Binance Testnet Account
API_KEY = "PLACE_YOUR_API_KEY_HERE"
SECRET_KEY = "PLACE_YOUR_SECRET_KEY_HERE"
# Logging Setup: This will record all API requests and responses
logging.basicConfig(
    filename='trading_bot.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret):
        # Initializing Binance Client with Testnet enabled
        self.client = Client(api_key, api_secret, testnet=True)
        # Setting the Base URL for Futures Testnet
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        print("Successfully connected to Binance Futures Testnet.")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Function to place Market and Limit orders on Binance Futures.
        """
        try:
            print(f"Placing {order_type} {side} order for {symbol}...")
            logging.info(f"Attempting {order_type} {side} order: {symbol}, Qty: {quantity}, Price: {price}")
            
            if order_type.upper() == 'MARKET':
                # Market Order Execution
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side.upper(),
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type.upper() == 'LIMIT':
                # Limit Order Execution (Requires Price and TimeInForce)
                if not price:
                    print("Error: Price is required for Limit orders.")
                    return
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side.upper(),
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                print("Invalid order type. Choose MARKET or LIMIT.")
                return

            # Success Logging
            logging.info(f"Order Successful. Response: {order}")
            print(f"Order Executed Successfully! Order ID: {order.get('orderId')}")
            return order

        except Exception as e:
            # Error Logging
            logging.error(f"Order Failed. Error: {str(e)}")
            print(f"Execution Error: {e}")
            return None

# Command Line Interface (CLI) for User Input
if __name__ == "__main__":
    bot = BasicBot(API_KEY, SECRET_KEY)
    
    print("\n--- Binance Crypto Trading Bot CLI ---")
    try:
        symbol_input = input("Enter Symbol (e.g., BTCUSDT): ").upper()
        side_input = input("Enter Side (BUY/SELL): ").upper()
        type_input = input("Enter Order Type (MARKET/LIMIT): ").upper()
        qty_input = input("Enter Quantity (e.g., 0.001): ")
        
        price_input = None
        if type_input == 'LIMIT':
            price_input = input("Enter Limit Price: ")

        bot.place_order(symbol_input, side_input, type_input, qty_input, price_input)
    except KeyboardInterrupt:

        print("\nBot stopped by user.")
