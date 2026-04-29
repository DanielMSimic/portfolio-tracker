# view.py

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def print_asset_added(asset):
    print(f"{asset['ticker']} added to portfolio.")

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
    
        if hist.empty:
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



