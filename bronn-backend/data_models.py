from datetime import date
from langchain_core.pydantic_v1 import BaseModel, Field, HttpUrl
from typing import List, Literal, Optional

class Summarization(BaseModel):
    summary: str = Field("", description="Write a summary of 4-6 sentences focusing on key facts that could affect stock price")
    prediction: Literal["UP", "DOWN"] = Field(..., description="Prediction indicating either 'UP' or 'DOWN'")

    class Config:
        json_schema_extra = {
            "example": {
                "summary": "The article discusses Q2 earnings of HDFC Bank, highlighting strong revenue growth and improved asset quality. The bank's digital initiatives and expanding customer base are noted as positive factors.",
                "prediction": "UP"
            }
        }


class Article(BaseModel):
    title: str = Field('', description="Title of the article")
    source: str = Field('', description="Domain name of the source (e.g., mint.com, bloomberg.com)")
    time_uploaded: str = Field('', description="Time when the article was uploaded")
    link: HttpUrl = Field('', description="URL of the article")

class News(BaseModel):
    intro: str = Field('', description="Introduction, 1 to 2 lines")
    articles: List[Article] = Field([], description="List of articles")
    conclusion: str = Field('', description="Conclusion")

class NewsResponse(BaseModel):
    news: News

    class Config:
        json_schema_extra = {
            "example": {
                "news": {
                    "intro": "Recent financial news highlights several key developments.",
                    "articles": [
                        {
                            "title": "Stock Market Reaches New High",
                            "source": "ft.com",
                            "time_uploaded": "1 day ago ",
                            "link": "https://www.ft.com/content/example-article"
                        },
                        {
                            "title": "Central Bank Announces Interest Rate Decision",
                            "source": "bloomberg.com",
                            "time_uploaded": "5 hour ago",
                            "link": "https://www.bloomberg.com/news/example-article"
                        }
                    ],
                    "conclusion": "These developments suggest a dynamic economic landscape."
                }
            }
        }

class StockPredictionReport(BaseModel):
    introduction: str = Field(..., description="A concise introduction summarizing the overall trend and key points from the prediction data.")
    insights: str = Field(..., description="A detailed string containing multiple insights derived from the prediction data in markdown format. Each insight should be clearly separated and easy to read.")
    conclusion: str = Field(..., description="A brief conclusion synthesizing the main points from the prediction data and their potential impact on the stock.")

    class Config:
        schema_extra = {
            "example": {
                "introduction": "The stock market has shown a bullish trend over the past quarter, driven by strong earnings reports and economic recovery.",
                "insights": "1. **Major tech stocks** have outperformed, with average gains of **15%**.\n2. **Energy sector** has lagged behind, with a **5% decrease**.\n3. **Retail stocks** have shown resilience, with steady growth of **8%**.",
                "conclusion": "Overall, the positive trend is expected to continue, potentially leading to further gains in major indices. However, caution is advised for energy sector investments."
            }
        }

class StockTimeFinder(BaseModel):
    ticker: Optional[str] = Field(" ", description="Stock ticker symbol, e.g., 'HDFCBANK.NS'")
    prediction_date: date = Field(" ", description="Date for the stock prediction in YYYY-MM-DD format")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "HDFCBANK.NS",
                "prediction_date": "2024-08-21"
            }
        }

class PriceFinder(BaseModel):
    price: Optional[int] = Field(0, description="Price of the stock in integer format, e.g., 50")

    class Config:
        json_schema_extra = {
            "example": {
                "price": 50
            }
        }


class SuggestionReport(BaseModel):
    introduction: str = Field(" ", description="A concise introduction summarizing the overall market context and the user's query or investment goal if provided.")
    conclusion: str = Field(" ", description="A brief conclusion synthesizing the main points from the analysis and providing specific recommendations.")

    class Config:
        schema_extra = {
            "example": {
                "introduction": "The stock market has experienced notable shifts recently, influenced by fluctuating economic indicators and sector-specific trends. The user is interested in evaluating stock performance to optimize their investment portfolio.",
                "conclusion": "The technology sector appears to be the most promising, given its high return rates and current market trends. Investors may consider increasing their allocation to tech stocks while maintaining a diversified portfolio. Further research and monitoring are recommended to adjust investments as market conditions evolve."
            }
        }

class BronnResponse(BaseModel):
    response: str = Field(..., description="Either a function number ('0', '1', '2') or a text response")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "1"
            },
            "example": {
                "response": "hi"
            }
        }