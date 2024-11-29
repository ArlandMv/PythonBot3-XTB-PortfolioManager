#src/trading/trading_logic
from datetime import datetime

from config.logger import setup_logger
import pandas as pd
from config.logger import setup_logger
from src.api.xtb_api import XTBApiClient
from src.api.xtb_api_utils import XtbApiUtils

# Hardcoded configuration for testing
DEMO_URL = "wss://ws.xtb.com/demo"
DEMO_STREAM_URL = "wss://ws.xtb.com/demoStream"
DEMO_USER_ID = "17101549"  # Replace with your test user ID
DEMO_PASSWORD = "p@5R{(&Wezx;*SFhBX.^b9"  # Replace with your test password

def main():
    # Testing valid credentials
    api_client = XTBApiClient(DEMO_URL, DEMO_STREAM_URL, DEMO_USER_ID, DEMO_PASSWORD)
    try:
        api_client.connect()
        api_client.login()
        # GET TIMES
        server_time_ms = api_client.get_server_time()

        remote_daytime = XtbApiUtils.ms_to_datetime(server_time_ms)
        server_day=remote_daytime.isoweekday()

        trading_hours = api_client.get_trading_hours("USDCLP")
        logger.debug(f"HOURS={trading_hours}")

        # GET start_time_ms AND end_time_ms OF TODAY
        #start_time_ms = trading_hours.get()
        #end_time_ms=

        is_tradable = XtbApiUtils.is_symbol_tradable(trading_hours, server_day, server_time_ms)

        # VERIFY MARKET
        #is_market_open = check_market_status(server_time_ms, start_time_ms, end_time_ms)
        #print(f"Market Open: {is_market_open}")

        # Check if the symbol is tradable today
        is_tradable = XtbApiUtils.is_symbol_tradable(trading_hours, server_day, server_time_ms)
        logger.info(f"Market Open Today: {is_tradable}")

        if is_tradable:
            logger.info("Market is open. Proceeding with trading logic...")
            # Add your trading logic here
        else:
            logger.warning("Market is closed. No trading action performed.")

        #ENTER TRADE
        #VERIFY ENTRY

    except Exception as e:
        logger.error(f"Trading Logic ERROR: {e}")
    finally:
        api_client.logout()
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