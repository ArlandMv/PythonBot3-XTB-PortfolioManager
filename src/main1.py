# src/main1.py
from configuration import config_logs

def main():
    print("printing:-- Starting PortfolioManager --")


if __name__ == "__main__":
    logger = config_logs()
    logger.info("-- Starting PortfolioManager --")
    main()
