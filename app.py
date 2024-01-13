import requests
import pandas as pd
import streamlit as st
import time
import json

with open("data/token_adresses.txt", "r") as f:
    tokens_str = f.read()
    
tokens = json.loads(tokens_str)


st.title("PulseChain DEX Viewer")
st.sidebar.title("Parameters")
crypto = st.sidebar.radio("I have", ["HEX", "PLS", "PLSX"])
nombre = st.sidebar.number_input("Number of tokens", value = 100000)

token_prices = {}
token_changes = {}

launch_button = st.sidebar.button("Launch")

def bgcolor_positive_or_negative(value):
    bgcolor = "#b1532d" if float(value.replace("%", "")) < 0 else "lightgreen"
    return f"background-color: {bgcolor}; opacity: 0.1"

if launch_button:
    for pair in tokens:
        url = f"https://api.dexscreener.com/latest/dex/pairs/pulsechain/{tokens[pair]}"
        response = requests.get(url)
        price = [response.json()["pairs"][0]["priceUsd"]]
        token_prices[pair] = price
        
        token_changes[pair] = response.json()["pairs"][0]["priceChange"]
        
    st.header("Variations")
    df_change = pd.DataFrame(token_changes).T
    df_change.reset_index(drop = False, inplace = True, names = ["Token"])
    
    for column in ["m5", "h1", "h6", "h24"]:
        df_change[column] = df_change[column].apply(lambda x: str(x) + "%")
    styled_df_change = df_change.style.applymap(bgcolor_positive_or_negative, subset = ["m5", "h1", "h6", "h24"])
    st.dataframe(styled_df_change, use_container_width=True, hide_index = True)
    
    st.header("Number of tokens and prices")
    df_tokens = pd.DataFrame.from_dict(token_prices, orient = "index")
    df_tokens.reset_index(drop = False, inplace = True)
    df_tokens.columns = ["Token", "PriceUSD"]
    df_tokens["NumberOfTokens"] = df_tokens.apply(lambda x: nombre * float(token_prices[crypto][0]) / float(x["PriceUSD"]), axis = 1)
    st.dataframe(df_tokens, use_container_width=True, hide_index = True)
    st.write("Total value:", nombre * float(token_prices[crypto][0]), "$")
