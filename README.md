Below is your complete `README.md` file in Markdown format:

```markdown
# 📊 Sales Forecasting API using Flask & Prophet

This project is a **Flask-based API** that processes **historical sales data** from CSV files, **aggregates sales per product**, and uses **Facebook Prophet** to predict future sales trends.

## 🚀 Features

- Accepts a CSV file containing monthly sales data for multiple products.
- Aggregates sales **per product per month** before forecasting.
- Uses **Facebook Prophet** for time series forecasting.
- Returns **future sales predictions** along with last year's actual sales for comparison.
- **Calculates error metrics** (MAE, RMSE, MAPE) to evaluate forecasting accuracy.

---

## 🏠 Project Structure

backend/
│── app/
│   ├── __init__.py          # Initialize Flask app
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions (CORS, DB)
│   ├── routes.py            # Registering blueprints
│   ├── api/                 # API endpoints (routes)
│   │   ├── __init__.py      # API module initializer
│   │   ├── prediction_api.py # Forecasting API route
│   │   ├── user_api.py      # User-related API routes
│   ├── controllers/         # Business logic layer
│   │   ├── __init__.py
│   │   ├── prediction_controller.py # Prediction logic
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   ├── views/               # View functions for rendering
│   │   ├── __init__.py
│   │   ├── home.py          # Home view
│── build/                   # Frontend build folder
│── migrations/              # Database migrations
│── tests/                   # Unit tests
│   ├── db_connect.py        # Database connection test
│── README.md                # Project documentation
│── requirements.txt         # Dependencies
│── run.py                   # Run Flask app
```

---

## ⚡ Installation

### **1⃣ Install Dependencies**

Ensure you have **Python 3.8+** installed, then run:

```sh
pip install -r requirements.txt
```

This will install:

- `Flask`
- `pandas`
- `prophet`
- `pymysql`
- `flask-cors`

### **2⃣ Start the Flask App**

Run the server:

```sh
python run.py
```

This starts the Flask API on **`http://localhost:5000/`**.

---

## 📤 API Usage

### **📌 Upload Sales CSV & Get Forecast**

#### **Endpoint**

```
POST /api/predictions/generate
```

#### **Request Format**

- `Content-Type: multipart/form-data`
- **Parameters:**
  - `file` → CSV file containing sales data
  - `start_date` → Forecast start date (YYYY-MM-DD)
  - `duration` → Number of months to predict

#### **Example Request (cURL)**

```sh
curl -X POST "http://localhost:5000/forecast" \
  -F "file=@sales_data.csv" \
  -F "start_date=2025-01-01" \
  -F "duration=3"
```

#### **💾 Sample CSV Format**

```
Product Name,Quantity Sold Jan 2024,Quantity Sold Feb 2024
Toothbrush Set,10,15
Toothbrush Set,5,10
```

---

## 🔍 Expected JSON Response

```json
{
    "message": "Prediction created successfully!",
    "data": [
        {
            "ProductName": "Toothbrush Set",
            "Duration": "2025-01-01 - 2025-01-31",
            "Forecast": 30.5,
            "Last Year Actual Sales": 15,
            "% Change from Previous Year": 103.3
        },
        {
            "ProductName": "Toothbrush Set",
            "Duration": "2025-02-01 - 2025-02-28",
            "Forecast": 40.8,
            "Last Year Actual Sales": 25,
            "% Change from Previous Year": 63.2
        }
    ]
}
```

- **`Forecast`** → Predicted total sales for the month.
- **`Last Year Actual Sales`** → Aggregated actual sales from the same period in the previous year.
- **`% Change from Previous Year`** → Percentage increase or decrease.

---

## 📊 Error Metrics

In addition to generating sales forecasts, the API also calculates **error metrics** to evaluate the model’s performance. These metrics are computed by comparing the forecasted sales with the actual sales data for the forecast period.

### Error Metrics Provided

- **MAE (Mean Absolute Error):**  
  The average absolute difference between the forecasted and actual sales. It indicates, on average, how many units off the prediction is.

- **RMSE (Root Mean Squared Error):**  
  The square root of the average of the squared differences between forecasted and actual sales. RMSE penalizes larger errors more significantly, highlighting potential outliers.

- **MAPE (Mean Absolute Percentage Error):**  
  The average percentage difference between forecasted and actual sales. Note that if actual sales are 0, MAPE is set to 0.0% to avoid division by zero.

### How It Works

1. **Training Data Cutoff:**  
   The forecasting model is trained only on historical sales data available up to a cutoff date (e.g., data until 2024-02 if the forecast starts on 2024-03-01).

2. **Forecasting Period:**  
   Forecasts are generated for a defined future period (e.g., from 2024-03-01 to 2024-05-31).

3. **Actual Sales Data:**  
   The API extracts the actual sales for the forecast period from the full dataset. These actual values are then compared with the forecasts.

4. **Computation:**  
   MAE, RMSE, and MAPE are calculated by comparing the forecasted values to the actual values, providing quantitative measures of the forecasting accuracy.

#### **Sample Error Metrics JSON Output**

```json
[
  {
    "ProductName": "T-Shirt",
    "Duration": "2026-02-01 - 2026-04-30",
    "Forecast": 489.55,
    "Actual Sales": 0.0,
    "Error Metrics": {
      "MAE": 163.18,
      "RMSE": 163.36,
      "MAPE": "0.0%"
    }
  }
]
```

*Note:* In this example, even though **Actual Sales** are 0, the MAE and RMSE still reflect the forecast error magnitude, while MAPE is displayed as 0.0% to avoid division by zero.

---

## 🛠️ Key Functions

### **🔹 `preprocess_data()`**

- Reads CSV file.
- Extracts and aggregates sales data per **product per month**.
- Handles duplicate product entries by summing sales.

### **🔹 `predict_sales_forecasting()`**

- Converts processed data into a Pandas DataFrame.
- Uses **Facebook Prophet** for forecasting.
- Returns JSON predictions that include forecast, last year's actual sales, and percentage change.

### **🔹 `create_error_metrics()`**

- Trains the forecasting model using historical data **up to the forecast start date**.
- Generates forecasts for a specified period.
- Extracts the actual sales for the forecast period from the full dataset.
- Calculates error metrics (MAE, RMSE, MAPE) to assess forecast accuracy.
- Returns a JSON response with forecast, actual sales, and error metrics.

---

## 📌 Future Enhancements

- ✅ **Database integration** for storing past forecasts.
- ✅ **Additional seasonality adjustments** in Prophet.
- ✅ **Interactive UI for uploading CSV files.**
- ✅ **Dockerize the application** for easy deployment.

---

## 🌆 Developed By

👨‍💻 **AIBarista**  
📧 192158931+aibarista@users.noreply.github.com

---

## ⚠️ License

This project is **open-source** under the **MIT License**.
```

This `README.md` file now includes a dedicated **Error Metrics** section alongside all other necessary project information.