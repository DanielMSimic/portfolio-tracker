# view.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def print_asset_added(asset):
    print(f"{asset['Ticker']} added to portfolio.")

# PLOTTING SINGLE TICKER
def plot_single_asset(hist, plot_asset, start_date, end_date):
    plt.figure()

    x_values = hist.index
    y_values = hist["Close"]
                
    plt.plot(x_values, y_values, label=plot_asset[0], linewidth=2)
    plt.fill_between(x_values, y_values, alpha=0.1)
    plt.tight_layout()
    plt.title(f"Close price: {plot_asset[0]}", weight='bold')
    #plt.grid()
    plt.ylabel("Closing price")
    plt.legend()

    print()
    print(f"Figure showing plot for: {plot_asset[0]} over the period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")
    plt.show()

# PLOTTING MULTIPLE TICKERS
def plot_multiple_assets(plot_asset, start_date, end_date, get_plot_history):
    plt.figure()
    for asset in plot_asset:
        hist = get_plot_history(asset, start_date, end_date)
    
        if hist is None or hist.empty:
            print(f"No data available for {asset}.")
            continue
                    
        x_values = hist.index
        y_values = hist["Close"] / hist["Close"].iloc[0]
        plt.plot(x_values, y_values, label=asset)
    
    plt.tight_layout()
    #plt.xticks(rotation=45)
    plt.title(f"Normalised price: {', '.join(plot_asset)}", weight='bold')
    plt.ylabel("Normalised closing price")
    #plt.grid()
    plt.legend()

    print()
    print(f"Figure showing plot(s) for: {', '.join(plot_asset)} over the period {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}.")
    plt.show()


def print_sim_results(mu, sigma, mean_predicted_pfval, median_predicted_pfval, percentile_5, percentile_95):
    print(f"\n{'=' * 60}")
    print(f"  Simulation results portfolio value 15 year forecast")
    print(f"     Annualised growth rate (μ):   {mu:.2%} ")
    print(f"     Annualised volatility (σ):    {sigma:.2%} ")
    print(f"{'=' * 60}")
            
    print(f"  Mean predicted portfolio value:      {mean_predicted_pfval:,.2f}")
    print(f"  Median predicted portfolio value:    {median_predicted_pfval:,.2f}")            
    print(f"  5th percentile value at risk (VaR):  {percentile_5:,.2f}")          
    print(f"  95th percentile:                     {percentile_95:,.2f}")   
    print(f"{'=' * 60}")

def plot_sim_paths(T, n_steps, sample_paths):
    # Plotting GBM paths
    time_horizon = np.linspace(0, T, n_steps + 1)
            
    for path in range(100):
        plt.plot(time_horizon, sample_paths[:, path])

    plt.title("Simulated paths of portfolio value over 15 years.")
    plt.xlabel("Years")
    plt.ylabel("Portfolio value (millions)")
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _:f'{x/1_000_000:,.1f}'))
    plt.show()
    
def sim_wait_msg():
    print("Simulating 100,000 GBM paths. This may take some time...")  
    print()

def sim_complete_msg():
    print("Simulation complete. Simulated 100,000 paths x 3,780 days, generating 378 million draws.")

def print_portfolio(portfolio, tot_curr_val, tot_cost, tot_pnl_abs, tot_pnl_pct):
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
                
    print("=" * 254)  # Sets underline bar length kind of naively, manually. Maybe have this be dynamic if time allows
                
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

def print_allocation(tot_sector_val, tot_class_val, tot_curr_val):
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

def help_command():
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

def welcome_msg():
    print()
    print("Welcome. \nThis Portfolio Tracker allows you to view your current portfolio, add assets, and track its performance.")
    print()
    print("Type 'help' for a full list of available commands.")
    print("Type 'exit' to close the application, confirm by (y/n).")

def unknown_command_msg():
    print("Unknown command. Type 'help' for available commands.")

