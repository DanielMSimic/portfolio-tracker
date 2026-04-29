# Portfolio Tracker CLI [a.s.r Werkstudent Python Project]

## Description
Command-line Interface application that tracks an investment portfolio. Add and remove assets, retrieve historical market data, simulate portfolio and analyse performance. 

The application supports:
- Asset tracking by pulling live data from Yahoo Finance.
- Portfolio valuation with profit and loss analysis.
- Allocation breakdown into sectors and asset classes of the assets in the portfolio.
- Historical price retrieval for specified time horizons for valid Yahoo Finance tickers (not limited to assets currently in the portfolio).
- Price plotting for single and multiple assets.
- Monte Carlo simulation forecasting future performance of the portfolio over 15 years under user input drift and volatility, using 100,000 Geometric Brownian Motion (GBM) paths.

## Installation
Clone the Github repository and install dependencies listed in requirements.txt.

```bash
pip install -r requirements.txt
```

## Running application
```bash
python3 main.py
```

## Commands

add: add an asset to the portfolio. You will be prompted for ticker, quantity, and purchase price per unit
	portfolio >> add
	Enter ticker: AAPL
	Enter quantity purchased: 10000
	Enter purchase price per unit: 260

The CLI will ask you to confirm (y/n) your entry. If (y), the CLI will return a brief confirmation that your asset has been added to the portfolio. 

remove: remove an asset from the current portfolio. Note, this removes ALL entries for the given ticker. In case the same ticker was added multiple times, this command removes all matching ticker entries. 
```
portfolio >> remove
Enter ticker of the asset you would like to remove ALL positions for. This action cannot be undone: AAPL
Remove all AAPL positions? (Y/n)
Removed AAPL from portfolio.
```

show: show current portfolio. If empty, you will be asked to add an asset or referred to 'help' for more information. 
Includes:
- Sector
- Asset Class
- Purchased quantity (QTY)
- Buy price (BUY PX)
- Transaction cost (COST)
- Current price (PX)
- Current market value (MKT VAL)
- Weights (WGT)
- Profit and loss (P&L)
- Profit and loss % (P&L%)

```
portfolio >> show
```

allocation: show portfolio value and weights per sector and asset class.
```
portfolio >> allocation
```
    
history: show historical data over a specified time period, for any valid Yahoo Finance ticker. Not limited to assets currently in the portfolio. 
```
portfolio >> history
Enter ticker: ASRNL.AS
Enter start date: 2019-1-1
Enter end date: 2021-1-1
```

plot: plot price data for one or multiple assets over a specified time period.
- Single assets (absolute prices)
- Multiple assets (normalised prices for comparison)
```
portfolio >> plot
Enter ticker(s): ASRNL.AS
Enter start date: 2019-1-1
Enter end date: 2021-1-1
```
    
simulate: Monte-carlo simulation forecasting portfolio performance (15 years, 100k GBM paths). Outputs mean, median, value at risk (VaR) and 95th percentile data for the simulation under specified drift and volatility.
```
portfolio >> simulate
Enter expected annualised return as percentage (5 for 5%): 5
Enter expected annualised volatility as percentage (10 for 10%): 10
```

exit: close the application. 
```
portfolio >> exit
```

help: open the help section to view available commands. 
```
portfolio >> help
```

## Notes
- Uses Yahoo Finance (yfinance) to fetch asset data for added tickers
- Tickers must match Yahoo Finance format (e.g. ASRNL.AS, AAPL, MSFT, NN.AS)

## Architecture
Basic Model-View-Controller (MVC) structure:
    Model: handles data fetching, calculations and simulation
    View: output formatting of printed statements, creation of tables and plots. 
    Controller: handles user inputs.

## Future improvements
- Allow multiple assets entries at the same time.
- Improve table rendering to better accompany scaling in smaller terminals windows.


