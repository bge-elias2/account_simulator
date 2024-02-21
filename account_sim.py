import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

initial_account_value = 1000000
account_value = initial_account_value
max_concurrent_trades = 1
active_trades = []
amount_invested = account_value / max_concurrent_trades
account_value_over_time = []

# Load the dataset
file_path = 'D:/ds_salary_proj/account_sim_master_sheet.csv'
data = pd.read_csv(file_path)

# Convert the datetime strings to datetime objects for comparison
data['entry_datetime'] = pd.to_datetime(data['entry_datetime'], format='%Y-%m-%d %H:%M:%S')
data['exit_datetime'] = pd.to_datetime(data['exit_datetime'], format='%Y-%m-%d %H:%M:%S')

# Sort the dataset by entry datetime to ensure chronological order
data_sorted = data.sort_values(by='entry_datetime')

# Initialize an empty list to keep track of ongoing trades
ongoing_trades = []

# Initialize a list to store indices of rows to keep
indices_to_keep = []

for index, row in data_sorted.iterrows():
    # Remove trades from ongoing_trades if their exit_datetime is before the current trade's entry_datetime
    ongoing_trades = [trade for trade in ongoing_trades if trade['exit_datetime'] >= row['entry_datetime']]
    
    # If there are less than "x" ongoing trades, we can enter a new trade
    if len(ongoing_trades) < max_concurrent_trades:
        ongoing_trades.append(row)
        indices_to_keep.append(index)

# Filter the dataset to keep only the trades that fit the criteria
filtered_data = data_sorted.loc[indices_to_keep]

def calculate_trade_result(ticker ,entry_price, exit_price, amount_invested):
    print(f"Calculating trade result for ticker: {ticker} with entry_price: {entry_price}, exit_price: {exit_price}, amount_invested: {amount_invested}")
    return (exit_price - entry_price) / entry_price * amount_invested

for index, row in filtered_data.iterrows():
    amount_invested = account_value / max_concurrent_trades
    trade_result = calculate_trade_result(row['Ticker'], row['entry_price'], row['exit_price'], amount_invested)
    print(trade_result)
    account_value += trade_result
    print(account_value)
    account_value_over_time.append(account_value)

print(f'final account value: {account_value}')
print(len(account_value_over_time))
print(len(filtered_data['Ticker']))

filtered_data['account_value_over_time'] = account_value_over_time

# Export filtered_data to an Excel file
file_path_to_export = 'D:/Account_Sim/exported_filtered_data_1_mill_1_trades.xlsx'  # Specify your desired file path
filtered_data.to_excel(file_path_to_export, index=False, engine='openpyxl')


