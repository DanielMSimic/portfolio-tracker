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



