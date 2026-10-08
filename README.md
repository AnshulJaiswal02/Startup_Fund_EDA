# 🇮🇳 India Startup Funding Analysis

An end-to-end exploratory data analysis of Indian startup funding using Python, Pandas, NumPy, Matplotlib, and Seaborn.

The project analyzes startup funding patterns across **time, cities, industries, investment stages, deal sizes, startups, and investors**.

---

## 📌 Project Overview

This project explores an Indian startup funding dataset to understand how startup investments have evolved and where capital is concentrated.

### Key Questions

- How did startup funding change over time?
- Which cities attracted the most funding?
- Which industries received the most investment?
- Which funding stages were most common?
- What is the typical startup funding amount?
- Which startups received the most disclosed funding?
- Which investors appeared most frequently?
- Which city-industry combinations attracted the most funding?

---

## 📊 Dataset

The dataset contains information about Indian startup funding rounds, including:

- Startup Name
- Funding Date
- Funding Amount
- City
- Industry
- Investment Stage
- Investors

The analysis primarily covers the period from **2015 to early 2020**.

> **Note:** Many funding amounts are undisclosed. Therefore, funding-value analysis is based on available disclosed funding amounts.

---

## 🧹 Data Cleaning

The project performs several data preparation steps, including:

- Handling missing values
- Converting funding amounts into numerical format
- Standardizing city names
- Standardizing industry categories
- Cleaning investment-stage labels
- Extracting year from funding dates
- Splitting investor information
- Identifying potential data-quality issues
- Checking extreme funding values

---

## 📈 Analysis Performed

### 1. Data Quality Analysis

The dataset is examined for:

- Missing values
- Data types
- Duplicate or inconsistent entries
- Missing funding amounts
- Data-quality issues

---

### 2. Funding Trends Over Time

The project analyzes:

- Number of funding rounds by year
- Total disclosed funding by year
- Median funding amount
- Distribution of deal sizes

This helps identify changes in startup funding activity over time.

---

### 3. Funding by City

The analysis identifies major startup funding hubs in India.

Cities analyzed include:

- Bengaluru
- Mumbai
- New Delhi
- Gurugram
- Pune
- Hyderabad
- Chennai
- Noida

The analysis compares cities based on funding amount and number of funding rounds.

---

### 4. Funding by Industry

The project analyzes funding across different startup industries.

Examples include:

- E-Commerce
- FinTech
- Education
- Consumer Internet
- Technology
- Healthcare
- Transportation

The analysis identifies industries receiving the highest levels of disclosed funding.

---

### 5. Investment Stage Analysis

Funding rounds are analyzed across different investment stages, including:

- Seed
- Angel
- Pre-Series A
- Series A
- Series B
- Series C
- Private Equity
- Debt
- Venture
- Bridge
- Other

This provides an understanding of how startup capital is distributed across funding stages.

---

### 6. Deal Size Analysis

The project analyzes the distribution of funding amounts using:

- Mean
- Median
- Percentiles
- Distribution plots
- Outlier analysis

Because startup funding is highly skewed, the **median** provides a better representation of a typical funding round than the mean.

---

### 7. Top Funded Startups

Startups are ranked according to their cumulative disclosed funding.

The project also performs sanity checks on unusually large funding values to identify possible data-entry issues.

---

### 8. Investor Analysis

Investor data is cleaned and analyzed to identify investors appearing most frequently in the dataset.

The analysis also highlights the difference between:

> **Investor frequency and total investment value**

An investor participating in many rounds does not necessarily mean that they invested the largest total amount.

---

### 9. City × Industry Analysis

A heatmap is used to analyze funding concentration across cities and industries.

This helps identify major startup ecosystem clusters and understand how different industries are distributed geographically.

---

## 💡 Key Insights

### Funding Trends

Startup funding activity varies significantly across years, with certain periods showing substantially higher deal volumes.

### Geographic Concentration

Major startup funding activity is concentrated in a small number of Indian cities, particularly Bengaluru, Mumbai, and the Delhi-NCR region.

### Industry Concentration

Consumer Internet, Technology, E-Commerce, and FinTech represent major areas of startup funding activity in the dataset.

### Deal Size

Startup funding amounts are highly skewed. A relatively small number of very large funding rounds can significantly affect the average.

### Data Quality

Real-world datasets require extensive cleaning and validation before being used for business analysis.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

---

## 🧠 Skills Demonstrated

- Exploratory Data Analysis
- Data Cleaning
- Data Preprocessing
- Missing Value Analysis
- Data Transformation
- Feature Engineering
- GroupBy Analysis
- Statistical Analysis
- Data Visualization
- Outlier Detection
- Business Insight Generation

---

## 📁 Project Structure

```text
india-startup-funding-analysis/
│
├── startup_funding_analysis.ipynb
├── startup_funding.csv
├── dashboard/
│   └── index.html
│
├── prepare_dashboard_data.py
│
└── README.md
