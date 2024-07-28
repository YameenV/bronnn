# Bronn
[![LangChain](https://img.shields.io/badge/LangChain-%2300E0E6?style=flat-square&logo=python&logoColor=white)](https://www.langchain.com) [![Python](https://img.shields.io/badge/Python-%2339457D?style=flat-square&logo=python&logoColor=white)](https://www.python.org) [![FastAPI](https://img.shields.io/badge/FastAPI-%23096E6C?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com) [![Uvicorn](https://img.shields.io/badge/Uvicorn-%2337475F?style=flat-square&logo=python&logoColor=white)](https://www.uvicorn.org) [![Pydantic](https://img.shields.io/badge/Pydantic-%2333B2FF?style=flat-square&logo=python&logoColor=white)](https://pydantic-docs.helpmanual.io) [![Requests](https://img.shields.io/badge/Requests-%232C2E2A?style=flat-square&logo=requests&logoColor=white)](https://docs.python-requests.org) [![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-%23D4A2A9?style=flat-square&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/) [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-%23F7931E?style=flat-square&logo=python&logoColor=white)](https://scikit-learn.org) [![Pandas](https://img.shields.io/badge/Pandas-%23150A54?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)

## Project Overview

The **Bronn Stock Analysis and Prediction Service** operates as an advanced chatbot designed to deliver comprehensive insights and recommendations for stock market investments. It employs a range of **specialized agents** to process user queries and provide actionable intelligence.

## Features

- **Stock News Analysis**: Retrieves and analyzes recent news articles related to a specific stock.
- **Stock Price Prediction**: Utilizes machine learning models to predict future stock prices.
- **Stock Suggestions**: Recommends alternative stocks based on the user's input and market data.
- **Comprehensive Reporting**: Generates detailed reports summarizing analysis results, predictions, and stock suggestions.

## Project Overview Video

![Watch the video](./bronn demo video.mp4)

## Architecture Diagram

![Architecture Diagram](./diagram.jpg)

## Agents and Their Functions

### 1. Bronn Orchestrator

The Bronn Orchestrator is the central decision-making agent in the system. It evaluates the user's query and determines which agent(s) should handle the request. Based on the response, it directs the flow of the request to:

- **Analyze Stock**: Retrieve and process stock news.
- **Predict Stock**: Generate price predictions.
- **Sugest Stock**: Provide stock suggestions based on price analysis.

### 2. Web Scraper

The Web Scraper fetches the latest news articles about a specific stock by performing a web search. It ensures that the news data is current and relevant to the user's query.

### 3. Article Info Extractor

After the Web Scraper retrieves the news articles, the Article Info Extractor processes them to extract key information such as headlines, summaries, and publication dates. This information is crucial for understanding market sentiment and trends.

### 4. Price Extractor

The Price Extractor finds the current price of the queried stock. This data is essential for making accurate predictions and suggestions.

### 5. Stock Predictor

The Stock Predictor uses machine learning models to forecast future stock prices based on historical data and current market conditions. It provides both detailed predictions and a summary for easier understanding.

### 6. Stock Suggester

The Stock Suggester recommends alternative stocks based on the current price and user preferences. It evaluates market trends and provides up to three suggested stocks for consideration.

### 7. Report Generators

- **Stock Report Generator**: Creates a detailed report of the stock prediction, including an introduction, insights, and conclusions.
- **Suggestion Report Generator**: Produces a report summarizing the suggested stocks, including detailed information to assist the user in making informed decisions.

## Dataset

The stock prediction model is trained using the dataset available from youdata.ai at the following link:

- [Stock Market Dataset](https://datalink.youdata.ai/3e6fve6e)

This dataset provides historical stock market data, which is crucial for training the prediction models and generating accurate forecasts.

## How It Works

1. **User Query**: The process starts when a user submits a query to the `/bronn` endpoint.
2. **Orchestration**: The Bronn Orchestrator determines the appropriate action (news analysis, price prediction, or stock suggestion) based on the query.
3. **Agent Invocation**: The orchestrator invokes the relevant agents to process the query.
4. **Data Processing**: Each agent processes the data and returns the results.
5. **Report Generation**: The appropriate report generator agent creates a comprehensive report.
6. **Response**: The orchestrator compiles the results and reports, then sends them back to the user.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **LangChain**: A framework for developing applications powered by language models, used here for web scraping and information extraction.
- **Uvicorn**: An ASGI server used to run the FastAPI application.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Deep Learning**: For stock price prediction and analysis using Neural Prophet.
- **Web Scraping**: To gather the latest news and stock data.

## Getting Started

To get started with the application, ensure you have the necessary environment variables set up and dependencies installed. Refer to the installation instructions and usage guidelines for more details on running the application and interacting with the API.


