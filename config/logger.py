import os
import logging
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def setup_logger(name, log_dir="logs", level=logging.INFO):
    """
    Sets up a logger with daily log files stored in monthly directories.

    Args:
        name (str): The name of the logger (e.g., "xtb_api", "trading").
        log_dir (str): The base directory for logs.
        level (int): Logging level (e.g., logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    #project_root = os.path.dirname(os.path.abspath(__file__))

    # Get the absolute path to the logs directory at the root of the project
    log_dir = os.path.join(PROJECT_ROOT, "..", log_dir)
    log_dir = os.path.abspath(log_dir)  # Ensure it's an absolute path

    # Get current date and build directory/file structure
    now = datetime.now()
    month_dir = now.strftime("%Y-%m")  # e.g., %m"2024-11"
    day_file = now.strftime("%y-%m-%d")  # e.g., "24-11-26"

    log_path = os.path.join(log_dir, month_dir)
    os.makedirs(log_path, exist_ok=True)

    log_file = os.path.join(log_path, f"{day_file}_{name.lower()}.log")

    # Set up the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Stream handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
