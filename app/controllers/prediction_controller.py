import json
import csv
from datetime import datetime
import re
from prophet import Prophet
import pandas as pd


def predict_sales_forecasting(data, start_date, duration):

    json_data = preprocess_data(data)
    forecast_periods = duration
    forecast_start_date = start_date
    forecast_last_start_date = (
        str(int(forecast_start_date[:4]) - 1) + forecast_start_date[4:]
    )

    df = pd.DataFrame(json_data)

    # Ensure the date column is in datetime format
    df["ds"] = pd.to_datetime(df["ds"], format="%Y-%m-%d")

    # Get unique products
    products = df["product_name"].unique()

    # Define forecast duration

    # Prepare forecast results storage
    forecast_results = []

    # Forecast separately for each product
    for product in products:
        # Filter dataset for the current product
        df_product = df[df["product_name"] == product]

        # Initialize Prophet Model
        m = Prophet()
        m.fit(df_product[["ds", "y"]])

        # Generate Future Dates for Forecasting (starting from custom date)
        future = pd.date_range(
            start=forecast_start_date, periods=forecast_periods, freq="MS"
        ).to_frame(index=False, name="ds")

        # Ensure the end date is the last day of the forecasted month
        end_date = future["ds"].max() + pd.offsets.MonthEnd(0)

        # Make Predictions for the Future
        forecast = m.predict(future)

        sum_forecast_now = forecast["yhat"].sum()

        selected_months = (
            df_product["ds"]
            .dt.strftime("%Y-%m")
            .isin(
                pd.date_range(
                    start=forecast_last_start_date, periods=forecast_periods, freq="MS"
                ).strftime("%Y-%m")
            )
        )

        actual_sales_values = df_product.loc[selected_months, "y"].tolist()
        actual_last_year_sales = (
            sum(actual_sales_values) if len(actual_sales_values) > 0 else 0
        )

        # Calculate percentage change correctly
        percent_change = (
            ((sum_forecast_now - actual_last_year_sales) / abs(actual_last_year_sales))
            * 100
            if actual_last_year_sales != 0
            else "N/A"
        )

        # Store the result in the required format
        forecast_results.append(
            {
                "ProductName": product,
                "Duration": f"{forecast_start_date} - {end_date.date()}",
                "Forecast": round(sum_forecast_now, 2),
                "Last Year Actual Sales": round(actual_last_year_sales, 2),
                "% Change from Previous Year": (
                    round(percent_change, 2) if percent_change != "N/A" else "N/A"
                ),
            }
        )
    return json.dumps(forecast_results, indent=4)


def preprocess_data(data):
    json_data = []
    data.stream.seek(0)  # Ensure reading from the start
    reader = csv.DictReader(data.stream.read().decode("utf-8").splitlines())

    headers = reader.fieldnames

    # Identify columns related to sales data (e.g., "Quantity Sold Jan 2016")
    sales_columns = [
        header for header in headers if re.match(r"Quantity Sold \w+ \d{4}", header)
    ]

    # Extract years from the column names (e.g., from "Quantity Sold Jan 2016")
    years = set()
    for col in sales_columns:
        match = re.match(r"Quantity Sold \w+ (\d{4})", col)
        if match:
            years.add(int(match.group(1)))

    # Dictionary to store aggregated sales
    aggregated_data = {}

    # Loop through each row in the CSV
    for row in reader:
        product_name = row["Product Name"]

        # Loop through the years and months dynamically
        for year in range(min(years), max(years) + 1):
            for month in range(1, 13):
                # Create the header for this specific month and year (e.g., "Quantity Sold Jan 2016")
                month_name = datetime(year=year, month=month, day=1).strftime(
                    "%b %Y"
                )  # e.g., "Jan 2016"
                column_name = f"Quantity Sold {month_name}"

                # Check if this column exists in the CSV for this product
                if column_name in row:
                    quantity_sold = row[column_name]

                    # Only add valid data (non-empty, non-null values)
                    if quantity_sold and quantity_sold.strip().isdigit():
                        # Format the date for the 'ds' field in the required format (YYYY-MM-DD)
                        date_str = datetime(year=year, month=month, day=1).strftime(
                            "%Y-%m-%d"
                        )

                        # **Aggregate Sales for Each Product and Date**
                        key = (product_name, date_str)
                        if key in aggregated_data:
                            aggregated_data[key]["y"] += int(quantity_sold)
                        else:
                            aggregated_data[key] = {
                                "ds": date_str,
                                "y": int(quantity_sold),
                                "product_name": product_name,
                            }

    # Convert aggregated data dictionary to a list
    json_data = list(aggregated_data.values())

    return json_data
