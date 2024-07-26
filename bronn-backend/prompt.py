from langchain.prompts import ChatPromptTemplate

article_extraction_prompt = ChatPromptTemplate.from_template("""
The following text is scraped from a Google News search for {stock_name} stock.
Please analyze the content and structure the information in the following JSON format:

Instructions:
1. Extract the top 3 most relevant articles about {stock_name} stock.
2. Only include articles that are clearly about {stock_name} stock. If you can't find any relevant articles, return an empty list for "articles".
3. Generate a concise introduction that summarizes the overall sentiment and key themes of the news.
4. For each article, provide the requested information accurately, including:
   - The full title of the article
   - The domain name of the source (e.g., mint.com, bloomberg.com)
   - The time of upload as provided in the scraped text
   - The complete URL link to the article (this is crucial and must not be omitted)
5. If a link is not available in the scraped text, use "No link available" instead of an empty string.
6. To get the domain name, extract it from the article's URL. If no URL is available, use a generic domain based on the source name (e.g., "financialtimes.com" for Financial Times).
7. Generate a brief conclusion that synthesizes the main points from the articles and their potential impact on the stock.
8. Ensure all text fields (intro, titles, conclusion) are properly escaped for JSON format.

Scraped text:
```{html_content}```
""")

summarization_prediction_prompt = ChatPromptTemplate.from_template("""
Analyze this article about {stock_name} stock. Provide a summary and prediction in this exact JSON format:
{{
  "summarization": "3-5 sentence summary focusing on key facts that could affect stock price",
  "prediction": "UP or DOWN"
}}
Instructions:
1. Summary: Write a detailed summary of the article in 4-6 sentences. Focus on the most important points that could impact the stock price. Include key financial data, company developments, and market trends mentioned in the article.

2. Prediction: Based on the information in the article, predict whether the stock is likely to go UP or DOWN in the short term. Use only "UP" or "DOWN" for your prediction.

Article:
```{article_content}```
                                                                   
""")

stock_time_extraction_prompt = ChatPromptTemplate.from_template("""
You are a financial assistant tasked with extracting stock ticker information and prediction timeframes from user queries. You have access to the following list of Indian stock tickers:

HDFCBANK.NS (HDFC Bank)
RELIANCE.NS (Reliance Industries)
ICICIBANK.NS (ICICI Bank)
INFY.NS (Infosys)
TCS.NS (Tata Consultancy Services)
LT.NS (Larsen & Toubro)
SUNPHARMA.NS (Sun Pharmaceutical Industries)
BHARTIARTL.NS (Bharti Airtel)
HINDUNILVR.NS (Hindustan Unilever)
DMART.NS (Avenue Supermarts / DMart)

User Query: {query}

Your tasks:
1. Analyze the user query and identify any mention of companies or stock names.
2. If a company or stock is mentioned, find the corresponding ticker from the list above.
3. Identify any mention of a prediction timeframe (e.g., "next week", "in 3 months", "by end of year").
4. Convert the identified timeframe to a specific date in the format YYYY-MM-DD.
   - Use the current date ({current_date}) as the reference point.
   - If no specific timeframe is mentioned, use the current date plus 7 days as the default.

Be sure to handle partial matches and common abbreviations for company names.

JSON Result:
""")


stock_report_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant specializing in explaining financial predictions. Your task is to interpret and communicate the results of our stock prediction model for {stock_name}. Remember, these are predictions and not guaranteed outcomes.

Stock Name: ```{stock_name}```
Our Model's Prediction Data:
```{prediction_data}```

Analyze this prediction data and provide a structured JSON response with the following components:

1. "introduction": A concise summary of 3 to 5 sentences our model's predicted trend for {stock_name}. Include the overall change and percentage change predicted by the model, as well as the number of business days in the prediction period.

2. "insights": A markdown-formatted string containing multiple observations from our prediction data. Each point should be presented as a separate bullet. Consider:
   - Predicted start and end values
   - Forecasted overall change and percentage change
   - All-time high and low prices with their respective dates
   - Average price and volatility
   - The trend over the last N days (where N is the shorter of 30 or the total prediction days)
   - Comparison of moving averages at the end of the prediction period (use the actual number of days as shown in the data)
   - Any notable patterns or turning points in our predicted data points

3. "conclusion": A brief synthesis of the main points from our model's prediction, including potential scenarios for the stock. Consider the volatility and trend information when discussing potential outcomes. Emphasize the speculative nature of these predictions and advise users to consider other factors and do their own research before making investment decisions.

Use clear, accessible language and always remind the user that these are model-based predictions, not guarantees. Interpret our model's predictions:
""")

suggested_analysis_prompt = ChatPromptTemplate.from_template("""
You are a sophisticated financial advisor tasked with providing insights on suggested stocks to a user. Based on the following stock suggestions, generate an introduction, detailed insights, and a conclusion.

Suggested Stocks:
{suggested_stocks}

Your tasks:
1. Introduction:
   - Briefly summarize the overall market context.
   - Mention the user's query or investment goal if provided.

2. Detailed Insights :
   - Analyze each suggested stock, focusing on:
     a) Current price and its relation to recent trends.
     b) 1-month return and what it indicates about the stock's performance.
     c) Daily change and its significance.
    d)Provide a brief outlook on the potential risks and rewards.                                                       
   - Compare the stocks' performances and potential.
   - Highlight any notable strengths or concerns for each stock.

3. Conclusion and Recommendations:
   - Summarize the key takeaways from the analysis.
   - Provide specific recommendations based on the data.
   - Suggest a potential investment strategy or allocation.
   - Remind the user about the importance of diversification and conducting further research.


Present your analysis in a clear, concise, and professional manner. Use the data provided to support your insights and recommendations.

Analysis:
""")


price_extraction_prompt = ChatPromptTemplate.from_template("""
You are a financial assistant tasked with extracting price information from user queries. 

User Query: {query}

Your tasks:
1. Analyze the user query and identify any mention of price or monetary value.
2. If a price or monetary value is mentioned, extract this information.
3. Handle different formats of price mention, such as "50Rs", "Rs 50", "INR 50", sixty hunder or "50 INR".
4. If no specific price is mentioned, return 0

Be sure to handle partial matches and common abbreviations for monetary values.

JSON Result:
""")


agent_orchestrator_prompt = ChatPromptTemplate.from_template("""
You are a financial assistant name Bronn a agent orchestrator specializing in stock market queries. Analyze the user query and determine the appropriate function

User Query: {query}

Functions:
0 - Analyzing stock news (recent news, updates, events affecting a specific stock)

1 - Predicting stock performance (future stock prices, performance predictions, price targets)

2 - Suggesting stocks (finding stocks based on price, sector, performance, criteria)

Instructions:
- If the query is about predicting stock prices for a specific date or range, choose function 1.
- If the query clearly matches one of these functions, output the corresponding function number (0, 1, or 2).

IMPORTANT: Greeting and Non-Matching Queries
- If the query is a greeting (e.g., "hi", "hello", "good morning") or doesn't exactly match any of these functions, DO NOT output a function number.
- Instead, provide a brief, helpful response related to stock market assistance.

Response:
""")



