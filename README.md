# Seasonal Agriculture Performance Data Analytics & Streamlit Deployment

**VOIS AICTE Batch 1 (2026-2027) Major Project**

---

## 🌾 Project Overview

This repository contains an end-to-end Data Analytics project investigating seasonal variations in agricultural performance across India. Using a dataset of **4,000 farm records across 28 features**, the project explores environmental factors (rainfall, temperature, humidity, sunlight, soil moisture/pH), farming practices (fertilizer, pesticide, seed quality, irrigation methods), and economic outcomes (yield, production, cost, revenue, net profit, water efficiency).

The project includes:
1. **Google Colab Notebook (`Seasonal_Agriculture_Performance_Data_Analytics.ipynb`)**: Complete Data Analytics workflow featuring data cleaning, missing value imputation, statistical summaries, univariate/bivariate/multivariate visualizations, outlier analysis, 3 student-driven deep dives, 10 documented insights, and a submission checklist.
2. **Interactive Streamlit Web App (`app.py`)**: Web application featuring multi-dimensional filtering, top KPI metric cards, and 6 interactive analytics tabs.

---

## 📁 Repository Structure

```text
├── Seasonal_Agriculture_Performance_Data_Analytics.ipynb  # Main Google Colab Jupyter Notebook
├── app.py                                                 # Streamlit Web Application Script
├── seasonal_agriculture_performance_dataset.csv          # Project Dataset (4,000 rows × 28 cols)
├── requirements.txt                                       # Python dependencies for Streamlit Cloud
└── README.md                                              # Project Documentation & Deployment Guide
```

---

## 📊 Dataset Features Summary

The dataset comprises **4,000 farm records** with 28 variables:
- **Categorical (6)**: `Farm_ID`, `State`, `District`, `Crop`, `Season` (Kharif, Rabi, Zaid), `Irrigation_Method` (Drip, Sprinkler, Flood, Rainfed).
- **Environmental & Soil (7)**: `Rainfall_mm`, `Avg_Temperature_C`, `Humidity_pct`, `Sunlight_Hours_Day`, `Soil_pH`, `Soil_Moisture_pct`, `Disease_Pest_Risk_pct`.
- **Agronomic Inputs (5)**: `Nitrogen_kg_ha`, `Phosphorus_kg_ha`, `Potassium_kg_ha`, `Fertilizer_kg_ha`, `Pesticide_Litre_ha`, `Seed_Quality_Score`.
- **Output & Financial (10)**: `Farm_Area_Hectares`, `Yield_Tonnes_Ha`, `Production_Tonnes`, `Market_Price_INR_Tonne`, `Total_Cost_INR`, `Revenue_INR`, `Profit_INR`, `Water_Used_m3`, `Water_Efficiency_t_per_1000m3`.

---

## 🚀 How to Run the Google Colab Notebook

1. Download `Seasonal_Agriculture_Performance_Data_Analytics.ipynb` and `seasonal_agriculture_performance_dataset.csv`.
2. Open [Google Colab](https://colab.research.google.com/).
3. Click **Upload** and select `Seasonal_Agriculture_Performance_Data_Analytics.ipynb`.
4. Upload `seasonal_agriculture_performance_dataset.csv` to the Colab session files or let the notebook prompt for upload.
5. Select **Runtime > Run all** to execute the analysis and view all generated plots and tables.

---

## 💻 How to Run the Streamlit App Locally

### Prerequisites
Make sure Python 3.9+ is installed on your system.

### Steps
1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL displayed in your terminal (typically `http://localhost:8501`).

---

## 🌐 Step-by-Step GitHub & Streamlit Cloud Deployment Guide

### Step 1: Create a GitHub Repository
1. Open [GitHub](https://github.com/) and log in.
2. Click the **"+"** icon in the top right and select **New repository**.
3. Name your repository (e.g., `seasonal-agriculture-analytics`).
4. Set repository visibility to **Public**.
5. Do **not** initialize with a README if uploading existing local files. Click **Create repository**.

### Step 2: Push Project Files to GitHub
Open your terminal / PowerShell in the project directory and run:

```bash
# Initialize git repository
git init

# Add all project files
git add .

# Commit changes
git commit -m "Initial commit - Seasonal Agriculture Performance Data Analytics Project"

# Rename branch to main
git branch -M main

# Add remote origin (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/seasonal-agriculture-analytics.git

# Push code to GitHub
git push -u origin main
```

### Step 3: Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **New app**.
3. Fill in the deployment details:
   - **Repository**: `YOUR_USERNAME/seasonal-agriculture-analytics`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **Deploy!**
5. Your Streamlit web app will build and go live in ~1-2 minutes with a shareable public URL!

---

## 💡 Student-Driven Advanced Analyses Included

1. **State-Wise Regional Analytics**: Evaluates state-level variation in yield and profit per hectare across 8 Indian states.
2. **Irrigation Efficiency & Productivity**: Compares Water Efficiency ($t/1000m^3$) and Yield across Drip, Sprinkler, Flood, and Rainfed irrigation.
3. **Eco-Agronomic Risk Dynamics**: Analyzes disease pest risk against pesticide dosage, seed quality score quartiles, and net financial returns.

---

## 📋 Checklist Verification

- [x] Full Google Colab notebook `.ipynb` generated and validated.
- [x] Streamlit web application `app.py` created with sidebar filters, KPIs, and 6 tabs.
- [x] Data cleaning (missing value audit & median imputation) performed.
- [x] Univariate, Bivariate, Multivariate, and Outlier analysis included.
- [x] 3 custom student-driven analyses implemented.
- [x] 10 documented evidence-based insights included.
- [x] Actionable recommendations, limitations, and final conclusion documented.
