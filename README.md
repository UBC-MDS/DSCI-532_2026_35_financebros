# DSCI-532_2026_35_financebros
Dashboard for stonks

## About

The financebros dashboard is a web application that tracks key financial metrics regarding a portfolio comprised of the Magnificent Seven stocks: Apple, Microsoft, Amazon, Alphabet (Google’s parent company), Meta, Nvidia, and Tesla. The dashboard provides users with insights into the performance of these stocks, including price trends, volatility, and other relevant financial indicators. It also compares the performance of the portfolio against the S&P 500 index.
## For Developers

To set up and run the dashboard locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UBC-MDS/DSCI-532_2026_35_financebros.git
   ```

2. **Navigate to the repository folder:**
   ```bash
   cd DSCI-532_2026_35_financebros
   ```

3. **Create the conda environment:**
   ```bash
   conda env create -f environment.yml
   ```

4. **Activate the environment:**
   ```bash
   conda activate financebros
   ```

5. **Run the Shiny app:**
   ```bash
   shiny run src/app.py
   ```

The dashboard will be available at the URL shown in the terminal (typically `http://127.0.0.1:8000`).
