from datetime import date
from typing import Any, Dict
from fastapi import HTTPException
import joblib
import pandas as pd



def reduce_data_points(forecast, num_points=10):
    if len(forecast) <= num_points:
        return forecast
    reduced_indices = [0, len(forecast) - 1]
    
    step = len(forecast) // (num_points - 1)
    reduced_indices.extend(range(step, len(forecast) - 1, step))
    
    reduced_indices = sorted(set(reduced_indices))
    
    return forecast.iloc[reduced_indices]

def make_prediction(ticker: str, target_date: date) -> Dict[str, Any]:
    try:
        model = joblib.load(f'./models/{ticker}_model.pkl')
        
        combined_data = pd.read_csv('top_10_indian_stocks_data.csv')
        
        stock_data = combined_data[combined_data['Ticker'] == ticker]
        stock_data = stock_data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
        
        model_start_date = date(2024, 7, 1)
        
        business_days = len(pd.date_range(start=model_start_date, end=target_date)) 
        
        future = model.make_future_dataframe(stock_data, periods=business_days + 2)
        future = future[['ds','y']]
        
        forecast = model.predict(future)
        forecast['ds'] = pd.to_datetime(forecast['ds'])

        all_time_high = forecast['yhat1'].max()
        all_time_low = forecast['yhat1'].min()
        avg_price = forecast['yhat1'].mean()
        std_dev = forecast['yhat1'].std()
        
        volatility = (std_dev / avg_price) * 100
  
        ath_date = forecast.loc[forecast['yhat1'].idxmax(), 'ds'].strftime('%Y-%m-%d')
        atl_date = forecast.loc[forecast['yhat1'].idxmin(), 'ds'].strftime('%Y-%m-%d')


        ma30_window = min(30, business_days)
        ma90_window = min(90, business_days)
        forecast['MA30'] = forecast['yhat1'].rolling(window=ma30_window, min_periods=1).mean()
        forecast['MA90'] = forecast['yhat1'].rolling(window=ma90_window, min_periods=1).mean()

        trend_window = min(30, business_days)
        last_n_days = forecast['yhat1'].tail(trend_window)
        trend = 'Upward' if last_n_days.iloc[-1] > last_n_days.iloc[0] else 'Downward'

        forecast['ds'] = forecast['ds'].dt.strftime('%Y-%m-%d')
        reduced_forecast = reduce_data_points(forecast)
        
        full_result = {
            "prediction": {
                "x": forecast['ds'].tolist(),
                "y": forecast['yhat1'].tolist()
            },
            "trend": {
                "x": forecast['ds'].tolist(),
                "y": forecast['trend'].tolist()
            }
        }
        
        reduce_result = {
            "prediction": {
                "x": reduced_forecast['ds'].tolist(),
                "y": reduced_forecast['yhat1'].tolist()
            },
            "trend": {
                "x": reduced_forecast['ds'].tolist(),
                "y": reduced_forecast['trend'].tolist()
            },
            "summary": {
                "start_date": forecast['ds'].iloc[0],
                "end_date": forecast['ds'].iloc[-1],
                "prediction_days": business_days,
                "start_value": round(forecast['yhat1'].iloc[0], 2),
                "end_value": round(forecast['yhat1'].iloc[-1], 2),
                "overall_change": round(forecast['yhat1'].iloc[-1] - forecast['yhat1'].iloc[0], 2),
                "overall_change_percent": round((forecast['yhat1'].iloc[-1] / forecast['yhat1'].iloc[0] - 1) * 100, 2),
                "all_time_high": round(all_time_high, 2),
                "all_time_high_date": ath_date,
                "all_time_low": round(all_time_low, 2),
                "all_time_low_date": atl_date,
                "average_price": round(avg_price, 2),
                "standard_deviation": round(std_dev, 2),
                "volatility_percent": round(volatility, 2),
                f"last_{trend_window}_day_trend": trend,
                f"ma{ma30_window}_end": round(forecast['MA30'].iloc[-1], 2),
                f"ma{ma90_window}_end": round(forecast['MA90'].iloc[-1], 2)
            }
        }
        
        return full_result, reduce_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")