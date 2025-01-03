from datetime import datetime ##measure responces

from websocket import create_connection, WebSocketConnectionClosedException
import json
from time import sleep, time
from config.logger import setup_logger
from src.api.xtb_api_utils import XtbApiUtils, get_time, milliseconds_to_string, ms_to_datetime, ms_to_time_object

from dotenv import load_dotenv
import os
load_dotenv()

# Initialize logger
logger = setup_logger("xtb_api")
app_name = "XTB BOT"

# configuration for testing
DEMO_URL = os.getenv("DEMO_URL")
DEMO_STREAM_URL = os.getenv("DEMO_STREAM_URL")
DEMO_USER_ID = os.getenv("DEMO_USER_ID")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")

class XTBApiClient:
    def __init__(self, base_url, stream_url, user_id, password, max_retries=3, retry_delay=5):
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
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.exec_start = get_time() #milliseconds
        logger.info(f"XTB API Client initialized at {milliseconds_to_string(self.exec_start)}.")

    def connect(self):
        """
        Establish WebSocket connection to the XTB API.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                logger.info("Attempting to connect to XTB API WebSocket.")
                #self.ws = websocket.WebSocket()
                #self.ws.connect(self.base_url)
                self.ws = create_connection(self.base_url, timeout=10)
                self.connected = True
                logger.info("Connection established successfully.")
                return
            except (ConnectionError, WebSocketConnectionClosedException) as e:
                retries += 1
                logger.error(f"Connection attempt {retries}/{self.max_retries} failed: {e}")
                sleep(self.retry_delay)

            logger.error("Max retries reached. Unable to connect to XTB API.")
            raise ConnectionError("Failed to connect to XTB API after retries.")

    def disconnect(self):
        if self.ws:
            try:
                logger.info("Closing connection.")
                self.ws.close()
                self.connected = False
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")

    def check_connection(self):
        """
        Ensure the WebSocket connection is active.
        """
        if not self.connected:
            logger.error("WebSocket is not connected.")
            raise ConnectionError("WebSocket is not connected.")

    def monitor_connection(self):
        """
        UNTESTED.
        """
        self.check_connection()
        try:
            logger.info("Monitoring WebSocket connection.")
            self.ws.ping()  # Example of sending a heartbeat if supported
        except WebSocketConnectionClosedException:
            logger.error("WebSocket connection lost. Reconnecting...")
            self.connect()

    def login(self):
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
                #self.stream_session_id = response["streamSessionId"]
                self.stream_session_id = response.get("streamSessionId")
                logger.info("Login successful.")
                logger.info(f"streamSessionId: {self.stream_session_id}")
            else:
                logger.error(f"Login failed: {response}")
                raise Exception("Login failed.")
        except Exception as e:
            logger.error(f"Error during login: {e}")
            raise

    def logout(self):
        """
        Logout from the XTB API and close the WebSocket connection.
        """
        self.check_connection()

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
            self.disconnect()

    # get symbols funtions

    def get_all_symbols(self):
        """
        Retrieve all symbols.
        """
        self.check_connection()
        symbols_request = {"command": "getAllSymbols"}

        try:
            self.ws.send(json.dumps(symbols_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                symbols = response.get("returnData", [])
                return symbols
            else:
                logger.error(f"Error fetching symbols: {response}")
                #raise Exception(f"Error fetching symbols: {response}")
                return []
        except Exception as e:
            logger.error(f"Error fetching symbols: {e}")
            raise

    def get_symbols_by_type(self, type_filter):
        """
        Retrieve all symbols of a specific category.
        """
        self.check_connection()

        logger.info(f"Fetching all symbols with 'categoryName' set to {type_filter}.")
        symbols_request = {"command": "getAllSymbols"}

        try:
            self.ws.send(json.dumps(symbols_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                symbols = response.get("returnData", [])
                filtered_symbols = [symbol for symbol in symbols if symbol.get('categoryName') == type_filter]
                logger.info(f"{len(filtered_symbols)} symbols retrieved: {filtered_symbols}")
                return filtered_symbols
            else:
                logger.error(f"Error fetching symbols: {response}")
                # raise Exception(f"Error fetching symbols: {response}")
                return []
        except Exception as e:
            logger.error(f"Error fetching symbols: {e}")
            raise

    def get_all_currency_pairs(self):
        """
        Retrieve all symbols that are currency pairs.
        """
        self.check_connection()

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

    def get_cfd_symbols(self):
        """
        Retrieve all symbols suitable for speculative trading or short selling (CFDs).
        """
        self.check_connection()

        logger.info("Fetching all speculative trading or short-selling symbols.")
        try:
            # Fetch all symbols
            symbols = self.get_all_symbols()

            # Filter for CFDs
            cfd_symbols = [
                symbol for symbol in symbols
                if symbol.get("shortSelling", False)  # Must support short selling
                   and symbol.get("leverage", 0) > 0  # Must have leverage
                   and symbol.get("categoryName", "").upper() == "STC"  # Stocks (as CFDs)
            ]

            logger.info(f"Found {len(cfd_symbols)} speculative symbols.")
            return cfd_symbols
        except Exception as e:
            logger.error(f"Error fetching speculative symbols: {e}")
            raise

    def get_symbol_data(self, symbol="USDCLP"):
        """
        Retrieve data for the specified symbol from the XTB API.
        """
        self.check_connection()

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

    def get_server_time(self):
        """
        Returns current time on trading server.

        Time described in form set on server (local time of server)

        ex: "returnData": {
           		"time": 1392211379731,
           		"timeString": "Feb 12, 2014 2:22:59 PM" }
        """
        self.check_connection()
        logger.info("Fetching server time.")
        symbol_request = {"command": "getServerTime"}

        try:
            self.ws.send(json.dumps(symbol_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                time_data = response.get("returnData", {})
                logger.info(f"Retrieved time: {time_data['timeString']}")
                return time_data['time']
            else:
                logger.error(f"Error retrieving TradingHours data: {response}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching server time: {e}")
            raise

    def get_trading_hours(self, symbol="USDCLP"):
        """
        Retrieve quotes and trading times.
        """
        self.check_connection()

        logger.info(f"Fetching TradingHours for symbol: {symbol}.")
        symbol_request = {
            "command": "getTradingHours",
            "arguments": {
                "symbols": [symbol]
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
                logger.error(f"Error retrieving TradingHours data: {response}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching TradingHours data: {e}")
            raise

    def is_symbol_tradable(self, symbol="USDCLP"):
        """
        Validate if the market is open for the given symbol.
        """
        server_time_ms = self.get_server_time()
        trading_hours = self.get_trading_hours(symbol)
        if not trading_hours or not trading_hours[0].get("trading"):
            logger.info(f"Trading hours not available for symbol {symbol}.")
            return False
        # quotes[], symbol[]
        try:
            logger.info(f"checking market for symbol {symbol}.")
            server_time_dt = ms_to_datetime(server_time_ms)
            server_day = server_time_dt.weekday()  # 0=Monday, ..., 6=Sunday
            trading_periods = [period for period in trading_hours[0]["trading"] if period["day"] == server_day]

            if not trading_periods:
                logger.warning(f"No trading periods found for symbol {symbol} on day {server_day}.")
                return False

            # Use the first trading period for today's trading hours
            fromT = trading_periods[0]["fromT"]
            toT = trading_periods[0]["toT"]

            # Convert server time to time in milliseconds from midnight
            server_time_of_day = (
                    server_time_dt.hour * 3600000 +
                    server_time_dt.minute * 60000 +
                    server_time_dt.second * 1000
            )
            # Check if the current time is within the trading period
            if fromT <= server_time_of_day <= toT:
                #print (from {fromT} to {ms_to_time_object(toT)
                logger.info(
                    f"Market for {symbol} is open.")
                return True
            else:
                logger.info(f"Market for {symbol} is closed (current time: {server_time_of_day} ms).")
                return False

        except Exception as e:
            logger.error(f"Error determining tradability: {e}")
            return False



    def to_milliseconds(self, days=0, hours=0, minutes=0):
        milliseconds = (days * 24 * 60 * 60 * 1000) + (hours * 60 * 60 * 1000) + (minutes * 60 * 1000)
        return milliseconds

    def get_ServerTime(self):
        time = {
            "command": "getServerTime"
        }
        time_json = json.dumps(time)
        result = self.ws.send(time_json)
        result = json.loads(self.ws.recv())
        time = result["returnData"]["time"]
        return time

    def get_Candles(self, period, symbol, days=0, hours=0, minutes=0, qty_candles=0):
        if period == "M1":
            minutes += qty_candles
            period = 1
        elif period == "M5":
            minutes += qty_candles * 5
            period = 5
        elif period == "M15":
            minutes += qty_candles * 15
            period = 15
        elif period == "M30":
            minutes += qty_candles * 30
            period = 30
        elif period == "H1":
            minutes += qty_candles * 60
            period = 60
        elif period == "H4":
            minutes += qty_candles * 240
            period = 240
        elif period == "D1":
            minutes += qty_candles * 1440
            period = 1440
        elif period == "W1":
            minutes += qty_candles * 10080
            period = 10080
        elif period == "MN1":
            minutes += qty_candles * 43200
            period = 43200
        if qty_candles != 0:
            minutes = minutes * 2
        start = self.get_ServerTime() - self.to_milliseconds(days=days, hours=hours, minutes=minutes)
        CHART_LAST_INFO_RECORD = {
            "period": period,
            "start": start,
            "symbol": symbol
        }
        candles = {
            "command": "getChartLastRequest",
            "arguments": {
                "info": CHART_LAST_INFO_RECORD
            }
        }
        candles_json = json.dumps(candles)
        result = self.ws.send(candles_json)
        result = json.loads(self.ws.recv())
        candles = []
        candle = {}
        qty = len(result["returnData"]["rateInfos"])
        candle["digits"] = result["returnData"]["digits"]
        if qty_candles == 0:
            candle["qty_candles"] = qty
        else:
            candle["qty_candles"] = qty_candles
        candles.append(candle)
        if qty_candles == 0:
            start_qty = 0
        else:
            start_qty = qty - qty_candles
        if qty == 0:
            start_qty = 0

        for i in range(start_qty, qty):
            candle = {}
            candle["datetime"] = result["returnData"]["rateInfos"][i]["ctmString"]
            candle["open"] = result["returnData"]["rateInfos"][i]["open"]
            candle["close"] = result["returnData"]["rateInfos"][i]["close"]
            candle["high"] = result["returnData"]["rateInfos"][i]["high"]
            candle["low"] = result["returnData"]["rateInfos"][i]["low"]
            candles.append(candle)
        if len(candles) == 1:
            return False
        return candles
        '''
        LIMITS:
        PERIOD_M1 --- <0-1) month, i.e. one month time
        PERIOD_M30 --- <1-7) month, six months time
        PERIOD_H4 --- <7-13) month, six months time
        PERIOD_D1 --- 13 month, and earlier on
        ##############################################
        PERIOD_M1	1	1 minute
        PERIOD_M5	5	5 minutes
        PERIOD_M15	15	15 minutes
        PERIOD_M30	30	30 minutes
        PERIOD_H1	60	60 minutes (1 hour)
        PERIOD_H4	240	240 minutes (4 hours)
        PERIOD_D1	1440	1440 minutes (1 day)
        PERIOD_W1	10080	10080 minutes (1 week)
        PERIOD_MN1	43200	43200 minutes (30 days)
        ##############################################
        close   Value of close price (shift from open price)
        ctm     Candle start time in CET / CEST time zone (see Daylight Saving Time)
        ctmString     String representation of the 'ctm' field
        high    Highest value in the given period (shift from open price)
        low     Lowest value in the given period (shift from open price)
        open    Open price (in base currency * 10 to the power of digits)
        vol     Volume in lots
        '''

    # TRADE TRANSACTION FUNCTIONS

    def trade_transaction(self, cmd, symbol, price, custom_comment="", order=0, sl=0.0, tp=0.0, type=0, volume=0.01, expiration=0, offset=0):
        """
        Execute a trade transaction using the XTB API.
        """
        self.check_connection()

        logger.info(f"Executing trade transaction for symbol: {symbol}, cmd: {cmd}, price: {price}, volume: {volume}.")
        TRADE_TRANS_INFO = {
            "cmd": cmd,
            "customComment": custom_comment,
            "expiration": expiration,
            "offset": offset,
            "order": order,
            "price": price,
            "sl": sl,
            "symbol": symbol,
            "tp": tp,
            "type": type,
            "volume": volume,
        }

        trade_request={
            "command": "tradeTransaction",
            "arguments": {
                "tradeTransInfo": TRADE_TRANS_INFO
            }
        }
        try:
            trade_json=json.dumps(trade_request)
            result = self.ws.send(trade_json)
            response = json.loads(self.ws.recv())

            if response.get("status"):
                transaction_data = response.get("returnData", {})
                logger.info(f"Trade transaction successful for symbol: {symbol}")
                return transaction_data
            else:
                logger.error(f"Error executing trade transaction: {response}")
                return {}
        except Exception as e:
            logger.error(f"Error during trade transaction: {e}")
            raise

    def trade_status(self, order):
        self.check_connection()
        trade_request = {
            "command": "tradeTransactionStatus",
            "arguments": {
                "order": order
            }
        }
        try:
            self.ws.send(json.dumps(trade_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                t_data = response.get("returnData", {})
                status = t_data["requestStatus"]
                logger.info(f"status are 3 ACCEPTED, 4  REJECTED: {status}" )
                return t_data
            else:
                logger.error(f"Error retrieving symbol data: {response}")
                return {}
        except Exception as e:
            logger.error(f"Error fetching symbol data: {e}")
            raise

    def open_trade(self, symbol, is_long=True, volume=0.01, sl=0.0, tp=0.0, custom_comment=""):
        """
        Open a trade with the asking price of a symbol using get_symbol.
        """
        self.check_connection()

        try:
            # Retrieve the symbol data
            symbol_data = self.get_symbol_data(symbol)
            ask_price = symbol_data.get("ask")  # Price for buying (long)
            bid_price = symbol_data.get("bid")  # Price for selling (short)

            if ask_price is None or bid_price is None:
                logger.error(f"Failed to retrieve prices for symbol: {symbol}")
                return {"status": False, "message": "Prices not found"}

            price = ask_price if is_long else bid_price
            cmd = 0 if is_long else 1  # 0: BUY (long), 1: SELL (short)

            risk = abs(ask_price - bid_price)
            sl = (price - risk) if is_long else (price + risk) if sl is None else sl
            tp = (price + (abs(price - sl) * 1.5)) if is_long else (
                        price - (abs(price - sl) * 1.5)) if tp is None else tp

            logger.info(
                f"Opening {'long' if is_long else 'short'} trade for {symbol} at price {price}, "
                f"volume {volume}, SL {sl}, TP {tp}."
            )

            logger.info(f"Opening trade for {symbol} at price {ask_price} with volume {volume}.")

            # Prepare trade payload
            trade_payload = {
                "command": "tradeTransaction",
                "arguments": {
                    "tradeTransInfo": {
                        "cmd": cmd,  # '0' means BUY and 1 means SELL
                        "customComment": custom_comment,
                        "price": ask_price,
                        "sl": sl,
                        "tp": tp,
                        "symbol": symbol,
                        "type": 0,  # '0' indicates market order
                        "volume": volume,
                    }
                }
            }

            # Send trade transaction request
            self.ws.send(json.dumps(trade_payload))
            response = json.loads(self.ws.recv())

            if response.get("status"):
                logger.info(f"Trade opened successfully for {symbol}. Order details: {response.get('returnData')}")
                return response.get("returnData", {})
            else:
                logger.error(f"Failed to open trade for {symbol}. Error: {response}")
                return {"status": False, "message": response.get("errorDescr", "Unknown error")}

        except Exception as e:
            logger.error(f"Error while opening trade for {symbol}: {e}")
            raise

    def open_position_amount (self, symbol: str, amount: float, cmd: int = 0, stop_loss: float = None,
                       take_profit: float = None):
        """
        Open a trading position for a given symbol with the specified amount.

        :param symbol: The trading symbol (e.g., "EURUSD").
        :param amount: The amount of money allocated for the trade.
        :param cmd: The trade type (0 for BUY, 1 for SELL). Default is 0 (BUY).
        :param stop_loss: Optional stop-loss price.
        :param take_profit: Optional take-profit price.
        """
        logger.info(f"Preparing to open position for symbol: {symbol} with amount: {amount}.")

        # Get the ask price for the symbol
        symbol_data = self.get_symbol_data(symbol)
        ask_price = symbol_data.get("ask")

        # TODO: refactor object validators
        if ask_price is None:
            logger.error(f"Unable to fetch ask price for symbol: {symbol}.")
            raise ValueError(f"Invalid symbol or missing ask price for {symbol}.")

        # Calculate the volume based on the amount and ask price
        volume = amount / ask_price
        logger.info(f"Calculated volume: {volume} for symbol: {symbol} at ask price: {ask_price}.")

        # missing 3 required positional arguments: 'symbol', 'volume', and 'price'

        # Prepare trade transaction details
        trade_trans_info = {
            "symbol": symbol,
            "cmd": cmd,  # 0 for BUY, 1 for SELL
            "volume": volume,
            "price": ask_price,
            "sl": stop_loss,  # Optional stop-loss
            "tp": take_profit,  # Optional take-profit
            "type": 0,  # Market order
            "customComment": "Trade opened by XTB BOT"
        }

        # Execute the trade transaction
        return self.trade_transaction(trade_trans_info)

    def close_trade_volume(self, order_id, symbol, volume=0.01, custom_comment=""):
        """
        Close an open trade position using the order ID.
        Args:
            order_id (int): The order ID of the trade to close.
            symbol (str): The symbol of the trade (e.g., EURUSD).
            volume (float): Volume to close (default: 0.01).
            custom_comment (str): Optional comment for the closing trade.

        Returns:
            dict: Response from the trade transaction.
        """
        self.check_connection()

        try:
            # Retrieve symbol prices to close the trade
            symbol_data = self.get_symbol_data(symbol)
            ask_price = symbol_data.get("ask")  # Price for BUY
            bid_price = symbol_data.get("bid")  # Price for SELL

            if ask_price is None or bid_price is None:
                logger.error(f"Failed to retrieve prices for symbol: {symbol}")
                return {"status": False, "message": "Prices not found"}

            # Determine the command based on the current position
            # If the position was a BUY (cmd=0), we close it with a SELL (cmd=1)
            # If the position was a SELL (cmd=1), we close it with a BUY (cmd=0)
            order_data = self.get_trade_order(order_id)  # Assuming this method retrieves trade details
            if not order_data:
                logger.error(f"Failed to retrieve trade details for order ID: {order_id}")
                return {"status": False, "message": "Trade details not found"}

            cmd = 1 if order_data["cmd"] == 0 else 0  # Invert the command to close the position
            close_price = bid_price if cmd == 1 else ask_price  # Use correct price for closing

            logger.info(f"Closing trade for {symbol} (order ID: {order_id}) at price {close_price}, volume {volume}.")

            # Execute the trade transaction to close the position
            transaction_data = self.trade_transaction(
                cmd=cmd,
                expiration=0,  # Immediate execution
                symbol=symbol,
                price=close_price,
                order=order_id,
                custom_comment=custom_comment,
                volume=volume
            )

            if transaction_data:
                logger.info(f"Trade closed successfully. Order ID: {order_id}, Details: {transaction_data}")
                return transaction_data
            else:
                logger.error(f"Failed to close trade for order ID: {order_id}.")
                return {"status": False, "message": "Failed to close trade"}

        except Exception as e:
            logger.error(f"Error while closing trade for order ID: {order_id}: {e}")
            raise

    def close_trade(self, order_id, symbol, custom_comment):
        """
        Close an open trade position using the order ID.

        Args:
            order_id (int): The order ID of the trade to close.
            symbol (str): The symbol of the trade (e.g., EURUSD).
            price(float): required
            volume optinal?
            expiration(int): OPTIONAL date like 1462006335000
            custom_comment (str): OPTIONAL comment for the closing trade.

        Returns:
            dict: Response from the trade transaction.
        """
        self.check_connection()

        # Retrieve symbol prices
        symbol_data = self.get_symbol_data(symbol)
        ask_price = symbol_data.get("ask")  # Price for BUY
        bid_price = symbol_data.get("bid")  # Price for SELL

        if ask_price is None or bid_price is None:
            logger.error(f"Failed to retrieve prices for symbol: {symbol}")
            return {"status": False, "message": "Prices not found"}

        # Determine the correct cmd to close the position
        cmd = 0
        close_price = bid_price if cmd == 1 else ask_price  # Correct price for closing
        close_price = ask_price #1.04913 it should be market price 1.04820
        close_price = self.get_Candles("M1", symbol, qty_candles=1)
        close_price = close_price[1]["open"] + close_price[1]["close"] #104938.0 instead of 1.04938
        close_price = close_price /100000
        close_price -= 0.00001 #slippage
        try:
            logger.info(f"Closing trade for {symbol} (order ID: {order_id}) at price {close_price}.")

            # Execute the trade transaction to close the position
            transaction_data = self.trade_transaction(
                cmd=cmd,
                expiration=0,  # Immediate execution
                symbol=symbol,
                price=close_price,
                order=order_id,
                custom_comment=custom_comment,
                volume=0.01,
                type=2
            )

            if transaction_data:
                logger.info(f"Trade closed successfully. Order ID: {order_id}, Details: {transaction_data}")
                return transaction_data
            else:
                logger.error(f"Failed to close trade for order ID: {order_id}.")
                return {"status": False, "message": "Failed to close trade"}

        except Exception as e:
            logger.error(f"Error while closing trade for order ID: {order_id}: {e}")
            raise

    def close_position(self, order_id, volume):
        """
        Close an open position.
        :param order_id: The unique identifier of the open position.
        :param volume: The volume to close.
        """
        self.check_connection()
        # Retrieve position data(cmd,symbol,volume)
        # check volume to close <= position volume
        # Retrieve the current market price acording to cmd and symbol
        try:
            position = self.get_trade_record([order_id])
            position_cmd = position['cmd']
            position_volume = position['volume']
            position_profit = position['profit']
            symbol = position['symbol']
            symbol_data = self.get_symbol_data(symbol)
            bid_price = symbol_data.get("bid")
            ask_price = symbol_data.get("ask")

            if bid_price is None or ask_price is None or position is None:
                logger.error("Failed to retrieve position data")
                return {"status": False, "message": "Position Data not found"}

            if volume > position_volume:
                logger.error(f"Volume to close ({volume}) exceeds position volume ({position_volume}).")

            price = ask_price if position_cmd == 0 else bid_price  # Use ask price for BUY positions, bid price for SELL positions

            # Prepare the trade transaction payload
            trade_trans_info = {
                "cmd": position_cmd,
                "customComment": "Closing position",
                "expiration": 0,
                "order": order_id,
                "price": price,
                "sl": 0.0,
                "tp": 0.0,
                "symbol": symbol,
                "type": 2,  # Type 2 indicates closing an existing position
                "volume": volume,
            }

            trade_request = {
                "command": "tradeTransaction",
                "arguments": {
                    "tradeTransInfo": trade_trans_info
                }
            }

            self.ws.send(json.dumps(trade_request))
            response = json.loads(self.ws.recv())

            if response.get("status"):
                logger.info(f"Successfully closed position {order_id} for symbol {symbol}.")
                return response.get("returnData", {})
            else:
                logger.error(f"Failed to close position {order_id} for symbol {symbol}. Error: {response}")
                #return {"status": False, "message": response.get("errorDescr", "Unknown error")}
                return response

        except Exception as e:
            logger.error(f"Error while closing position {order_id}: {e}")
            raise

    def get_trade_record(self, orders):
        """
        Retrieve trade records for the given order numbers from the XTB API.
        """
        self.check_connection()

        logger.info(f"Fetching trade records for orders: {orders}.")
        trade_records_request = {
            "command": "getTradeRecords",
            "arguments": {
                "orders": orders
            }
        }

        try:
            self.ws.send(json.dumps(trade_records_request))
            response = json.loads(self.ws.recv())
            if response.get("status"):
                trade_records = response.get("returnData", [])
                logger.info(f"Retrieved trade records: {trade_records}")
                return trade_records[0]
            else:
                logger.error(f"Error retrieving trade records: {response}")
                return None
        except Exception as e:
            logger.error(f"Error during trade record retrieval: {e}")
            raise



# Example usage for testing
if __name__ == "__main__":
    # Testing invalid credentials
    #BAD_PASSWORD = "badPassword"
    #bad_api_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, BAD_PASSWORD)
    #try:
        #logger.info("Testing invalid credentials.")
        ##bad_api_client.connect()
        ##bad_api_client.login()
    #except Exception as e:
        #logger.error(f"Error during invalid credentials test: {e}")

    # Testing valid credentials
    ws_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    try:
        ws_client.connect()
        ws_client.login()

        tradable = ws_client.is_symbol_tradable("AMZN.US_4")
        logger.info(f"Data: {tradable}")

        symbol_data = ws_client.get_symbol_data("TSLA.US_4")
        logger.info(f"Data: {symbol_data}")

        #currency_pairs = ws_client.get_all_currency_pairs()
        #logger.info(f"Currency Pairs: {currency_pairs}")

        all_symbols = ws_client.get_all_symbols()
        #categories = set(symbol.get('categoryName') for symbol in all_symbols)
        #logger.info(f"categories: {categories}")

        #symbols = ws_client.get_all_symbols()
        #US_4_symbols = [symbol["symbol"] for symbol in symbols if symbol.get('symbol', '').endswith('.US_4')]
        #logger.info(f"found {len(US_4_symbols)} symbols: {US_4_symbols}") #1250 sybols

        # indices_symbols = get_symbols_by_type(all_symbols, "IND")

        symbols = ws_client.get_all_symbols()
        #filtered_symbols = [symbol for symbol in symbols if symbol["groupName"] == "France"]
        #logger.info(f"found {len(filtered_symbols)} symbols: {filtered_symbols}") #X sybols


        #french stocks = danone 'BN.FR_4', Michelin ML, orange ORA.FR_4
        search_query = "tesla"
        logger.info(f"Looking for {search_query}:")
        found_symbols = [
        # symbol["symbol"] for symbol in symbols if search_query.lower() in symbol['description'].lower()
        symbol for symbol in symbols if search_query.lower() in symbol['description'].lower()
        ]
        logger.info(f"Looking for {search_query}: {found_symbols}")

        logger.info("DONE")
    except Exception as e:
        logger.error(f"{app_name}: An error occurred: {e}")
    finally:
        ws_client.logout()
