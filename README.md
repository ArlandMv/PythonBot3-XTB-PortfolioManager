# PythonBot3-XTB-PortfolioManager
⚡ **Automates portfolio management and live tracking via XTB API.**
Logs data locally for transparency and enables holding strategy optimization for long-term traders.

---

## **Features**

- ✅ **Portfolio Monitoring**:
  - Logs account balance, equity, and open positions every 15 minutes for real-time tracking and audit purposes.
- 💰 **Automated ETF Purchase**:
  - Executes a $100 buy order for the S&P 500 ETF every Friday.
- 📂 **Logging**:
  - Saves relevant portfolio and trade data to local log files for easy transparency and analysis.
- 🛠️ **Extendable Framework**:
  - Easily customizable for additional features such as advanced trade strategies or integration with other APIs.

---

## **Getting Started**

### **XTB API Requirements**

To use the XTB API, ensure you meet the following requirements:

1. **XTB Trading Account**:
   - Register for a live or demo account on the [XTB Platform](https://www.xtb.com/).

2. **API Credentials**:
   - Obtain your XTB API credentials (username and password) from the client area.

3. **WebSocket Support**:
   - Ensure your development environment supports WebSocket communication, as the XTB API uses WebSocket for real-time data streaming.
   - Python 3.10.4

4. **API Documentation**:
   - Familiarize yourself with the [official XTB API documentation](http://developers.xstore.pro/documentation). This provides details on endpoints, data structures, and usage limits.

5. **API Limits**:
   - Be mindful of XTB's rate limits for API requests to avoid connection issues or bans. Handle API errors gracefully in your code.


### **Project Prerequisites**
0. **Verify Python**:
   ```bash
   python --version 
   ```
// add verify python version
1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **XTB Account**:
   - Sign up for an XTB demo or live account to obtain API credentials.
3. **Directory Structure**:
   Ensure the following file structure:
   ```
   PythonBot3-XTB-PortfolioManager/
   │
   ├── logs/
   │   └── .gitkeep
   ├── src/
   │   ├── __init__.py
   │   ├── main.py
   │   └── log_config.py
   ├── tests/
   │   ├── __init__.py
   │   └── test_main.py
   ├── .gitignore
   ├── README.md
   └── DEV_PLAN.md

   ```
---


### **Setup and Configuration**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PythonBot3-XTB-PortfolioManager.git
   cd PythonBot3-XTB-PortfolioManager
   ```
2. Update `xtb_api.py`:
   - Replace `your_username` and `your_password` with your XTB API credentials.

3. Run the application:
   ```bash
   python main.py
   ```

---

## **How It Works**

### **1. Portfolio Monitoring**

Every 15 minutes, the app:
- Retrieves portfolio data (balance, equity, open positions).
- Logs the data to `logs/actions.log`.

### **2. Automated ETF Purchase**

Every Friday at 3:00 PM (server time), the app:
- Executes a $100 buy order for the S&P 500 ETF.
- Logs the action to `logs/actions.log`.

### **3. Portfolio Data Logging**

Portfolio data is stored in a structured log file, which can be used for:
- Real-time monitoring.
- Historical analysis and strategy optimization.

---

## **Folder Structure**

```
PythonBot3-XTB-PortfolioManager/
├── main.py              # Main script to schedule tasks
├── xtb_api.py           # XTB API interaction logic
├── logs/
│   └── actions.log      # Log file for portfolio and trade actions
```

---

## **Extending the App**

### **Add Email Alerts**
Integrate email notifications for trade confirmations or portfolio updates using Python's `smtplib`.

### **Database Integration**
Use SQLite or a cloud database to persist portfolio snapshots:
```python
import sqlite3

# Initialize Database
conn = sqlite3.connect("portfolio.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        timestamp TEXT,
        balance REAL,
        equity REAL
    )
""")
```

### **Backtesting Framework**
Export portfolio logs to CSV for backtesting with tools like **Backtrader** or **pandas**.

---

## **FAQ**

### **1. What is the frequency of portfolio updates?**
The app updates portfolio data every 15 minutes. This interval can be adjusted in `main.py`.

### **2. Can I customize the buy amount or symbol?**
Yes! Modify the `buy_etf` function in `xtb_api.py` to adjust the amount or symbol.

### **3. How do I handle API rate limits?**
Ensure that your API requests are within XTB's limits. Use error handling and retry logic for WebSocket connections.

---

## **Contributing**

Feel free to fork this repository and submit pull requests for additional features or improvements. Contributions are welcome! 🙌

---

## **License**

This project is licensed under the MIT License.

---

## **Contact**

For questions or support:
- 📧 Email: [arlandmichelenav@gmail.com](mailto:arlandmichelenav@gmail.com)
- 🔗 GitHub: [ArlandMv](https://github.com/ArlandMv)

---

### **Happy Automating! 🚀**
```

---

### **Summary of Changes**:
- Updated the **project name** to `PythonBot3-XTB-PortfolioManager`.
- Adjusted the **description** to reflect its new emphasis on "holding strategy optimization."
- Ensured consistent use of the updated name throughout the README.
- Enhanced clarity and alignment with long-term trading strategies.

Let me know if further tweaks are needed! 😊