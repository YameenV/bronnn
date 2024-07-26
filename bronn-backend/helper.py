
import logging
from typing import Literal, Optional
from pydantic import BaseModel, Field, HttpUrl
import requests
from agents import summarize_and_predict
from data_models import  NewsResponse
from services.webscraper import WebScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Article(BaseModel):
    title: str = Field('', description="Title of the article")
    source: str = Field('', description="Name of the source")
    time_uploaded: str = Field('', description="Time when the article was uploaded")
    link: HttpUrl = Field('', description="URL of the article")
    summary: str = Field('', description="Summary of the article")
    prediction: Literal["UP", "DOWN"] = Field(None, description="Prediction indicating either 'UP' or 'DOWN'")

async def process_articles(news_response: NewsResponse, stock_name: str) -> NewsResponse:
    processed_articles = []
    for article in news_response.news.articles:
        try:
            scraper = WebScraper(article.link)
            article_data = scraper.scraping_with_langchain(wanted_tags=["h1", "h2", "h3", "span", "p"])
            sum_data = await summarize_and_predict(article_data, stock_name)
            print(sum_data)
            processed_article = Article(
                title=article.title,
                source=article.source,
                time_uploaded=article.time_uploaded,
                link=article.link,
                summary=sum_data.summary,
                prediction=sum_data.prediction
            )
            processed_articles.append(processed_article)
        except Exception as e:
            logger.error(f"Error processing article: {str(e)}")
            processed_article = Article(
                title=article.title,
                source=article.source,
                time_uploaded=article.time_uploaded,
                link=article.link,
                summary="",
                prediction=""
            )
            processed_articles.append(processed_article)  # Add original article if processing fails

    news_response.news.articles = processed_articles
    return news_response

def get_logo_url(ticker: str) -> Optional[str]:
    company_name = ticker.split('.')[0]
    url = f"https://logo.clearbit.com/{company_name}.com"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return url
    except Exception as e:
        print(f"Error fetching logo for {ticker}: {str(e)}")
    return None