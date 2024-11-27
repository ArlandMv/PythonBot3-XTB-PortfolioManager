```plaintext
xtb_bot/
├── logs/                         # Logs directory (subdirectories created by logger dynamically)
│   └── YYYY-MM/                  # Monthly folders for logs
│       └── YY-MM-DD_xtb_api.log  # Daily API log
│       └── YY-MM-DD_trading.log  # Daily Trading log
├── src/                          # Source code
│   ├── api/                      # API-related modules
│   │   ├── xtb_api.py            # Handles WebSocket connection and API interactions
│   │   ├── xtb_api_utils.py      # Helper functions for API data parsing and manipulation
│   ├── trading/                  # Trading-specific modules
│   │   ├── trading_logic.py      # Business logic for trade decisions
│   │   ├── indicators.py         # Custom indicators (e.g., MA200, RSI)
│   ├── automation/               # Automation modules
│   │   ├── schedule_tasks.py     # Scheduling and automation logic
│   ├── utils/                    # General utility modules
│   │   ├── logger.py             # Custom logging setup
│   │   ├── config.py             # Configuration management
│   ├── tests/                    # Unit and integration tests
│       ├── test_api.py           # Tests for API-related functionality
│       ├── test_trading.py       # Tests for trading logic
│   ├── main.py                   # Main entry point for running the bot
├── config/                       # Configuration files
│   ├── xtb_demo_config.json      # Config for demo environment
│   ├── xtb_prod_config.json      # Config for production environment
├── docs/                         # Documentation
│   ├── README.md                 # Overview and setup instructions
│   ├── API_REFERENCE.md          # Documentation for API methods
├── .env                          # Environment variables (e.g., API keys)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── DEV_PLAN.md                   # Development plan and roadmap
```