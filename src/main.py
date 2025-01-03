#from utils.logger import setup_logger
from config.logger import setup_logger
from src.api.xtb_api import XTBApiClient

from dotenv import load_dotenv
import os
load_dotenv()

# configuration for testing
DEMO_URL = os.getenv("DEMO_URL")
DEMO_STREAM_URL = os.getenv("DEMO_STREAM_URL")
DEMO_USER_ID = os.getenv("DEMO_USER_ID")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")


def main():
    logger.info("--- MAIN START---")

    #BUILD LIST OF SYMBOLS TO WATCH
    symbols = ["TSLA.US_4", "AMZN.US_4", "GOOG.US_4", "AAPL.US_4", "NVDA.US_4", "US100", "US500"]

    # Buy and sell symbol
    # 1- get symbol
    # 2- build info
    # 3- open transaction
    # 4- close transaction
    ws_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    ws_client.connect()
    ws_client.login()
    # "TSLA.US_4", 712533775, VOLUMEN NO VALIDO(MIN=1)
    # "AMZN.US_4", 712533223, VOLUMEN NO VALIDO
    # "GOOG.US_4",
    # "AAPL.US_4",
    # "NVDA.US_4",
    # "US100",
    # "US500"
    try:
        # open_position with ammount or volume ws_client.open_position(symbol="TSLA", amount=100)
        symbol="TSLA.US_4"
        symbol_data = ws_client.get_symbol_data(symbol)



        response = ws_client.open_trade( symbol, volume=1, custom_comment="Opening trade US100")
        logger.info(f"Opened trade for {symbol}: {response}")
        # response = close_trade(order_id=123456789, price=1.2350, volume=0.1)

        #symbol_price= symbol_data.get("bid") # selling 1.04882
        #symbol_price= symbol_data.get("ask") # 1.0509
        #symbol_price= 0

        # buy_order = ws_client.trade_transaction( 0, 0, symbol, symbol_price, "xtest")
        # 'order': 699208863}
        # logger.info(f"TRADE {buy_order}")

        # SELL TRADE  {'order': 699740841} {'order': 699762931}
        #sellingtrade = ws_client.open_trade(symbol, False, volume=0.01, custom_comment="selling test")
        #logger.info(f"TRADE {trade}")

        # CLOSE TRANSACTION
        #closingtrade = ws_client.trade_transaction(0, 0, symbol, symbol_price, "closing test", order=699740841 ,type=2) #INTERNAL ERROR  SE199
        #closingtrade = ws_client.trade_transaction(0, symbol, symbol_price, "closing test", order=699740841, type=2,volume=0.01) #INTERNAL ERROR  SE199
        order_id = 704595929
        closingtrade = ws_client.close_position(order_id=order_id ,volume=0.01)
        logger.info(f"CLOSING TRADE {closingtrade}")

        # Error executing trade transaction: {'status': False, 'errorCode': 'SE199', 'errorDescr': 'Internal error'}
        logger.info("--- MAIN END---")
    except Exception as e:
        logger.error(f"An Exception error occurred: {e}")
    finally:
        ws_client.logout()

if __name__ == "__main__":
    logger = setup_logger("main")
    #logger = setup_logger(__name__)
    main() #test buy and sell
