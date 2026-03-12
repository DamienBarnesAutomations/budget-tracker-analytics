import os
import pandas as pd
from services.dashboard_service import get_data

def main():
    print("Fetching data from 'Cleaned_Data'...")
    df = get_data()
    if df.empty:
        print("Dataframe is empty.")
        return
    
    print(f"Loaded {len(df)} rows.")
    print("Categories present in 'Cleaned_Data':")
    print(df['Category'].unique())
    
    flights = df[df['Category'] == 'Flights']
    print(f"Number of flight entries: {len(flights)}")
    if len(flights) > 0:
        print("First few flight entries:")
        print(flights.head())

if __name__ == "__main__":
    main()
