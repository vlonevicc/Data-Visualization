import requests
import pygal
from datetime import datetime

#Api setup
API_KEY = "6S6GQ8K8UNOSFDJS"
BASE_URL = "https://www.alphavantage.co/query"

while True:
    stock_symbol = input("Enter stock symbol (e.g., AAPL, MSFT): ").upper()

    print("\nEnter chart type \n1.Line\n2.Bar\n")
    chart_type = input("Enter chart type (1 or 2): ").lower()

    print("\nEnter Time Series \n1.Intraday\n2.Daily\n3.Weekly\n4.Monthly\n")
    function_choice = input("Enter 1, 2, 3, or 4: ")

    start_date = input("\nEnter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    continue_prompt = input("\nDo you want to continue? (yes/no): \n").lower()
    if continue_prompt != 'yes':
        print("Exiting the program.")
        break

# Determine function choice to API parameters
if function_choice == '1':
    function = "TIME_SERIES_INTRADAY"
    interval = "60min"
elif function_choice == '2':
    function = "TIME_SERIES_DAILY"
elif function_choice == '3':
    function = "TIME_SERIES_WEEKLY"
elif function_choice == '4':
    function = "TIME_SERIES_MONTHLY"
else:
    print("Invalid choice. Exiting.")
    exit()
