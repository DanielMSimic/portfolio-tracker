# model.py

import numpy as np
import yfinance as yf

def pull_asset_data(ticker):
    ticker = ticker.upper()
    yf.ticker = yf.Ticker(ticker)
    