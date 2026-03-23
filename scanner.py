import yfinance as yf
import pandas as pd
import requests

def run_scanner():
    # Professional Headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    })

    tickers = ["RELIANCE.NS", "TCS.NS", "BHARTIARTL.NS", "SBIN.NS", "ICICIBANK.NS", "INFY.NS", "TATAMOTORS.NS"]
    
    results = []
    for ticker in tickers:
        try:
            df = yf.download(ticker, period="5d", interval="1d", progress=False, session=session)
            if df.empty or len(df) < 2: continue
            
            # Flatten columns for newer yfinance versions
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            prev_day = df.iloc[-2]
            curr_day = df.iloc[-1]

            if curr_day['Close'] > prev_day['High'] and curr_day['Volume'] > prev_day['Volume']:
                results.append(f"🚀 {ticker}: BUY @ {curr_day['Close']:.2f}")
        except Exception as e:
            print(f"Error scanning {ticker}: {e}")

    if results:
        print("\n".join(results))
    else:
        print("No BTST signals found today.")

if __name__ == "__main__":
    run_scanner()
