#from utils.logger import setup_logger
from config.logger import setup_logger



def main():
    # Set up loggers
    api_logger = setup_logger("xtb_api", log_dir="logs")
    trading_logger = setup_logger("trading", log_dir="logs")

    # Log some test messages
    api_logger.info("XTB API Logger initialized.")
    api_logger.error("Test error message from XTB API.")

    trading_logger.debug("Debugging trading logic.")
    trading_logger.warning("Trading warning message.")


if __name__ == "__main__":
    main()
