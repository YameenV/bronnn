from datetime import date
import logging
import os
from dotenv import load_dotenv
from typing import List
from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from prompt import stock_time_extraction_prompt, stock_report_prompt, summarization_prediction_prompt, article_extraction_prompt, price_extraction_prompt, suggested_analysis_prompt, agent_orchestrator_prompt
from data_models import BronnResponse, PriceFinder, StockPredictionReport, StockTimeFinder, SuggestionReport, Summarization, NewsResponse
from services.stock_prediction import make_prediction

load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_TICKERS = [
    "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS",
    "LT.NS", "SUNPHARMA.NS", "BHARTIARTL.NS", "HINDUNILVR.NS", "DMART.NS"
]

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY environment variable is not set")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

async def predict_stock(query: str):
    stock_time_llm = ChatGroq(api_key=groq_api_key, model="mixtral-8x7b-32768")
    stock_time_structured_llm = stock_time_llm.with_structured_output(StockTimeFinder)

    current_date = date.today()

    extraction_chain = stock_time_extraction_prompt | stock_time_structured_llm
   
    result = await extraction_chain.ainvoke({"query": query, "current_date": current_date})
    
    if result.ticker and result.prediction_date:
        if result.ticker in VALID_TICKERS:
            full_prediction, reduced_prediction = make_prediction(result.ticker, result.prediction_date)
            return full_prediction, reduced_prediction, result.ticker
        else:
            raise HTTPException(status_code=400, detail=f"We only provide predictions for the following stocks: {', '.join(VALID_TICKERS)}. The requested stock {result.ticker} is not in this list.")
    else:
        raise HTTPException(status_code=400, detail="Could not extract ticker or prediction date from the query.")

async def generate_stock_report(prediction_data: dict, stock_name: str) -> StockPredictionReport:

    stockreport = ChatGroq(api_key=groq_api_key, model="mixtral-8x7b-32768")
    structured_stockreport_llm = stockreport.with_structured_output(StockPredictionReport)

    extraction_chain = stock_report_prompt | structured_stockreport_llm 
    try:
        result = await extraction_chain.ainvoke({"prediction_data": prediction_data, "stock_name": stock_name})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stock report: {str(e)}")
    
async def extract_article_info(html_content: str, stock_name: str) -> NewsResponse:
    article_extraction_llm = ChatGroq(api_key=groq_api_key, model="llama3-70b-8192")
    structured_articles_llm = article_extraction_llm.with_structured_output(NewsResponse)

    extraction_chain = article_extraction_prompt | structured_articles_llm 
    try:
        result = await extraction_chain.ainvoke({"html_content": html_content, "stock_name": stock_name})
        return result
    except Exception as e:
        logger.error(f"Error in extract_article_info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error extracting article information")

async def summarize_and_predict(article_content: str, stock_name: str) -> Summarization:
    summarize_and_predict_llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")
    structured_summarize_and_predict_llm = summarize_and_predict_llm.with_structured_output(Summarization)

    summarization_chain = summarization_prediction_prompt | structured_summarize_and_predict_llm 
    try:
        result = await summarization_chain.ainvoke({
            "article_content": article_content, 
            "stock_name": stock_name, 
        })
        return result
    except Exception as e:
        logger.error(f"Error in summarize_and_predict: {str(e)}")
        raise HTTPException(status_code=500, detail="Error summarizing and predicting")
    

async def extract_price(query: str) -> PriceFinder:
    price_extractor = ChatGroq(api_key=groq_api_key, model="gemma2-9b-it")
    price_extractor_structured = price_extractor.with_structured_output(PriceFinder)
    price_extraction_chain = price_extraction_prompt | price_extractor_structured

    try:
        result = await price_extraction_chain.ainvoke({"query": query})
        return result
    except Exception as e:
        logger.error(f"Error in extract_price: {str(e)}")
        raise HTTPException(status_code=500, detail="Error extracting price from query")

async def generate_suggestion_report(suggested_stocks: List) -> SuggestionReport:
    suggestion_report = ChatGroq(api_key=groq_api_key, model="gemma2-9b-it")
    suggestion_report_structured = suggestion_report.with_structured_output(SuggestionReport)
    suggestion_report_chain = suggested_analysis_prompt | suggestion_report_structured

    try:
        result = await suggestion_report_chain.ainvoke({"suggested_stocks": suggested_stocks})
        return result
    except Exception as e:
        logger.error(f"Error in generate_suggestion_report: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating suggestion report")
    
async def bronn_orchestrator(query: str) -> BronnResponse:
    bronn_orchestrator = ChatOpenAI(api_key=openai_api_key, model="gpt-4o")
    bronn_orchestrator_structured = bronn_orchestrator.with_structured_output(BronnResponse)

    bronn_orchestrator_chain = agent_orchestrator_prompt | bronn_orchestrator_structured

    try:
        result = await bronn_orchestrator_chain.ainvoke({"query": query})

        if result.response in ['0', '1', '2']:
            return BronnResponse(response=result.response)
        else:
            return BronnResponse(response=result.response)
        
    except Exception as e:
        logger.error(f"Error in generate_suggestion_report: {str(e)}")
        return BronnResponse(response="I'm sorry, I encountered an error while processing your request. Could you please try rephrasing your query?")
    

    
    