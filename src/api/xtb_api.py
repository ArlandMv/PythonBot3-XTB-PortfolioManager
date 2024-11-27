import websocket
import json
import logging
from time import sleep
from config.logger import setup_logger

# Initialize logger
logger = setup_logger("xtb_api")
app_name = "XTB BOT"

# Hardcoded configuration for testing
DEMO_URL = "wss://ws.xtb.com/demo"
DEMO_STREAM_URL = "wss://ws.xtb.com/demoStream"
DEMO_USER_ID = "your test user ID"  # Replace with your test user ID
DEMO_PASSWORD = "your test password"  # Replace with your test password

class XTBApiClient:
    def __init__(self, base_url, stream_url, user_id, password):
        """
        Initialize the XTB API Client.
        """
        self.base_url = base_url
        self.stream_url = stream_url
        self.user_id = user_id
        self.password = password
        self.ws = None
        self.connected = False
        self.stream_session_id = None

    def connect(self):
        """
        Establish WebSocket connection to the XTB API.
        """
        logger.info("Attempting to connect to XTB API WebSocket.")
        try:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.base_url)
            self.connected = True
            logger.info("Connection established successfully.")
        except Exception as e:
            logger.error(f"Error connecting to WebSocket: {e}")
            self.connected = False
            raise

    def login(self):
        """
        Login to the XTB API using user ID and password.
        """
        if not self.connected:
            logger.error("Cannot login, WebSocket is not connected.")
            raise ConnectionError("WebSocket is not connected.")

        logger.info("Logging in to XTB API.")
        login_request = {
            "command": "login",
            "arguments": {
                "userId": self.user_id,
                "password": self.password,
                "appId": "XTB BOT",
                "appName": "XTB BOT"
            }
        }

        try:
            self.ws.send(json.dumps(login_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                #self.stream_session_id = response["streamSessionId"]
                logger.info("Login successful.")
                logger.debug(f"streamSessionId: {self.stream_session_id}")
            else:
                logger.error(f"Login failed: {response}")
                raise Exception("Login failed.")
        except Exception as e:
            logger.error(f"Error during login: {e}")
            raise

    def get_all_currency_pairs(self):
        """
        Retrieve all symbols that are currency pairs.
        """
        if not self.connected:
            logger.error("Cannot fetch symbols, WebSocket is not connected.")
            raise ConnectionError("WebSocket is not connected.")

        logger.info("Fetching all symbols with 'currencyPair' set to True.")
        symbols_request = {"command": "getAllSymbols"}

        try:
            self.ws.send(json.dumps(symbols_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                symbols = response.get("returnData", [])
                currency_pairs = [
                    symbol["symbol"] for symbol in symbols if symbol.get("currencyPair")
                ]
                logger.info(f"{len(currency_pairs)} pairs retrieved: {currency_pairs}")
                return currency_pairs
            else:
                logger.error(f"Error fetching symbols: {response}")
                #raise Exception(f"Error fetching symbols: {response}")
                return []
        except Exception as e:
            logger.error(f"Error fetching symbols: {e}")
            raise

    def get_symbol_data(self, symbol="USDCLP"):
        """
        Retrieve data for the specified symbol from the XTB API.
        """
        if not self.connected:
            logger.error("Cannot retrieve symbol data, WebSocket is not connected.")
            raise ConnectionError("WebSocket is not connected.")

        logger.info(f"Fetching data for symbol: {symbol}.")
        symbol_request = {
            "command": "getSymbol",
            "arguments": {
                "symbol": symbol
            }
        }

        try:
            self.ws.send(json.dumps(symbol_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                symbol_data = response.get("returnData", {})
                logger.info(f"Retrieved data for symbol: {symbol}")
                return symbol_data
            else:
                logger.error(f"Error retrieving symbol data: {response}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching symbol data: {e}")
            raise

    def logout(self):
        """
        Logout from the XTB API and close the WebSocket connection.
        """
        if not self.connected:
            logger.error("Cannot logout, WebSocket is not connected.")
            raise ConnectionError("WebSocket is not connected.")

        logger.info("Logging out and closing connection.")
        logout_request = {"command": "logout"}
        try:
            self.ws.send(json.dumps(logout_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                logger.info("Logged out successfully.")
            else:
                logger.error(f"Error during logout: {response}")
        except Exception as e:
            logger.error(f"Error during logout: {e}")
        finally:
            self.ws.close()
            self.connected = False
            logger.info("Connection closed.")

# Example usage for testing
if __name__ == "__main__":
    # Testing invalid credentials
    BAD_PASSWORD = "badPassword"
    bad_api_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, BAD_PASSWORD)
    try:
        logger.info("Testing invalid credentials.")
        bad_api_client.connect()
        bad_api_client.login()
    except Exception as e:
        logger.error(f"Error during invalid credentials test: {e}")

    # Testing valid credentials
    api_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    try:
        api_client.connect()
        api_client.login()
        currency_pairs = api_client.get_all_currency_pairs()
        logger.info(f"Currency Pairs: {currency_pairs}")
        usdclp_data = api_client.get_symbol_data()
        logger.info(f"USDCLP Data: {usdclp_data}")
        eurusd_data = api_client.get_symbol_data("EURUSD")
        logger.info(f"EURUSD Data: {eurusd_data}")
    except Exception as e:
        logger.error(f"{app_name}: An error occurred: {e}")
    finally:
        # logger.info("COMMENTED:Logging out and closing connection")
        api_client.logout()
