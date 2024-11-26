import os
from datetime import datetime
from configuration import config_logs

def test_logging_setup():
    log_directory = "logs"
    logger = config_logs(log_directory=log_directory)

    # Check if the logger is correctly configured
    assert logger.name == "portfolio_manager_logger"
    assert os.path.exists(log_directory), "Log directory should be created"

    # Simulate a log message and check the console/file
    logger.info("Test log message.")
    log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(log_directory, log_filename)
    assert os.path.exists(log_path), "Log file should exist"


