import time
from datetime import datetime
import json

from config.logger import setup_logger

# Initialize logger
logger = setup_logger("xtb_api_utils")

def get_time() -> int:
    """
    Description: Get the current local time as a timestamp in milliseconds.
    Use: (future) time calculations or logging execution time.
    """
    return int(time.time() * 1000)

def ms_to_datetime(ms: int) -> datetime:
    """
    Description: Format milliseconds to datetime.
    Use: logs and debugs ? - [ ]
    """
    return datetime.fromtimestamp(ms / 1000.0)

def milliseconds_to_string(ms):
    """Format a datetime object into a readable string."""
    ms_datetime = datetime.fromtimestamp(ms / 1000.0) #ms_datetime
    return ms_datetime.strftime("%Y-%m-%d %H:%M:%S")

def timestamp_to_datetimeISO(timestamp):
    """
    Convert a timestamp (milliseconds since epoch) to an ISO 8601 formatted string.
    Args: timestamp (int): Timestamp in milliseconds.
    Returns: Human-readable datetime in ISO format.
    """
    try:
       dt = datetime.fromtimestamp(timestamp / 1000).isoformat()
       return dt
    except Exception as e:
       logger.error(f"Error converting timestamp {timestamp} to datetime: {e}")
       return None


def calculate_response_time(start_time: int, end_time: int) -> int:
    """Calculate the response time in milliseconds."""
    response_time = end_time - start_time
    logger.info(f"Response time: {response_time} ms")
    return response_time

class XtbApiUtils:

    @staticmethod
    def calculate_response_time(start_time, end_time):
        """
        Calculate the response time for a request.

        Args:
            start_time (int): Start time in milliseconds.
            end_time (int): End time in milliseconds.

        Returns:
            int: Response time in milliseconds.
        """
        response_time = end_time - start_time
        logger.info(f"Response time: {response_time} ms")
        return response_time

    @staticmethod
    def parse_response(response):
        """
        Parse a JSON response and log any errors if present.

        Args:
            response (str): JSON response string.

        Returns:
            dict: Parsed response as a dictionary.
        """
        try:
            response_data = json.loads(response)
            if response_data.get("status"):
                logger.info("Response parsed successfully.")
                return response_data
            else:
                error_code = response_data.get("errorCode", "Unknown")
                logger.warning(f"API Error: {error_code}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {e}")
            return None

    @staticmethod
    def is_symbol_tradable(trading_hours, server_day: int, server_time_ms: int) -> bool:
        """
        Determine if a symbol is tradable based on today's trading hours.
        """
        for period in trading_hours:
            if period["day"] == server_day:
                start_time = period["fromT"]
                end_time = period["toT"]
                if start_time <= server_time_ms < end_time:
                    logger.info(
                        f"Symbol is tradable between {ms_to_time_object(start_time)} and {ms_to_time_object(end_time)}.")
                    return True
        logger.warning("Symbol is not tradable today.")
        return False

    @staticmethod
    def log_request_and_response(request, response):
        """
        Log the request and response for debugging purposes.

        Args:
            request (dict): The request object sent to the API.
            response (dict): The response object received from the API.
        """
        logger.debug(f"Request sent: {json.dumps(request, indent=4)}")
        logger.debug(f"Response received: {json.dumps(response, indent=4)}")


def ms_to_time_object(ms: int) -> time:
    """
    Convert milliseconds from midnight to a time of day in HH:MM:SS format.
    Args:
        ms (int): Milliseconds from midnight.
    Returns:
        str: The time of day in HH:MM:SS format.
    """
    total_seconds = ms // 1000
    hours, remainder = divmod(total_seconds, 3600)  # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute
    # Format the time as HH:MM:SS
    #return f"{hours:02}:{minutes:02}:{seconds:02}"
    return time(hour=hours, minute=minutes, second=seconds)



