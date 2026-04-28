# controller.py

# import datetime

# from model import ()

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
            
        elif command == "add":
            print("ADD COMMAND REACHED")
        
        else:
            print("Unknown command. Type 'help' for available commands.")

