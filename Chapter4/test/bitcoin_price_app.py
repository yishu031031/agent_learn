import streamlit as st
import requests
import datetime

def fetch_bitcoin_data():
    """Fetches the current price and 24h price change of Bitcoin from CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["bitcoin"]["usd"], data["bitcoin"]["usd_24h_change"]
    except requests.Timeout:
        st.error("Request timed out. Please try again later.")
        return None, None
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None, None

def main():
    st.title("Bitcoin Price Tracker")

    # Add a refresh button at the top
    if st.button("Refresh Price"):
        st.experimental_rerun()

    # Fetch Bitcoin data
    with st.spinner("Fetching Bitcoin price..."):
        current_price, price_change_24h = fetch_bitcoin_data()

    if current_price is not None:
        # Display current price
        st.metric("Current Bitcoin Price (USD)", f"${current_price:,.2f}")

        # Display price change information
        change_amount = current_price * (price_change_24h / 100)
        st.metric("24h Change", f"{price_change_24h:.2f}%", f"${change_amount:,.2f}")

        # Log the last update time
        st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
       st.warning("Unable to display Bitcoin data at the moment. Please try refreshing the page.")

if __name__ == "__main__":
    main()