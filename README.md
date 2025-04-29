
Built by https://www.blackbox.ai

---

```markdown
# Future MT5 Trading Platform

## Project Overview
Future MT5 is a trading platform designed for automated trading using the MetaTrader 5 (MT5) trading terminal. The software employs a trading strategy that utilizes various indicators, allowing users to define their trading parameters. The interface is built with a modern design using `tkinter`, providing an easy-to-use control panel for setting assets, timeframes, and lot sizes.

## Installation

To run the Future MT5 project, ensure you have Python 3.7 or higher installed. Follow the steps below for installation:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/future-mt5.git
   cd future-mt5
   ```

2. **Install the required packages:**
   Use `pip` to install necessary packages. Ensure you have `MetaTrader5`, `numpy`, and `pandas` installed:
   ```bash
   pip install MetaTrader5 numpy pandas
   ```

3. **Run the application:**
   Use the main script to start the application:
   ```bash
   python main.py
   ```

**Note:** You must have the MetaTrader 5 terminal properly installed and a trading account configured.

## Usage

1. **Login:** Start by entering your MT5 server, login, and password in the login screen that appears.
2. **Select Assets:** Choose up to 4 trading assets to monitor and analyze.
3. **Set Timeframe:** Specify the timeframe for the trading strategy (options include M1, M5, M15, M30, H1, H4, D1).
4. **Lot Size:** Define the lot size for your trades.
5. **Start Trading:** Click the "Start Bot" button to activate the strategy and begin trading based on the defined parameters.
6. **Monitor Logs:** Observe trading signals and logs for each selected asset in the log sections displayed in the interface.

## Features

- **Multi-Asset Trading:** Allow trading of multiple assets simultaneously.
- **Customizable Parameters:** Users can configure strategy parameters like RSI, MACD, EMA, Bollinger Bands, etc.
- **User-Friendly Interface:** Easy-to-navigate GUI for managing trades, viewing logs, and monitoring balance.
- **Real-Time Updates:** Dynamic logging of trading signals and market data.
- **Theming Options:** Toggle between dark and light themes for better visibility.

## Dependencies

The project has the following dependencies listed in the `requirements.txt`:

- `MetaTrader5`
- `numpy`
- `pandas`
- `tkinter` (part of the standard library for Python)

You can create a `requirements.txt` file for this project as follows:
```
MetaTrader5
numpy
pandas
```

## Project Structure

```plaintext
future-mt5/
├── main.py               # Entry point of the application
├── login.py              # User authentication interface
├── painel.py             # Main trading dashboard interface
├── estrategia.py         # Trading strategy logic
├── log_system.py         # Logging system for tracking trades and signals
├── splash_screen.py      # Splash screen displayed on startup
├── utils.py              # Utility functions for login and MT5 connection
└── README.md             # Project documentation
```

Each component of the project is organized into specific files to maintain a clean architecture and modularity.

## License

This project is licensed under the MIT License. Feel free to modify and use as you see fit!

## Contributions

Contributions are welcome! Please submit a pull request or open an issue for discussions.
```

### Note:
Change the git clone URL in the Installation section to your repository URL if this is hosted on a platform like GitHub or Bitbucket, and you can adjust the license section as necessary.