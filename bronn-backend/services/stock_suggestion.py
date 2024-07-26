from typing import List, Optional
from pydantic import BaseModel
import yfinance as yf
from collections import deque
import bisect
from helper import get_logo_url

class StockSuggestion(BaseModel):
    ticker: str
    company_name: str
    current_price: float
    return_1mo: float
    daily_change: float
    daily_change_percent: float
    logo_url: Optional[str]

class StockSuggester:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        self.stock_prices = self.load_stock_prices()
    
    def load_stock_prices(self):
        stock_prices = []
        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                price = stock.history(period="1d")['Close'].iloc[-1]
                stock_prices.append((price, ticker))
            except Exception as e:
                print(f"Error loading {ticker}: {str(e)}")
        return sorted(stock_prices)
    
    def suggest_stocks(self, user_price: float, num_suggestions: int = 3):
        suggestions = deque(maxlen=num_suggestions)
        idx = bisect.bisect_left(self.stock_prices, (user_price, ''))
        left = max(0, idx - num_suggestions)
        right = min(len(self.stock_prices), idx + num_suggestions)
        
        for price, ticker in self.stock_prices[left:right]:
            price_diff = abs(price - user_price)
            if len(suggestions) < num_suggestions:
                suggestions.append((price_diff, ticker, price))
            elif price_diff < max(suggestions, key=lambda x: x[0])[0]:
                suggestions.remove(max(suggestions, key=lambda x: x[0]))
                suggestions.append((price_diff, ticker, price))
        
        return [(ticker, price) for _, ticker, price in sorted(suggestions, key=lambda x: x[0])]
    
    def get_detailed_data(self, suggestions: List[tuple]) -> List[StockSuggestion]:
        detailed_suggestions = []
        for ticker, current_price in suggestions:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1mo")
                
                start_price = hist['Close'].iloc[0]
                return_1mo = ((current_price - start_price) / start_price) * 100
                prev_close = hist['Close'].iloc[-2]
                daily_change = current_price - prev_close
                daily_change_percent = (daily_change / prev_close) * 100
                company_name = stock.info.get('longName', ticker)
                logo_url = get_logo_url(ticker)

                detailed_suggestions.append(StockSuggestion(
                    ticker=ticker,
                    company_name=company_name,
                    current_price=round(current_price, 2),
                    return_1mo=round(return_1mo, 2),
                    daily_change=round(daily_change, 2),
                    daily_change_percent=round(daily_change_percent, 2),
                    logo_url=logo_url
                ))
            except Exception as e:
                print(f"Error getting detailed data for {ticker}: {str(e)}")
        
        return detailed_suggestions