import requests
import pygal
from datetime import datetime

#Api setup
API_KEY = "6S6GQ8K8UNOSFDJS"
BASE_URL = "https://www.alphavantage.co/query"

while True:
    #user inputs
    stock_symbol = input("Enter stock symbol (e.g., AAPL, MSFT): ").upper()

    print("\nEnter chart type \n1.Line\n2.Bar\n")
    chart_type = input("Enter chart type (1 or 2): ").lower()

    print("\nEnter Time Series \n1.Intraday\n2.Daily\n3.Weekly\n4.Monthly\n")
    function_choice = input("Enter 1, 2, 3, or 4: ")

    start_date = input("\nEnter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

#determine choice of API parameters
    if function_choice == '1':
        function = "TIME_SERIES_INTRADAY"
        interval = "60min"
    elif function_choice == '2':
        function = "TIME_SERIES_DAILY"
        interval = None
    elif function_choice == '3':
        function = "TIME_SERIES_WEEKLY"
        interval = None
    elif function_choice == '4':
        function = "TIME_SERIES_MONTHLY"
        interval = None
    else:
        print("Invalid choice. Please try again.")
        continue

    #api parameters
    params = {
        "function": function,
        "symbol": stock_symbol,
        "apikey": API_KEY
    }
    if interval:
        params["interval"] = interval

    print("\nFetching data from Alpha Vantage...")
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    #check if data is valid
    time_series_key = None
    for key in data.keys():
        if "Time Series" in key:
            time_series_key = key
            break

    if not time_series_key:
        print("No valid data returned. Possibly hit the API limit or invalid symbol.")
        continue

    time_series_data = data[time_series_key]

    #filter data
    filtered_dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    close_prices = []

    for date_str, values in time_series_data.items():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date() if ' ' in date_str else datetime.strptime(date_str, "%Y-%m-%d").date()
            if start_date <= date_str[:10] <= end_date:
                filtered_dates.append(date_obj)
                open_prices.append(float(values["1. open"]))
                high_prices.append(float(values["2. high"]))
                low_prices.append(float(values["3. low"]))
                close_prices.append(float(values["4. close"]))
        except Exception as e:
            continue

    if not filtered_dates:
        print("No data found in that date range. Try a wider range.")
        continue

    filtered_dates, open_prices, high_prices, low_prices, close_prices = zip(*sorted(zip(filtered_dates, open_prices, high_prices, low_prices, close_prices)))

    #create chart
    print("Generating chart...")
    if chart_type == '2':
        chart = pygal.Bar(x_label_rotation=45)
        chart.title = f"{stock_symbol} Stock Prices (Bar Chart)"
        chart.x_labels = filtered_dates
        chart.add("Open Price", open_prices)
        chart.add("High Price", high_prices)
        chart.add("Low Price", low_prices)
        chart.add("Close Price", close_prices)
    else:
        chart = pygal.Line(x_label_rotation=45)
        chart.title = f"{stock_symbol} Stock Prices (Line Chart)"
        chart.x_labels = filtered_dates
        chart.add("Open Price", open_prices)
        chart.add("High Price", high_prices)
        chart.add("Low Price", low_prices)
        chart.add("Close Price", close_prices)

    chart.render_in_browser()
    print("Chart generated successfully!\n")

#continue or exit
    continue_prompt = input("\nDo you want to continue? (yes/no): \n").lower()
    if continue_prompt != 'yes':
        print("Exiting the program.")
        break