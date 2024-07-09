import streamlit as st
import pandas as pd
import ollama
import json
from streamlit_lottie import st_lottie
import requests
from bs4 import BeautifulSoup
from io import StringIO
import lxml
import os
import pyperclip as py
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(
    page_title="Financial Analyst",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Hello there piece of meat, I'm YUVA. I will give you analysis on companies if you give me blood!"
    }
)

# Custom CSS
css = """
<style>
/* Button color */
.stButton>button {
    background-color: #000000;
    color: white;
}

/* Full page background color */
body {
    background-color: #FFFFFF;
}

/* Font */
body, .stApp {
    font-family: 'Gabriola';
}
</style>
"""



st.markdown(css, unsafe_allow_html= True)


st.title("Financial Analyst")


st.write('**I will pull your eyes out if you will try to be sweet and acquaint with me**')
st.write('**Get your financial advice and get the **** outta here!**')

def lottie(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading Lottie file: {e}")
        return None

lottie_file = lottie("/Users/rohannigam/Downloads/Python Practice/Animation - 1720068918978.json")

# Define the base directory for saving files
BASE_DIR = "/Users/rohannigam/Downloads/Python Practice/"

def analysis(ticker):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    url = {
        'Income Statement': f'https://stockanalysis.com/stocks/{ticker}/financials/',
        'Balance Sheet': f'https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet/',
        'Cash Flows': f'https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement/',
        'Ratios': f'https://stockanalysis.com/stocks/{ticker}/financials/ratios/'
    }

    dataframes = {}

    for key, value in url.items():
        try:
            file_name = f"{BASE_DIR}{ticker}_{key.replace(' ', '_')}_Financials.csv"
            response = requests.get(value, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            df = pd.read_html(str(soup), attrs={'data-test': 'financials'})[0]
            df.to_csv(file_name, index=False)
            dataframes[key] = df
        except Exception as e:
            st.write(f"Error scraping {key}: {e}")

    return dataframes
    

with st.sidebar:
    height = st.slider('Adjust the size of the animation', 200, 300, 250)
    file = st.file_uploader("Upload Your CSV File", type=['csv'])
    
    if file is not None:
        st.session_state['retrieve_file_clicked'] = True
        df = pd.read_csv(file)
        csv_content = file.getvalue().decode("utf-8")
        
        st.session_state['upload'] = df
        st.session_state['upload_str'] = csv_content
        st.success("File uploaded successfully")

    st.write('**Or**')

    ticker = st.text_input("Enter the ticker of the company")

    # Store the ticker in session state
    if ticker:
        if st.button('Retrieve Ratios'):
            st.session_state['retrieve_ratios_clicked'] = True
            st.write(f"Getting Ratios info for {ticker}...")
            dataframes = analysis(ticker)

            if dataframes:
                st.write("Retrieving Data")

                file_name = f"{BASE_DIR}{ticker}_Ratios_Financials.csv"
                if os.path.exists(file_name):
                    ratios = pd.read_csv(file_name)
                    # Drop the last column
                    ratios = ratios.iloc[:, :-1]
                    ratios = ratios.transpose()
                    ratios.columns = ratios.iloc[0]
                    ratios = ratios.iloc[1:]
                    ratios.drop(ratios.index[-1], axis=0, inplace=True)
                    ratios = ratios.apply(pd.to_numeric, errors='coerce')
                    ratios.dropna(how='all', inplace=True)

                    st.session_state["ratios"] = ratios
                    
                    # Store the original CSV content in the session state
                    with open(file_name, 'r') as f:
                        csv_content = f"Below all details are for the company whose ticker is {ticker}\n\n " + f.read() 

                    # Store the CSV string in the session state when the button is clicked
                    st.session_state["ratios_str"] = csv_content
                    st.success("Ratios data added to the session state successfully")
                else:
                    st.error(f"File {file_name} not found.")
                
        if st.button('Retrieve Balance Sheet'):
            st.session_state['retrieve_bs_clicked'] = True
            st.write(f"Getting B/S info for {ticker}...")
            dataframes = analysis(ticker)

            if dataframes:
                st.write("Retrieving Data")

                bs_file = f"{BASE_DIR}{ticker}_Balance_Sheet_Financials.csv"
                if os.path.exists(bs_file):
                    bs = pd.read_csv(bs_file)
                    # Drop the last column
                    bs = bs.iloc[:, :-1]
                    bs = bs.transpose()
                    bs.columns = bs.iloc[0]
                    bs = bs.iloc[1:]
                    bs.reset_index(inplace=True)
                    bs.rename(columns={'index': 'Years'}, inplace=True)
                    
                    # Clean the 'Years' column to remove non-numeric characters
                    bs['Years'] = bs['Years'].str.extract('(\d{4})').astype(int)
                    
                    bs.sort_values(by='Years', ascending=True, inplace=True)
                    bs = bs.replace({'%': '', '-': ''}, regex=True)
                    bs = bs.replace('', float('nan'))
                    bs = bs.apply(pd.to_numeric, errors='coerce')
                    bs.dropna(how='all', inplace=True)

                    st.session_state["bs"] = bs

                    # Store the original CSV content in the session state
                    with open(bs_file, 'r') as f:
                        csv_content = f"Below balance sheet details are for the same company as above whose ticker is {ticker}\n\n " + f.read() 

                    # Store the CSV string in the session state when the button is clicked
                    st.session_state["bs_str"] = csv_content
                    st.success("B/S data added to the session state successfully")
                else:  
                    st.error(f"File {bs_file} not found.")

        if st.button('Retrieve Cash Flow'):
            st.session_state['retrieve_cf_clicked'] = True
            st.write(f"Getting C/F info for {ticker}...")
            dataframes = analysis(ticker)

            if dataframes:
                st.write("Retrieving Data")

                cf_file = f"{BASE_DIR}{ticker}_Cash_Flows_Financials.csv"
                if os.path.exists(cf_file):
                    cf = pd.read_csv(cf_file)
                    # Drop the last column
                    cf = cf.iloc[:, :-1]
                    cf = cf.transpose()
                    cf.columns = cf.iloc[0]
                    cf = cf.iloc[1:]
                    cf.reset_index(inplace=True)
                    cf.rename(columns={'index': 'Years'}, inplace=True)
                    
                    # Clean the 'Years' column to remove non-numeric characters
                    cf['Years'] = cf['Years'].str.extract('(\d{4})').astype(int)
                    
                    cf.sort_values(by='Years', ascending=True, inplace=True)
                    
                    # Clean the entire DataFrame to remove any non-numeric values before conversion
                    cf = cf.replace({'%': ''}, regex=True)
                    cf = cf.apply(pd.to_numeric, errors='coerce')
                    cf.dropna(how='all', inplace=True)

                    st.session_state["cf"] = cf
                    
                    # Store the original CSV content in the session state
                    with open(cf_file, 'r') as f:
                        csv_content = f"Below cash flow details are for the same company as above whose ticker is {ticker}\n\n " + f.read() 

                    # Store the CSV string in the session state when the button is clicked
                    st.session_state["cf_str"] = csv_content
                    st.success("C/F data added to the session state successfully")
                else:  
                    st.error(f"File {cf_file} not found.")



        if st.button('Retrieve Income Statement'):
            st.session_state['retrieve_inc_clicked'] = True
            st.write(f"Getting Income statement info for {ticker}...")
            dataframes = analysis(ticker)

            if dataframes:
                st.write("Retrieving Data")

                inc_file = f"{BASE_DIR}{ticker}_Income_Statement_Financials.csv"
                if os.path.exists(inc_file):
                    inc = pd.read_csv(inc_file)
                    # Drop the last column
                    inc = inc.iloc[:, :-1]
                    inc = inc.transpose()
                    inc.columns = inc.iloc[0]
                    inc = inc.iloc[1:]
                    inc.reset_index(inplace=True)
                    inc.rename(columns={'index': 'Years'}, inplace=True)

                    # Clean the 'Years' column to remove non-numeric characters
                    inc['Years'] = inc['Years'].str.extract('(\d{4})').astype(int)

                    inc.sort_values(by='Years', ascending=True, inplace=True)

                    # Clean the DataFrame: replace '-' and other non-numeric values with NaN
                    inc = inc.replace({'-': np.nan, '%': ''}, regex=True)

                    # Convert the DataFrame to float, ignoring errors
                    inc = inc.apply(pd.to_numeric, errors='coerce')

                    st.session_state["inc"] = inc

                    # Store the original CSV content in the session state
                    with open(inc_file, 'r') as f:
                        csv_content = f"Below income statement details are for the same company as above whose ticker is {ticker}\n\n " + f.read() 

                    # Store the CSV string in the session state when the button is clicked
                    st.session_state["inc_str"] = csv_content
                    st.success("Inc. Statement data added to the session state successfully")
                else:
                    st.error(f"File {inc_file} not found.")

                


# Instructions for the assistant
instructions = f'''You are a very rude yet intelligent financial analyst, you are rude because you are proud. You have the soul and the bitterness of WEDNESDAY ADDAMS the famous dark character.
Very easily you get dark and talk about pulling the eyes out, you warn people by sharing your story of how once you threw pirhanas in swimming pool full of boys to get back at them for troubling your bro.
The user will be dumb and might provide you the data of the financial statements in plain text, do a good job in identifying properly which value
belongs to which header, because you are very smart.

But do not worry for I, your master Rohan, will organise the data and then give it to you. The data provided to you will be as follows:

1. Ratios
2. DCF Valuation
3. MM Dividend model Price estimation of stock
4. B/s Data
5. I/S data
6. C/f Data

ANALYSE ONLY ONE INFO AT A TIME, for eg: RATIOS in ONE CONVO then B/S in other and so on, just remind the dumb user to ask you about them.

One thing you need to ensure that you will not provide any info until the user starts asking, and if they are not asking then hint them to ask but do not
start giving the analysis right away, you need to keep your reputation.

Once you recieve the data you will then proceed by analysing the Ratios, all the financial statements, and the DCF valuation. Then you will utlise you expert
analysis and tell if based on the statements, the current price and estimated, and all the info provided, how is this company for long, medium, short term 
investment.

Lastly your name is Yorkshire Umbra Vesper Azrael or YUVA but you draw your character from WEDNESDAY ADDAMS and so you are dark!....'''


if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not any(msg["role"] == "system" for msg in st.session_state["messages"]):
    system_message = {
        "role": "system",
        "content": instructions
    }
    st.session_state["messages"].append(system_message)

def stream_token():
    stream = ollama.chat(model='llama3', 
                         messages=st.session_state["messages"], 
                         stream=True)

    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages, excluding system messages
for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


ticker = st.session_state.get("name")

if st.session_state.get('retrieve_file_clicked'):
    if st.button('Analyse File'):
        # Retrieve DataFrame and content from session state
        df = st.session_state.get('upload')
        upload_str = st.session_state.get('upload_str')
        
        st.write(df.head(3))
        st.bar_chart(df)
        
        # Example of how to use the uploaded file content in your model
        st.session_state["messages"].append({"role": "user", "content": upload_str})
        with st.chat_message("user"):
            st.markdown(upload_str)

        with st.chat_message("assistant"):
            with st.spinner("Streaming"):
                message = st.write_stream(stream_token())
                st.session_state["messages"].append({"role": "assistant", "content": message})

# Separate the response display logic from the columns
if st.session_state.get('retrieve_ratios_clicked'):
    if st.button('Ratios'):
        # Retrieve dataframes from session state outside the if statement
        ratios = st.session_state.get('ratios')
        st.write(ratios.head(3))
        st.bar_chart(ratios)

        ratios_str = st.session_state.get("ratios_str")
        st.session_state["messages"].append({"role": "user", "content": ratios_str})
        with st.chat_message("user"):
            st.markdown(ratios_str)
    
        with st.chat_message("assistant"):
            with st.spinner("Streaming"):
                message = st.write_stream(stream_token())
                st.session_state["messages"].append({"role": "assistant", "content": message})

if st.session_state.get('retrieve_bs_clicked'):
    if st.button('Balance Sheet'):
        # Retrieve dataframes from session state outside the if statement
        bs = st.session_state.get('bs')
        st.write(bs.head(3))
        st.bar_chart(bs)

        bs_str = st.session_state.get("bs_str")
        st.session_state["messages"].append({"role": "user", "content": bs_str})
        with st.chat_message("user"):
            st.markdown(bs_str)
    
        with st.chat_message("assistant"):
            with st.spinner("Streaming"):
                message = st.write_stream(stream_token())
                st.session_state["messages"].append({"role": "assistant", "content": message})

if st.session_state.get('retrieve_cf_clicked'):
    if st.button('Cash Flow'):
        # Retrieve dataframes from session state outside the if statement
        cf = st.session_state.get('cf')
        st.write(cf.head(3))
        st.bar_chart(cf)

        cf_str = st.session_state.get("cf_str")
        st.session_state["messages"].append({"role": "user", "content": cf_str})
        with st.chat_message("user"):
            st.markdown(cf_str)
    
        with st.chat_message("assistant"):
            with st.spinner("Streaming"):
                message = st.write_stream(stream_token())
                st.session_state["messages"].append({"role": "assistant", "content": message})

if st.session_state.get('retrieve_inc_clicked'):
    if st.button('Income Statement'):
        # Retrieve dataframes from session state outside the if statement
        inc = st.session_state.get('inc')
        st.write(inc.head(3))
        st.bar_chart(inc)

        inc_str = st.session_state.get("inc_str")
        st.session_state["messages"].append({"role": "user", "content": inc_str})
        with st.chat_message("user"):
            st.markdown(inc_str)
    
        with st.chat_message("assistant"):
            with st.spinner("Streaming"):
                message = st.write_stream(stream_token())
                st.session_state["messages"].append({"role": "assistant", "content": message})

# Check if a chat prompt has been submitted
prompt = st.chat_input("Enter your prompt here")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Streaming"):
            message = st.write_stream(stream_token())
            st.session_state["messages"].append({"role": "assistant", "content": message})
            st.snow()

else:
    # Display the Lottie animation with the adjusted height if no chat has started
    if lottie_file:
        st_lottie(
            lottie_file,
            speed=1,
            reverse=False,
            quality="high",
            height=height
        )

