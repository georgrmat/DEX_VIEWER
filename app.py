import requests
import pandas as pd
import streamlit as st
import time
import json

# Load token addresses from a file
with open("data/token_adresses.txt", "r") as f:
    tokens_str = f.read()

# Parse JSON data from the file
tokens = json.loads(tokens_str)

# Streamlit app setup
st.title("PulseChain DEX Viewer")
st.sidebar.title("Parameters")
crypto = st.sidebar.radio("I have", ["HEX", "PLS", "PLSX"])
nombre = st.sidebar.number_input("Number of tokens", value=100000)

token_prices = {}
token_changes = {}

# Button to trigger data retrieval and analysis
launch_button = st.sidebar.button("Launch")

# Function to determine background color based on percentage change
def bgcolor_positive_or_negative(value):
    bgcolor = "#b1532d" if float(value.replace("%", "")) < 0 else "lightgreen"
    return f"background-color: {bgcolor}; opacity: 0.1"

# Execute when the Launch button is clicked
if launch_button:
    # Retrieve data for each token pair
    for pair in tokens:
        url = f"https://api.dexscreener.com/latest/dex/pairs/pulsechain/{tokens[pair]}"
        response = requests.get(url)
        
        # Extract price and price change information
        price = [response.json()["pairs"][0]["priceUsd"]]
        token_prices[pair] = price
        token_changes[pair] = response.json()["pairs"][0]["priceChange"]

    # Display variations in a DataFrame
    st.header("Variations")
    st.markdown(
        "This section shows the variations in token prices over different timeframes. "
        "The data is displayed in a DataFrame with columns for different timeframes (m5, h1, h6, h24)."
    )

    df_change = pd.DataFrame(token_changes).T
    df_change.reset_index(drop=False, inplace=True, names=["Token"])

    # Format percentage columns
    for column in ["m5", "h1", "h6", "h24"]:
        df_change[column] = df_change[column].apply(lambda x: str(x) + "%")

    # Apply styling to the DataFrame
    styled_df_change = df_change.style.applymap(bgcolor_positive_or_negative, subset=["m5", "h1", "h6", "h24"])
    st.dataframe(styled_df_change, use_container_width=True, hide_index=True)

    # Display number of tokens and prices in a DataFrame
    st.header("Number of tokens and prices")
    st.markdown(
        "This section displays the number of tokens and their corresponding prices. "
        "The data is presented in a DataFrame with columns for the token name, "
        "the price in USD, and the calculated number of tokens based on user input."
    )

    df_tokens = pd.DataFrame.from_dict(token_prices, orient="index")
    df_tokens.reset_index(drop=False, inplace=True)
    df_tokens.columns = ["Token", "PriceUSD"]

    # Calculate number of tokens and total value
    df_tokens["NumberOfTokens"] = df_tokens.apply(lambda x: nombre * float(token_prices[crypto][0]) / float(x["PriceUSD"]), axis=1)
    st.dataframe(df_tokens, use_container_width=True, hide_index=True)
    st.write("Total value:", nombre * float(token_prices[crypto][0]), "$")
