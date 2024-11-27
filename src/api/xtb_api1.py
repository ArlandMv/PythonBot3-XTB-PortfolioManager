import json
import websocket
import logging
import time

# Logger setup
logger = logging.getLogger(__name__)

# WebSocket URL for XTB demo
XTB_API_URL = "wss://demo.xtb.com/demo"

# Define the WebSocket client class
class XTBWebSocketClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ws = None
        self.is_logged_in = False

    def on_message(self, ws, message):
        """
        Handles incoming messages from the WebSocket.
        """
        logger.info(f"Message received: {message}")
        data = json.loads(message)

        if data.get("status") == "error":
            logger.error(f"Error: {data.get('errorCode')}")
        else:
            logger.info(f"Received: {data}")

    def on_error(self, ws, error):
        """
        Handles errors in the WebSocket connection.
        """
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """
        Handles WebSocket closure.
        """
        logger.info(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

    def on_open(self, ws):
        """
        Sends login request once WebSocket connection is open.
        """
        logger.info("WebSocket connection established.")
        login_payload = {
            "command": "login",
            "arguments": {
                "user": self.username,
                "password": self.password
            }
        }
        ws.send(json.dumps(login_payload))

    def login(self):
        """
        Connects to XTB API WebSocket and logs in.
        """
        self.ws = websocket.WebSocketApp(
            XTB_API_URL,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.ws.run_forever()

    def logout(self):
        """
        Sends logout request and closes the connection.
        """
        if self.ws:
            logout_payload = {
                "command": "logout",
                "arguments": {}
            }
            self.ws.send(json.dumps(logout_payload))
            self.ws.close()
            self.is_logged_in = False
            logger.info("Logged out of XTB API.")

    def reconnect(self):
        """
        Reconnect to the WebSocket.
        """
        logger.info("Attempting to reconnect...")
        self.ws.close()
        time.sleep(5)  # Delay before reconnecting
        self.login()

    def get_account_status(self):
        """
        Fetch current user data (balance, details).
        """
        if self.ws:
            account_status_payload = {
                "command": "getCurrentUserData",
                "arguments": {}
            }
            self.ws.send(json.dumps(account_status_payload))
        else:
            logger.error("WebSocket connection not established.")

    def get_balance(self):
        """
        Fetch account balance.
        """
        if self.ws:
            balance_payload = {
                "command": "getBalance",
                "arguments": {}
            }
            self.ws.send(json.dumps(balance_payload))
        else:
            logger.error("WebSocket connection not established.")
