# Bronn API

This FastAPI application provides endpoints for stock analysis, prediction, and suggestions based on user queries. The API integrates various services to scrape stock news, predict stock performance, and suggest stocks based on user-defined criteria.

## Features

- **Analyze Stock**: Scrapes stock news and processes articles to provide insights.
- **Predict Stock**: Predicts stock performance based on user queries.
- **Suggest Stocks**: Suggests stocks based on user price and predefined tickers.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/stock-analysis-api.git
    cd stock-analysis-api
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add necessary environment variables.

## Environment Variables

Ensure you have a `.env` file in your project root. The content of the `.env` file should look like this:
```
Add your environment variables here
Example:
GROQ_API_KEY = GROQ_API_KEY
OPENAI_API_KEY = OPENAI_API_KEY
```

## Usage

1. **Run the application**:
    ```sh
    uvicorn main:app --reload
    ```

2. **API Endpoints**:

    - **Analyze Stock**: 
      ```sh
      POST /bronn
      ```
      Request Body:
      ```json
      {
          "query": "Your stock query"
      }
      ```

## Code Structure

```
├── main.py                        # Main application file
├── agents                         # Agents handling various tasks
│   ├── bronn_orchestrator.py
│   ├── extract_article_info.py
│   ├── extract_price.py
│   ├── generate_stock_report.py
│   ├── generate_suggestion_report.py
│   └── predict_stock.py
├── helper                        # Helper functions
│   └── process_articles.py
├── services                      # Service modules
│   ├── stock_prediction.py
│   ├── stock_suggestion.py
│   └── webscraper.py
├── .env                          # Environment variables file
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

- **main.py**: The main FastAPI application file that defines the API endpoints and integrates the services.
- **agents**: Contains orchestrator and other agent functionalities for various tasks like article extraction, price extraction, etc.
- **services**: Contains service classes like `StockSuggester` and `WebScraper` that handle specific functionalities.
- **helper.py**: Helper functions to process articles and perform other utility tasks.
- **.env**: Environment variables file to store sensitive information.

## Dependencies

- **fastapi**: The web framework used to build the API.
- **pydantic**: Data validation and settings management using Python type annotations.
- **uvicorn**: ASGI server to run the FastAPI application.
- **dotenv**: To load environment variables from a `.env` file.
- Other dependencies required for scraping, prediction, and suggestion tasks (list them in `requirements.txt`).

## Logging

The application uses Python's built-in logging module to log information and errors. Logs are configured to display info level messages and above.

## Middleware

The application uses `CORSMiddleware` to handle Cross-Origin Resource Sharing (CORS). It allows all origins, methods, and headers.

