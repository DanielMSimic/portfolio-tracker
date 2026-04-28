# controller.py

import datetime
from model import create_asset, get_history, validate_ticker
from view import print_asset_added

def run_portfolio_CLI():
    portfolio = []

    print("Welcome. \nThis Portfolio Tracker allows you to view your current portfolio, add assets, and track its performance.")
    print("Type 'help' for a full list of available commands.")
    print("Type 'exit' to close the application, confirm by (y/n).")
    
    while True:
        command = input("portfolio >> ").strip().lower()       
        
        # EXIT command.
        if command == "exit":
            confirm_exit = input("Are you sure you want to exit the Portfolio Tracker? (y/n): ").strip().lower()
            if confirm_exit == "y":
                print("Goodbye. Closing application")
                break
            else:
                print("Cancelled exit. Resuming application")

        # HELP command.
        elif command == "help":
            print("\nPortfolio Tracker Help\n" + "-"*55)
            print("""
    add:          
        Add an asset to the current portfolio. 
        Input: >>TICKER -> QTY -> PRICE
        Example: ASRNL.AS -> 10000 -> 60
                
    remove:       
        Remove ALL entries of an asset from the current portfolio. 
        Input: >>TICKER
                     
    show:         
        Show current portfolio.
                            
    allocation:  
        Show portfolio value and weights per sector and asset class. 
                
    history:      
        Show historical information for a specified asset. 
        Input: >>TICKER, >>START DATE, >>END DATE
        Format: yyyy-mm-dd
        Note: START DATE cannot be after END DATE
            
    plot:          
        Plot price data for 1 or multiple assets.
        Input: >>TICKER(S)
        Format: TICKER1 TICKER2 TICKER3, separated by spaces
        Example: ASRNL AAPL GOOG NN.NL
        Note: single TICKER plots absolute prices, multiple TICKERS plots normalised prices. 
                
    simulate:     
        Monte-carlo simulation forecasting portfolio performance (15 years, 100k GBM paths).
        Input: 
            annualised return. E.g. 5 for 5%
            annualised volatility. E.g. 20 for 20
                  
    exit:         
        Close the application.\n
        
            """)
            
        # ADD command.
        elif command == "add":
            ticker_input = input("Enter ticker or 'back' to return: ").strip()
            # Need to start adding 'back' options to navigate the levels of the CLI better...
            if ticker_input.lower() == 'back':
                print("Add asset cancelled")
                continue
            
            Ticker = ticker_input.upper()
            
            qty_purchased_input = input("Enter quantity purchased or 'back' to return: ").strip()
            if qty_purchased_input.lower() == "back":
                print("Add asset cancelled")
                continue

            try:
                qty_purchased = float(qty_purchased_input.replace(",", ""))
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                continue
            
            purchase_price_input = input("Enter purchase price or 'back' to return: ").strip()
            if purchase_price_input.lower() == "back":
                print("Add asset cancelled")
                continue

            try:
                purchase_price = float(purchase_price_input.replace(",", ""))
            except ValueError:
                print("Invalid price. Please enter a number.")
                continue

            try:
                asset = create_asset(Ticker, qty_purchased, purchase_price)
            except Exception:
                print("Error retrieving asset data. Please retry.")
            
            if asset is None:
                print("Current Price not available. Asset not added. Please retry.")
                continue

            name = asset['Name']
            sector = asset['Sector']
            asset_class = asset['Asset Class']

            # BEFORE APPENDING, ASK FOR CONFIRMATION AND SHOW ONCE THE TO-BE ADDED ASSET INFORMATION?
            print(f"Asset {Ticker} ({name}) will be added to the portfolio. \n{Ticker}  |  {sector}  |  {asset_class}  |  {qty_purchased:,.2f}  |  {purchase_price:,.2f}  |")
            confirm_add = input('Please confirm your entry (y/n):' ).strip().lower()
            if confirm_add == "y":
                portfolio.append(asset)
                print(f"Added {name} ({Ticker}) to portfolio.")
            else:
                print(f"Cancelled addition of {name} ({Ticker}) to portfolio.")

                
        # SHOW command. 
        elif command == "show":
            if not portfolio:
                print("Portfolio is empty. Add assets, or see 'help' for more information.")
            else:
                tot_curr_val = sum(asset['Current Value'] for asset in portfolio)             # Sums over all Current Value keys in the Asset dictionary for all assets in the portfolio list. Needed to calculate portfolio weights
                
                # Calculated profit and loss for total portfolio. 
                tot_cost = sum(asset['Transaction Value'] for asset in portfolio)
                tot_pnl_abs = tot_curr_val - tot_cost
                if tot_cost == 0:
                    tot_pnl_pct = 0
                else:
                    tot_pnl_pct = tot_pnl_abs / tot_cost

                # TABLE HEADER (ROW 0) FORMATTING
                print()
                print(
                    f"{'TICKER':<10}  |  "
                    f"{'NAME':<35}  |  "
                    f"{'SECTOR':<23}  |  "
                    f"{'CLASS':<15}  |  "
                    f"{'QTY':>17}  |  "
                    f"{'BUY PX':>12}  |  " 
                    f"{'COST':>19}  |  "
                    f"{'PX':>15}  |  "
                    f"{'MKT VAL':>19}  |  "
                    f"{'WGT':>8}  |  "
                    f"{'P&L':>17}  |  "
                    f"{'P&L %':>8}")
                
                print("=" * 254)                               # Sets underline bar length kind of naively, manually. Maybe have this be dynamic if time allows...
                
                for asset in portfolio:                                                       # Looping over all assets in portfolio list...
                    if tot_curr_val == 0:
                        weight = 0                                                            # Edge case, preventing division by zero. 
                    else:
                        weight =  asset["Current Value"] / tot_curr_val                       # ... accessing the key Current Value, and dividing by TOTAL CURRENT VALUE for all those assets to get the weights of all assets in the portfolio.

                    
                    asset_pnl_abs = asset["Current Value"] - asset['Transaction Value']       # Calculates profit and loss for each asset: absolute difference between (current price - purchase price) * quantity purchased.
                    if asset['Transaction Value'] == 0:                                       # Edge case, preventing division by zero. 
                        asset_pnl_pct = 0
                    else:
                        asset_pnl_pct = asset_pnl_abs / asset['Transaction Value']            # Calculates profit and loss for each asset: percentage increase/decrease. 

                    
                    print(                                                                    # ... and over all asset[KEY] to print.
                        f"{asset['Ticker']:<10}  |  "
                        f"{asset['Name']:<35}  |  "
                        f"{asset['Sector']:<23}  |  "
                        f"{asset['Asset Class']:<15}  |  "
                        f"{asset['Quantity']:>17,.2f}  |  "
                        f"{asset['Purchase Price']:>12,.2f}  |  "
                        f"{asset['Transaction Value']:>19,.2f}  |  "
                        f"{asset['Current Price']:>15,.2f}  |  "
                        f"{asset['Current Value']:>19,.2f}  |  "
                        f"{weight:>8.2%}  |  "
                        f"{asset_pnl_abs:>17,.2f}  |  "
                        f"{asset_pnl_pct:>8.2%}"
                    )
                
                print("-" * 254)
                print()

                print(f"TOTAL COST:                {tot_cost:,.2f}")
                print(f"TOTAL PORTFOLIO VALUE:     {tot_curr_val:,.2f}")
                print(f"TOTAL P&L:                 {tot_pnl_abs:,.2f}")
                print(f"TOTAL P&L %:               {tot_pnl_pct:.2%}")

        
        # ALLOCATION command.
        elif command == "allocation":
            if not portfolio:
                print("Portfolio is empty. Add assets, or see 'help' for more information.")
                continue
            else:
                tot_curr_val = sum(asset['Current Value'] for asset in portfolio)             # Sums over all Current Value keys in the Asset dictionary for all assets in the portfolio list. Same as before. 

            tot_sector_val = {}
            tot_class_val = {}

            for asset in portfolio:
                sector = asset["Sector"]
                asset_class = asset["Asset Class"]
            
                if sector not in tot_sector_val:
                    tot_sector_val[sector] = 0
                
                tot_sector_val[sector] += asset['Current Value']
                    

                if asset_class not in tot_class_val:
                    tot_class_val[asset_class] = 0 

                tot_class_val[asset_class] += asset["Current Value"]


            width = 65
            print()
            print("Allocation by SECTOR".center(width))
            print()
            print(f"{'SECTOR':<30}  |  {'POSITION':>15}  |  {'WEIGHT':>8}  ")
            print(f"{'=' * 65}")
            for sector, value in tot_sector_val.items():
                print(f"{sector:<30}  |  {value:>15,.2f}  |  {value / tot_curr_val:8.2%}")
            print(f"{'-' * 65}")

            print()
            
            print("Allocation by ASSET CLASS".center(width))
            print()
            print(f"{'ASSET CLASS':<30}  |  {'POSITION':>15}  |  {'WEIGHT':>8}  ")
            print(f"{'=' * 65}")
            for asset_class, value in tot_class_val.items():
                print(f"{asset_class:<30}  |  {value:>15,.2f}  |  {value / tot_curr_val:8.2%}")
            print(f"{'-' * 65}")


        # REMOVE command.
        elif command == "remove":
            if not portfolio:
                print("Portfolio is empty. Add an asset first, or see 'help' for more information.")
                continue
            
            remove_asset = input("Enter ticker of the asset you would like to remove ALL positions for. This action cannot be undone: ").strip().upper()

            
            #print(f"Remove all {remove_asset} positions? (y/n)")
            confirm_remove = input(f'Remove all {remove_asset} positions? (y/n)').strip().lower()
            if confirm_remove == "y":
                original_len = len(portfolio)                   # Grabbing length of the list, to check later if something was actually removed.


                portfolio = [asset for asset in portfolio if asset.get("Ticker") != remove_asset]         # Rebuild the list but only with those dictionaries that do not include the TICKER that we want to remove. 
                if len(portfolio) < original_len:                                                         # Grab original number of assets (so not unique) in the portfolio and see if the REMOVE command actually removed an asset.
                    print(f"Removed {remove_asset} from portfolio.")                                      # If it did remove an asset, print the removal confirmation.
                else:
                    print(f"{remove_asset} not found in current portfolio.")                              # If nothing was removed, inform user the asset was not found. 
            else:
                print("Removal cancelled.")
            
        # HISTORY command.
        elif command == "history":
            Ticker = input("Enter ticker: ").strip().upper()
            if not validate_ticker(Ticker):
                print("Unable to retrieve data.")
                continue

            cancel_history = False
            while True:
                user_start_date = input("Enter start date (yyyy-mm-dd) or 'back' to return: ").strip().lower()
                if user_start_date == 'back':
                    cancel_history = True
                    break
                    
                user_end_date = input("Enter end date (yyyy-mm-dd) or 'back' to return: ").strip().lower()
                if user_end_date == 'back':
                    cancel_history = True
                    break
                    
                try:
                    start_date = datetime.datetime.strptime(user_start_date, "%Y-%m-%d")
                    end_date = datetime.datetime.strptime(user_end_date, "%Y-%m-%d")
                    if end_date <= start_date:
                        print("End date cannot be before start date. Please try again.")
                        continue
                    
                    break
                except ValueError:
                    print("Invalid date format. Please try again.")

            if cancel_history:
                print("Asset history cancelled.")
                continue
            
            # Actual historical data pull from YAHOO FIN.
            history = get_history(Ticker, start_date, end_date)

            # Printing time series, with option to print full custom period or just the last 25 rows.
            if history.empty:
                print("No historical data available.")
            else:
                print(f"Retrieved {len(history)} rows.")
                show_all = input("Show full history? Else the 25 most recent entries will be shown. (y/n): ").strip().lower()
                if show_all == "y":
                    print(history[["Open", "High", "Low", "Close", "Volume"]].to_string())
                else:
                    print(history[["Open", "High", "Low", "Close", "Volume"]].tail(25).to_string())

        
        
        else:
            print("Unknown command. Type 'help' for available commands.")

