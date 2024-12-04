#src/trading/trading_logic
from datetime import datetime
from config.logger import setup_logger
import pandas as pd
from config.logger import setup_logger
from src.api.xtb_api import XTBApiClient
from src.api.xtb_api_utils import XtbApiUtils, ms_to_time_object, ms_to_datetime

from dotenv import load_dotenv
import os
load_dotenv()

# configuration for testing
DEMO_URL = os.getenv("DEMO_URL")
DEMO_STREAM_URL = os.getenv("DEMO_STREAM_URL")
DEMO_USER_ID = os.getenv("DEMO_USER_ID")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")

def main():
    # Testing valid credentials
    ws_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    try:
        ws_client.connect()
        ws_client.login()

        # Check if the symbol is tradable today
        is_tradable = ws_client.is_symbol_tradable() #USDCLP #

        if is_tradable:
            logger.info("Market is open. Proceeding with trading logic...")
            # Add your trading logic here
        else:
            logger.info("Market is closed. No trading action performed.")
            # call error here

        # GET TIMES
        #server_time_ms = ws_client.get_server_time()

        ##ms_to_time_object or XtbApiUtils.ms_to_datetime(server_time_ms)
        #remote_daytime = ms_to_datetime(server_time_ms)
        #server_day=remote_daytime.isoweekday()

        #trading_hours = ws_client.get_trading_hours("USDCLP")
        #logger.debug(f"HOURS={trading_hours}")

        # GET start_time_ms AND end_time_ms OF TODAY
        #start_time_ms = trading_hours.get()
        #end_time_ms=

        #is_tradable = XtbApiUtils.is_symbol_tradable(trading_hours, server_day, server_time_ms)

        # VERIFY MARKET
        #is_market_open = check_market_status(server_time_ms, start_time_ms, end_time_ms)
        #print(f"Market Open: {is_market_open}")


        #ENTER TRADE
        #VERIFY ENTRY

    except Exception as e:
        logger.error(f"Trading Logic ERROR: {e}")
    finally:
        ws_client.logout()
        logger.info("Trading logic completed.")


def check_market_status(server_time_ms: int, start_time_ms: int, end_time_ms: int) -> bool:
    """
    Args:
        server_time_ms (int): Current server time in milliseconds since midnight.
        start_time_ms (int): Trading start time in milliseconds since midnight.
        end_time_ms (int): Trading end time in milliseconds since midnight.
    Returns:
        bool: True if the server time is within trading hours, False otherwise.
    """
    # Convert server time and trading hours to time objects
    server_time_obj = ms_to_time_object(server_time_ms)
    start_time_obj = ms_to_time_object(start_time_ms)
    end_time_obj = ms_to_time_object(end_time_ms)

    logger.info(f"Server Time: {server_time_obj}")
    logger.info(f"Trading Hours: From {start_time_obj} to {end_time_obj}")

    if start_time_obj <= server_time_obj <= end_time_obj:
        print(f"Server time {server_time_obj} is within trading hours.")
        return True

    print(f"Server time {server_time_obj} is outside trading hours.")
    return False

if __name__ == "__main__":
    logger = setup_logger("trading_logic")
    logger.info("TESTING trading_logic.py")
    main()