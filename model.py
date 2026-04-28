import yfinance as yf



def create_asset(Ticker, qty_purchased, purchase_price):
    yf_ticker = yf.Ticker(Ticker)

    info = yf_ticker.info

    name = info.get('shortName', Ticker)

    sector = info.get('sector', "Unknown")

    asset_class = info.get('quoteType', "Unknown")

    transac_val = qty_purchased * purchase_price

    curr_price = (
        info.get('currentPrice')
        or info.get('regularMarketPrice')
        or info.get('navPrice')
        or info.get('previousClose')
    )

    if curr_price is None:
        return None

    curr_val = qty_purchased * curr_price

    asset = {
        'Ticker': Ticker,
        'Name': name,
        'Sector': sector,
        'Asset Class': asset_class,
        'Quantity': qty_purchased,
        'Purchase Price': purchase_price,
        'Transaction Value': transac_val,
        'Current Price': curr_price,
        'Current Value': curr_val,
    }

    return asset