#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:01:21 2024

@author: hohlbein
"""
import yfinance as yf
import pandas as pd
from datetime import datetime

# Step 1: Fetch Historical Data
def fetch_sp500_data(start_date="1980-01-01"):
    sp500 = yf.Ticker("^GSPC")  # ^GSPC is the Yahoo Finance symbol for the S&P 500
    data = sp500.history(start=start_date)
    return data

# Step 2: Calculate Average Yearly Increase
def calculate_average_yearly_increase(data):
    data['Year'] = data.index.year  # Extract the year from the index
    yearly_data = data.groupby('Year')['Close'].last()  # Take the closing price for each year
    yearly_increase = yearly_data.pct_change().dropna()  # Calculate the percentage change
    
    avg_yearly_increase = yearly_increase.mean()  # Calculate the average increase
    return avg_yearly_increase

# Step 3: Extrapolate to January 2029
def extrapolate_to_date(start_value, avg_yearly_increase, target_date):
    current_year = datetime.now().year
    target_year = target_date.year
    years_to_project = target_year - current_year
    
    projected_value = start_value * ((1 + avg_yearly_increase) ** years_to_project)
    return projected_value

# Main Program
if __name__ == "__main__":
    # Fetch historical data starting from 1980
    historical_data = fetch_sp500_data(start_date="1980-01-01")
    
    # Calculate average yearly increase
    avg_increase = calculate_average_yearly_increase(historical_data)
    # avg_increase = 0.106
    print(f"Average yearly increase: {avg_increase * 100:.2f}%")
    
    # Get the latest S&P 500 closing value
    latest_close = historical_data['Close'].iloc[-1]
    print(f"Latest S&P 500 closing value: {latest_close:.2f}")
    
    # Extrapolate to January 2029
    target_date = datetime(2029, 1, 19)
    projected_value = extrapolate_to_date(latest_close, avg_increase, target_date)
    print(f"Projected S&P 500 value on {target_date.strftime('%Y-%m-%d')}: {projected_value:.2f}")


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# import yfinance as yf

# # Step 1: Load the historical S&P500 data
# # Fetch data using yfinance
# sp500 = yf.Ticker("^GSPC")
# data = sp500.history(period="max")  # Fetches maximum available history
# data.reset_index(inplace=True)
# data = data[['Date', 'Close']]  # Keep only relevant columns

# # Step 2: Calculate the average annual increase
# data['Year'] = data['Date'].dt.year
# annual_avg = data.groupby('Year')['Close'].mean()  # Calculate yearly average close
# annual_increase = annual_avg.pct_change().mean()  # Calculate average percentage increase

# # Step 3: Extrapolate to January 2029
# latest_year = data['Year'].max()
# latest_close = data.loc[data['Year'] == latest_year, 'Close'].iloc[-1]  # Get the latest close price
# years_to_2029 = 2029 - latest_year
# extrapolated_value = latest_close * ((1 + annual_increase) ** years_to_2029)

# # Step 4: Plot historical data and trendline
# plt.figure(figsize=(12, 6))
# plt.plot(data['Date'], data['Close'], label='Historical S&P500', color='blue')

# # Add trendline
# trend_years = np.arange(latest_year + 1, 2030)
# trendline_values = [latest_close * ((1 + annual_increase) ** (year - latest_year)) for year in trend_years]
# trend_dates = pd.date_range(start=f'{latest_year}-01-01', periods=len(trend_years), freq='Y')
# plt.plot(trend_dates, trendline_values, label='Trendline to 2029', color='red', linestyle='--')

# # Annotate extrapolated value
# plt.scatter(trend_dates[-1], trendline_values[-1], color='green', label=f'2029: {extrapolated_value:.2f}')
# plt.text(trend_dates[-1], trendline_values[-1], f"{extrapolated_value:.2f}", fontsize=10, color="green")

# # Formatting plot
# plt.title('S&P500 Historical Data with Trendline Projection to 2029', fontsize=14)
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('S&P500 Index', fontsize=12)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()

# # Show plot
# plt.show()

# # Print extrapolated value
# print(f"Extrapolated value for January 2029: {extrapolated_value:.2f}")
