# 📈 NIFTY 50 Volatility Forecasting: Unveiling Market Dynamics with GARCH

Welcome to a journey through the ups and downs of the Indian stock market! This project dives deep into the NIFTY 50 index, forecasting its volatility using the power of GARCH models, Apache Spark, and stunning visualizations. Whether you're a data enthusiast, a financial analyst, or a curious coder, this project offers insights into market behavior with a blend of statistical modeling and big data magic.

---

## 🌟 What’s This Project About?

Imagine trying to predict the heartbeat of the stock market—its volatility. That’s exactly what this project does for the NIFTY 50 index, India’s benchmark stock market index. Using historical data from 2014 to 2024, we:

- **Process massive datasets** with Apache Spark to compute log returns and range-based volatility.
- **Forecast future volatility** with a GARCH(1,1) model, revealing patterns in market turbulence.
- **Visualize trends** with Plotly (interactive HTML plots) and Seaborn (static PNGs), making the data come alive.
- **Query insights** with Spark SQL to uncover high-volatility days and market trends.

This isn’t just about numbers—it’s about understanding the rhythm of the market and equipping yourself with tools to anticipate its next move.

---

## 🛠️ Tech Stack: The Tools That Made It Happen

Here’s the lineup of technologies that powered this project:

- **Python 3.12.7 (Anaconda)**: The backbone of our coding adventure.
- **PySpark 3.5.0**: For distributed data processing and SQL queries on large datasets.
- **arch**: To fit and forecast with GARCH(1,1) models.
- **Plotly 6.1.0**: For interactive visualizations (saved as HTML due to Kaleido hiccups).
- **Seaborn & Matplotlib**: For crisp, static plots of volatility and volume trends.

---

## 📂 Project Structure: A Guided Tour

The project is organized for clarity and ease of use:

- **`data_fetch.py`**: Fetches and merges NIFTY 50 historical data (2014–2024) into `data/nifty50_historical.csv`.
- **`preprocess_spark.py`**: Uses Spark to compute log returns and range-based volatility, saving to `data/nifty50_processed.csv`.
- **`sql_queries.py`**: Runs Spark SQL queries to identify high-volatility days and more.
- **`garch_model.py`**: Fits a GARCH(1,1) model and forecasts 30-day volatility, saved to `data/garch_forecast.csv`.
- **`visualize.py`**: Creates stunning visualizations of trends, volatility, and forecasts.

### Outputs
- **Processed Data**: `data/nifty50_processed_single.csv` (log returns, range-based volatility).
- **Forecasts**: `data/garch_forecast.csv` (30-day volatility forecast).
- **Visualizations**:
  - `plots/closing_price_trend.html`: NIFTY 50 closing price trend (interactive Plotly HTML).
  - `plots/range_volatility.png`: Range-based volatility over time (Seaborn).
  - `plots/volume_vs_volatility.png`: Volume vs. volatility scatter plot (Seaborn).
  - `plots/forecasted_volatility.html`: 30-day forecasted volatility (interactive Plotly HTML).

---

## 🚀 How to Run This Project

Ready to dive in? Follow these steps to get the project up and running on your machine.

### Prerequisites
- Python 3.12.7 (Anaconda recommended).
- Apache Spark 3.5.0 (configured for Windows).
- Git (to clone the repository).

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Trishapaul5/nifty50_volatility_forecasting.git
   cd nifty50_volatility_forecasting

  📊 Key Insights from the GARCH Model
The GARCH(1,1) model revealed fascinating patterns in NIFTY 50 volatility:

High Volatility Persistence: alpha[1] + beta[1] = 0.9674, indicating that volatility tends to linger.
Significant Parameters:
ARCH term (alpha[1] = 0.1034): Recent shocks impact volatility.
GARCH term (beta[1] = 0.8640): Past volatility strongly influences future volatility.
Model Fit:
Log-Likelihood: -3508.04
AIC: 7024.08
These insights highlight the market’s volatility clustering—periods of calm followed by turbulent storms.
🌱 Future Enhancements
This project is just the beginning! Here are some ideas to take it further:

Extend the Data: Include 2025 data from NSE India for more recent insights.
Explore New Models: Try EGARCH or TGARCH for asymmetric volatility effects.
Build a Web App: Deploy with Flask or Streamlit to create an interactive dashboard for real-time forecasts.
🤝 Contributing
Found a bug or have an idea to improve this project? Feel free to open an issue or submit a pull request! Let’s make this project even better together.

📜 License
This project is licensed under the MIT License—see the LICENSE file for details.
👩‍💻 About the Author
Hi, I’m Trishapaul5! I’m passionate about data science, financial modeling, and building tools that make sense of complex systems. Connect with me on GitHub or LinkedIn to chat about markets, code, or anything in between!

Happy forecasting! 📉📈
