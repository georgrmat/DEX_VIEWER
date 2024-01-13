import requests
import pandas as pd
import streamlit as st




token_hex = "0x2cc85b82Ce181bce921dc4c0758CFd37a6BC240A"
token_pls = "0x6753560538ECa67617A9Ce605178F788bE7E524E"
token_plsx = "0xf9FD52Ea7326c4FfD0391a233a96C7fE890C7eb8"

st.sidebar.title("Parameters")
crypto = st.sidebar.radio("I have", ["HEX", "PLS", "PLSX"])
nombre = st.sidebar.number_input("Number", value = 100000)


tokens = {"HEX": token_hex,
          "PLS": token_pls,
          "PLSX": token_plsx}

token_prices = {}

launch_button = st.sidebar.button("Launch")

if launch_button:
    for pair in tokens:
        url = f"https://api.dexscreener.com/latest/dex/pairs/pulsechain/{tokens[pair]}"
        response = requests.get(url)
        price = [response.json()["pairs"][0]["priceUsd"]]
        token_prices[pair] = price
        
    df = pd.DataFrame.from_dict(token_prices, orient = "index")
    df.reset_index(drop = False, inplace = True)
    df.columns = ["token", "priceUSD"]
    
    df["number token"] = df.apply(lambda x: nombre * float(token_prices[crypto][0]) / float(x["priceUSD"]), axis = 1)

    st.dataframe(df, use_container_width=True, hide_index = True)
    st.write("Total value:", nombre * float(token_prices[crypto][0]), "$")
    

    

