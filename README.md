# Financial Analyst

This Streamlit application provides a financial analysis based on company data. It scrapes financial data from the web and presents it in an interactive format. The application also features a conversational assistant named Yorkshire Umbra Vesper Azrael (YUVA), who provides detailed analysis in a unique, dark, and proud character style inspired by Wednesday Addams. 

![Alt text](FinAnalyst.gif)

## Features

- Scrapes financial data from the web, including income statements, balance sheets, cash flow statements, and financial ratios.
- Allows users to upload their CSV files for analysis.
- Interactive visualizations and data display.
- Conversational assistant (YUVA) provides detailed financial analysis.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.6 or higher
- Git

### Clone the Repository

1. Clone the repository to your local machine using Git:

   ```bash
   git clone https://github.com/your_username/financial-analyst.git
   cd financial-analyst


## Create a Virtual Environment

It’s a good practice to use a virtual environment. Create and activate a virtual environment:
    
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

## Install Dependencies

3.	Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt


## Features and Interaction

	•	Upload a CSV File: Use the file uploader in the sidebar to upload your financial data in CSV format.
	•	Retrieve Financial Data: Enter the ticker symbol of the company you wish to analyze and click the corresponding buttons to retrieve financial ratios, balance sheet, cash flow, and income statement data.
	•	Conversational Assistant (YUVA): Interact with YUVA, who will provide detailed financial analysis. Ensure you provide the data in plain text or ask YUVA specific questions.

## Example of Interaction

	1.	Upload a CSV File:
	•	Click the “Upload Your CSV File” button in the sidebar.
	•	Select and upload your CSV file.
	•	The application will display a preview of the uploaded data.
	2.	Retrieve Financial Data:
	•	Enter the ticker symbol (e.g., AAPL) in the text input field.
	•	Click “Retrieve Ratios”, “Retrieve Balance Sheet”, “Retrieve Cash Flow”, or “Retrieve Income Statement” to fetch the respective financial data.
	•	The application will scrape and display the data.
	3.	Conversational Analysis:
	•	Start a conversation with YUVA by entering a prompt in the chat input.
	•	YUVA will respond with analysis based on the provided data.
