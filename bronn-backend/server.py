from fastapi import FastAPI, HTTPException
import logging
from dotenv import load_dotenv
from agents import bronn_orchestrator, extract_article_info, extract_price, generate_stock_report, generate_suggestion_report, predict_stock
from helper import process_articles
from services.stock_suggestion import StockSuggester
from services.webscraper import WebScraper
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from services.stock_prediction import make_prediction

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserPrompt(BaseModel):
    query: str

TICKERS = [
    "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS",
    "LT.NS", "SUNPHARMA.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "DMART.NS",
    "KOTAKBANK.NS", "ASIANPAINT.NS", "MARUTI.NS", "AXISBANK.NS", "TITAN.NS",
    "BAJFINANCE.NS", "ITC.NS", "SBIN.NS", "WIPRO.NS", "HCLTECH.NS",
    "ULTRACEMCO.NS", "TECHM.NS", "NESTLEIND.NS", "POWERGRID.NS", "GRASIM.NS",
    "ONGC.NS", "ADANIGREEN.NS", "JSWSTEEL.NS", "NTPC.NS", "M&M.NS"
]
suggester = StockSuggester(TICKERS)



async def analyze_stock(prompt: UserPrompt):
    try:
        scraper = WebScraper(f"https://www.google.com/search?q={prompt.query}+stock+news&tbm=nws")
        scraper_articles = await scraper.scraping_with_langchain()
        news_response = await extract_article_info(scraper_articles, prompt.query)
        
        processed_news_response = await process_articles(news_response, prompt.query)
        return processed_news_response
    
    except Exception as e:
        logger.error(f"Error in analyze_stock: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing stock")

async def predict(user_query: UserPrompt):
    try:
        full_prediction, reduced_prediction, stock_name = await predict_stock(user_query.query)

        report = await generate_stock_report(reduced_prediction, stock_name)
        
        response = {
            "prediction": full_prediction,
            "report": {
                "introduction": report.introduction,
                "insights": report.insights,
                "conclusion": report.conclusion
            }
        }
        
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

async def analyze_stocks(user_query: UserPrompt):
    try:
        price_finder = await extract_price(user_query.query)
        user_price = price_finder.price

        results = suggester.suggest_stocks(user_price, num_suggestions=3)
        detailed_results = suggester.get_detailed_data(results)

        suggestion_report = await generate_suggestion_report(detailed_results)

        return {
            "suggested_stocks": detailed_results,
            "report": suggestion_report
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in analyze_stocks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    

@app.post("/bronn")
async def bronn_endpoint(user_prompt: UserPrompt):
    try:
        bronn_response = await bronn_orchestrator(user_prompt.query)
        
        if bronn_response.response == "0":
            return await analyze_stock(user_prompt)
        elif bronn_response.response == "1":
            return await predict(user_prompt)
        elif bronn_response.response == "2":
            return await analyze_stocks(user_prompt)
        else:
            return {"general": bronn_response.response}
    
    except Exception as e:
        logger.error(f"Error in bronn_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing request")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)