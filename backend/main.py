import os
import sys
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.dashboard_service import get_data, TOTAL_BUDGET
from transformations.data_transformations import (
    calculate_daily_avg_category_per_country,
    calculate_daily_average_per_category,
    calculate_average_daily_budget_per_country,
    calculate_total_spend_per_country,
    calculate_cumulative_spend_per_country_by_day
)

app = FastAPI(title="Travel Expenses API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/summary")
async def get_summary():
    df = get_data()
    if df.empty:
        return {"error": "No data found"}
    
    total_spent = float(df['Amount'].sum())
    total_days = int(df['Date'].nunique())
    daily_avg = total_spent / total_days if total_days > 0 else 0
    remaining = float(TOTAL_BUDGET - total_spent)
    percent_used = min(total_spent / TOTAL_BUDGET, 1.0)
    days_remaining = int(remaining / daily_avg) if daily_avg > 0 else 0
    
    return {
        "total_spent": total_spent,
        "daily_avg": daily_avg,
        "remaining": remaining,
        "days": total_days,
        "percent_used": percent_used,
        "days_remaining": days_remaining,
        "total_budget": TOTAL_BUDGET
    }

@app.get("/api/charts/allocation")
async def get_allocation_chart():
    df = get_data()
    if df.empty:
        return []
    
    cat_avg_df = calculate_daily_average_per_category(df.copy())
    return cat_avg_df.to_dict(orient="records")

@app.get("/api/charts/country")
async def get_country_charts():
    df = get_data()
    if df.empty:
        return {"total": [], "daily": []}
    
    total_spend = calculate_total_spend_per_country(df.copy())
    daily_avg = calculate_average_daily_budget_per_country(df.copy())
    
    return {
        "total": total_spend.to_dict(orient="records"),
        "daily": daily_avg.to_dict(orient="records")
    }

@app.get("/api/charts/trends")
async def get_trend_charts():
    df = get_data()
    if df.empty:
        return {"cumulative": [], "comparison": []}
    
    # Cumulative burn
    burn_df = df.groupby('Date')['Amount'].sum().reset_index().sort_values('Date')
    burn_df['Cumulative_Total'] = burn_df['Amount'].cumsum()
    # Format date for frontend
    burn_df['Date'] = pd.to_datetime(burn_df['Date']).dt.strftime('%Y-%m-%d')
    
    # Comparison
    comparison_df = calculate_cumulative_spend_per_country_by_day(df.copy())
    
    return {
        "cumulative": burn_df.to_dict(orient="records"),
        "comparison": comparison_df.to_dict(orient="records")
    }

@app.get("/api/charts/categories")
async def get_category_charts():
    df = get_data()
    if df.empty:
        return []
    
    cat_country_data = calculate_daily_avg_category_per_country(df.copy())
    return cat_country_data.to_dict(orient="records")

@app.get("/api/transactions")
async def get_transactions():
    df = get_data()
    if df.empty:
        return []
    
    # Take latest 15 transactions
    latest = df.head(15).copy()
    # Convert dates to string for JSON serialization
    latest['Date'] = pd.to_datetime(latest['Date']).dt.strftime('%Y-%m-%d')
    return latest.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
