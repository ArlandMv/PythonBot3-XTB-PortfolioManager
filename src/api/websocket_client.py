import websocket
from config.logger import setup_logger
##from src.api.xtb_api import trade_transaction, login, ping
from src.api.xtb_api import trade_transaction

# Initialize logger
##logger = setup_logger("websocket_client")
logger = setup_logger(__name__)

"""
TODO: refactor webs socket fundamental functionality from xtb_api.
   - connect/disconnect: Establish WebSocket connection to the XTB API.
   - get_ServerTime
   - trade_transaction
   - trade_status
   - calculate communication time responce
"""

class WebSocketClient:
    def __init__(self, api_url, user_id, password):
        """
        Initializes the WebSocket client.

        Args:
            api_url (str): WebSocket API endpoint.
            user_id (str): User ID for login.
            password (str): Password for login.
        """
        self.api_url = api_url
        self.user_id = user_id
        self.password = password
        self.ws = None

    def connect(self):
        """Establishes the WebSocket connection."""
        self.ws = websocket.WebSocket()
        self.ws.connect(self.api_url)
        logger.info("WebSocket connection established.")
        self.login()

    def login (self):
        """
        Login to the XTB API using user ID and password.
        """
        self.check_connection()

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
                # self.stream_session_id = response["streamSessionId"]
                self.stream_session_id = response.get("streamSessionId")
                logger.info("Login successful.")
                logger.info(f"streamSessionId: {self.stream_session_id}")
            else:
                logger.error(f"Login failed: {response}")
                raise Exception("Login failed.")
        except Exception as e:
            logger.error(f"Error during login: {e}")
            raise

    def send_message(self, message):
        """
        Sends a message to the WebSocket API.

        Args:
            message (str): The JSON-encoded message to send.
        """
        self.ws.send(message)
        logger.debug(f"Sent: {message}")

    def receive_message(self):
        """
        Receives a message from the WebSocket API.

        Returns:
            str: The received message.
        """
        response = self.ws.recv()
        logger.debug(f"Received: {response}")
        return response

    def open_position(self, trade_trans_info):
        """
        Opens a new trading position.

        Args:
            trade_trans_info (dict): Trade transaction details.
        """
        open_msg = trade_transaction(trade_trans_info)
        self.send_message(open_msg)
        logger.info("Open position request sent.")

    def close(self):
        """Closes the WebSocket connection."""
        if self.ws:
            self.ws.close()
            logger.info("WebSocket connection closed.")
