# Portfolio Tracker CLI [a.s.r Werkstudent Python Project]

## Description
Command-line Interface application that tracks an investment portfolio.

## Commands

add: add an asset to the portfolio. You will be prompted for ticker, quantity, and purchase price per unit
	portfolio >> add
	Enter ticker: AAPL
	Enter quantity purchased: 100
	Enter purchase price per unit: 260

	The CLI will ask you to confirm (y/n) your entry. If (y), the CLI will return a brief confirmation that your asset has been added to the portfolio. 

view: view current portfolio. If empty, you will be asked to add an asset or referred to 'help' for more information.
	portfolio >> show

remove: remove an asset from the current portfolio. Note, this removes ALL entries for the given ticker. In case the same ticker was added multiple times, this command removes all matching ticker entries. 
	portfolio >> remove
	Enter ticker of the asset you would like to remove ALL positions for. This action cannot be undone: AAPL
	Remove all AAPL positions? (Y/n)
	Removed AAPL from portfolio.

help: open the help section to view available commands. [ALSO STILL NEED TO PIMP THIS A BIT]
	portfolio >> help

## Notes
- Uses Yahoo Finance (yfinance) to fetch asset data for added tickers
- Tickers (for now) must match Yahoo Finance format (e.g. ASRNL.AS, AAPL, MSFT, NN.AS)

## Run
python main.py