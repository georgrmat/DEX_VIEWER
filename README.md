# PulseChain DEX Viewer

This Streamlit web application provides a real-time view of variations in token prices on the PulseChain DEX. It fetches data from the Dexscreener API for specified token pairs and displays the information in an interactive dashboard.

## Features

- **Variations Section:** Displays the variations in token prices over different timeframes (m5: 5 minutes, h1: 1 hour, h6: 6 hours, h24: 24 hours) in a styled DataFrame.

- **Number of Tokens and Prices Section:** Shows the number of tokens and their corresponding prices. The data is presented in a DataFrame, including the calculated number of tokens based on user input.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/pulsechain-dex-viewer.git

Navigate to the project directory:

bash
Copy code
cd pulsechain-dex-viewer
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Ensure you have created a file named token_adresses.txt in the data directory, containing the necessary token addresses.

Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open the provided URL in your web browser to interact with the app.

Parameters
I have: Select the cryptocurrency you are interested in (HEX, PLS, PLSX).

Number of tokens: Set the desired number of tokens for calculations.

Click the "Launch" button to retrieve and display real-time data.

Dependencies
streamlit
requests
pandas
Acknowledgements
This app uses data from the Dexscreener API. For more information, visit Dexscreener.

License
This project is licensed under the MIT License.

vbnet
Copy code

Replace placeholders like `your-username` and customize sections as neede
