### Section 1: Motivation and Purpose

rubric={reasoning:10}

Briefly explain the "Why":

- **Target Audience:** Who are they and what role are you embodying?
- **Problem:** What challenge are they facing?
- **Solution:** How will your dashboard help them solve it?

### Section 2: Description of the Data

rubric={reasoning:8}

Describe the dataset you finalized in Step 1.

- **Stats:** Number of rows/columns.
- **Relevance:** How variables potentially link to the problem.

### Section 3: Research Questions & Usage Scenarios

rubric={reasoning:10}

Detail how the audience will interact with the app.

- **Persona:** Brief description of a user.
- **Usage Scenario** create a narrative describing user needs and context.
- **User Stories / JTBD:** Provide **at least 3** User Stories or Job Stories that outline specific tasks the user needs to perform.

- **Persona - Daniel Chen**
Daniel is a data-driven retail investor working as tech professional, specifically as a data science instructor for MDS, he is an intermediate retail trader with goals of comparing top tech stocks efficiently and making informed long-term investment decisions. He struggles to consolidate information as financial data is scattered across multiple websites and hes overwhelmed by raw financial statements. He has been losing consistently and wants to trace where he went wrong.

- **Usage scenario**
Daniel is reviewing his investment portfolio after noticing that most of his holdings are concentrated in large-cap tech stocks. He wants to better understand how the Magnificent 7 stocks compare across valuation, profitability, and performance metrics. Instead of checking multiple financial websites, Alex opens the dashboard. He filters the time range to the past 3 years and examines price performance trends, P/E ratios and revenue growth, market cap comparison, and volatility metrics. The dashboard enables him to make a data-backed decision in minutes instead of hours.

- **User Stories / Jobs To Be Done (JTBD)**
User story 1 – Performance Comparison: As an investor and I want to compare historical stock performance across the Magnificent 7, so that I can identify which companies are leading or lagging over a selected time period, and also compare these stocks to the S&P 500 so I can understand how top tech stocks compare.

User Story 2 – Valuation Analysis: As a valuation-focused trader, I want to compare key metrics of booming tech stocks, specfically metrics such as P/E ratio, earnings growth, and revenue growth side-by-side, so that I can assess whether a stock appears overvalued or undervalued relative to the market and to other similar tech stocks.

### Section 4: Exploratory Data Analysis

rubric={reasoning:10}

Demonstrate that your data can actually support your user stories.

- Select **one** of your User Stories/JTBD from Section 3.
- Create a Jupyter notebook in the `notebooks/` folder (e.g., `notebooks/eda_analysis.ipynb`).
  - Create 1-2 static visualizations or summary tables that directly address the user's task.
- In your proposal document (this section), briefly explain what the visualization shows and how comparing these values specifically supports the user's decision-making.
  - _(Include the relevant plots or a link to the notebook in this section)._