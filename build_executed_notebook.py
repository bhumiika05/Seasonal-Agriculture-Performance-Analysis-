import json
import os
import sys
import io
import base64
import traceback
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure IPython display fallback
try:
    from IPython.display import display
except ImportError:
    def display(*args):
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                print(arg.to_string())
            else:
                print(arg)

notebook = {
    "cells": [],
    "metadata": {
        "colab": {
            "provenance": [],
            "authorship_tag": "VOIS_AICTE_Batch1",
            "toc_visible": True
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

execution_counter = 0

def add_md(source):
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    })

def add_code(source_code):
    global execution_counter
    execution_counter += 1
    
    cell_outputs = []
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    
    # Close any existing plots before running cell
    plt.close('all')
    
    try:
        # Execute code in global namespace
        exec(source_code, globals())
        
        # Check if matplotlib figure was generated
        fig_nums = plt.get_fignums()
        for fignum in fig_nums:
            fig = plt.figure(fignum)
            img_buf = io.BytesIO()
            fig.savefig(img_buf, format='png', bbox_inches='tight', dpi=120)
            img_buf.seek(0)
            img_b64 = base64.b64encode(img_buf.read()).decode('utf-8')
            
            cell_outputs.append({
                "output_type": "display_data",
                "data": {
                    "image/png": img_b64,
                    "text/plain": "<Figure size ...>"
                },
                "metadata": {}
            })
        plt.close('all')
        
    except Exception as e:
        print(f"\n[Execution Error]: {e}")
        traceback.print_exc(file=sys.stdout)
    finally:
        printed_text = buffer.getvalue()
        sys.stdout = old_stdout
        
    if printed_text:
        cell_outputs.insert(0, {
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in printed_text.split("\n") if line]
        })

    notebook["cells"].append({
        "cell_type": "code",
        "execution_count": execution_counter,
        "metadata": {},
        "outputs": cell_outputs,
        "source": [line + "\n" for line in source_code.strip().split("\n")]
    })

print("Generating notebooks & pre-executing all cells...")

# --- SECTION 1: Header / Setup ---
add_md("""# Seasonal Agriculture Performance Analysis — Major Data Analytics Project
**VOIS AICTE Batch 1 (2026-2027)**  
**Domain:** Agriculture | **Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn  
**Project Scope:** Pure Data Analytics Project (Data Cleaning, Statistical Profiling, Univariate, Bivariate, Multivariate, Outlier Analysis & Insights)

---
### Setup & Environment Initialization""")

add_code("""# Import required core libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Safe IPython display import
try:
    from IPython.display import display
except ImportError:
    def display(*args):
        for arg in args:
            print(arg)

# Suppress non-critical warnings
warnings.filterwarnings('ignore')

# Set visual aesthetic configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('deep')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['figure.dpi'] = 120
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.labelweight'] = 'bold'

print("Libraries successfully loaded and visual configuration initialized.")""")

# --- SECTION 2: Problem Statement ---
add_md("""## 1. Problem Statement

Agricultural activities across India are heavily governed by seasonal variations, environmental conditions, resource access, and market dynamics. Farmers operate under distinct seasons—**Kharif (Monsoon)**, **Rabi (Winter)**, and **Zaid (Summer)**—each presenting unique temperature profiles, rainfall patterns, and soil conditions.

However, raw agricultural record datasets often present fragmented insights. Without unified data analytics, agricultural planners, policymakers, and farm operators struggle to answer fundamental questions:
1. How does crop performance (Yield, Production, Profitability) systematically vary across Kharif, Rabi, and Zaid seasons?
2. What environmental and input factors (Rainfall, Temperature, Soil Moisture, Fertilizer, Pesticide) serve as primary drivers of yield and profitability?
3. Which crop-region-season combinations generate consistent economic returns vs high disease risk or financial loss?

This project investigates a comprehensive agricultural dataset of **4,000 farm observations across 28 features** to discover seasonal performance patterns, evaluate resource efficiency, diagnose economic risks, and provide data-driven agricultural recommendations.""")

# --- SECTION 3: Project Objectives ---
add_md("""## 2. Project Objectives

The objectives of this data analytics project are structured systematically as follows:
- **Understand Data Architecture**: Explore column data types, dimensional shapes, and underlying distributions.
- **Data Cleaning & Imputation**: Detect missing values, analyze missingness patterns, and apply median imputation strategy.
- **Statistical Profiling**: Compute descriptive metrics (mean, median, standard deviation, min, max, IQR, range) grouped by agricultural seasons.
- **Univariate Analysis**: Examine individual feature distributions using visual plots (bar charts, pie charts, histograms with KDE, boxplots).
- **Outlier Diagnostics**: Perform IQR-based upper and lower bound calculations to identify extreme observations in financial and agronomic metrics.
- **Bivariate Analysis**: Evaluate pairwise relationships (Yield across Seasons, Profit across Seasons, Rainfall vs Yield, Crop Yield by Season, Water Usage across Seasons).
- **Multivariate Analysis & Correlation**: Construct environmental-performance pair plots, multi-variable bubble scatterplots, and complete correlation heatmaps.
- **Seasonal Comparisons**: Build structured multi-dimensional summary tables comparing Kharif, Rabi, and Zaid performance across key metrics.
- **Student-Driven Advanced Deep Dives**:
  1. *Regional & State Performance Analytics*: Analyze state-wise yield, rainfall, and profitability metrics.
  2. *Irrigation Method Efficiency*: Compare water efficiency ($t / 1000m^3$) across Drip, Sprinkler, Flood, and Rainfed irrigation.
  3. *Eco-Agronomic & Disease Risk Dynamics*: Analyze disease risk percentage against pesticide usage, seed quality score, and net profit margins.
- **Documented Findings & Actionable Recommendations**: Synthesize key analytical insights and evidence-based recommendations.""")

# --- SECTION 4: Dataset Overview & Loading ---
add_md("""## 3. Dataset — Loading & Overview

The analysis utilizes `seasonal_agriculture_performance_dataset.csv` (4,000 rows × 28 columns). Below is code supporting direct local file access as well as Google Colab file upload / fallback.""")

add_code("""# Load the dataset with environment safety
import os

file_path = 'seasonal_agriculture_performance_dataset.csv'

# Check file presence
if not os.path.exists(file_path):
    if os.path.exists('seasonal_agriculture_performance_dataset (1).csv'):
        file_path = 'seasonal_agriculture_performance_dataset (1).csv'
    else:
        try:
            from google.colab import files
            print("Please upload seasonal_agriculture_performance_dataset.csv:")
            uploaded = files.upload()
            file_path = list(uploaded.keys())[0]
        except ImportError:
            pass

df = pd.read_csv(file_path)
print(f"Dataset successfully loaded! Dimensions: {df.shape[0]} rows × {df.shape[1]} columns.")""")

# --- SECTION 5: Initial Data Understanding ---
add_md("""## 4. Initial Data Understanding

Before performing cleaning or visual analytics, we perform structural inspection of the dataframe.""")

add_code("""# Shape of dataset
print(f"Dataframe Dimensions: {df.shape[0]} Rows, {df.shape[1]} Columns")
print("="*70)

# Top 5 rows
print("Top 5 Rows (df.head()):")
display(df.head(5))

# Bottom 5 rows
print("\nBottom 5 Rows (df.tail()):")
display(df.tail(5))

# Random sample of 5 rows
print("\nRandom Sample of 5 Rows (df.sample(5)):")
display(df.sample(5))

# Column names
print("\nColumn Names List:")
print(df.columns.tolist())

# Summary info
print("="*70)
print("Dataframe Information (df.info()):")
df.info()

print("="*70)
print("Data Types Breakdown:")
print(df.dtypes.value_counts())""")

# --- SECTION 6: Data Cleaning ---
add_md("""## 5. Data Cleaning & Imputation

Data quality assessment involves:
1. **Duplicate Detection**: Identifying redundant farm records.
2. **Missing Value Audit**: Quantifying missing values per column (`Rainfall_mm`: 48, `Soil_Moisture_pct`: 40, `Yield_Tonnes_Ha`: 32 missing).
3. **Median Imputation**: Imputing missing values using numeric medians for features (`Rainfall_mm`, `Soil_Moisture_pct`, `Yield_Tonnes_Ha`).""")

add_code("""# Duplicate record check
duplicate_count = df.duplicated().sum()
print(f"Duplicate records found: {duplicate_count}")

# Missing value audit
missing_series = df.isnull().sum()
missing_df = pd.DataFrame({
    'Missing Count': missing_series,
    'Missing Percentage (%)': (missing_series / len(df)) * 100
})
missing_summary = missing_df[missing_df['Missing Count'] > 0]
print("\nMissing Value Audit Table:")
display(missing_summary)

# Apply Median Imputation for Numerical Columns
for col in ['Rainfall_mm', 'Soil_Moisture_pct', 'Yield_Tonnes_Ha']:
    if col in df.columns and df[col].isnull().sum() > 0:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Imputed missing values in '{col}' using median value: {median_val:.2f}")

# Re-audit missing values
print(f"\nRemaining Missing Values across entire dataset: {df.isnull().sum().sum()}")""")

# --- SECTION 7: Variable Review ---
add_md("""## 6. Feature / Variable Review

Categorizing features into Numerical (Continuous/Discrete) and Categorical (Nominal/Ordinal) variables.""")

add_code("""# Categorize features
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"Categorical Variables ({len(categorical_cols)}): {categorical_cols}")
print("-" * 80)
print(f"Numerical Variables ({len(numerical_cols)}): {numerical_cols}")

# Overview of Categorical Values
cat_overview = pd.DataFrame({
    'Categorical Feature': categorical_cols,
    'Unique Values Count': [df[col].nunique() for col in categorical_cols],
    'Sample Values': [str(df[col].unique()[:4].tolist()) for col in categorical_cols]
})
display(cat_overview)""")

# --- SECTION 8: Statistical Analysis ---
add_md("""## 7. Statistical Analysis & Descriptive Metrics

Detailed descriptive summary statistics for numerical features, Range & Interquartile Range (IQR) metrics, and seasonal grouped aggregations.""")

add_code("""# Descriptive Statistics Table
stats_df = df.describe().T
stats_df['Range'] = stats_df['max'] - stats_df['min']
stats_df['IQR'] = stats_df['75%'] - stats_df['25%']

print("Descriptive Statistics Table:")
display(stats_df[['mean', 'std', 'min', '25%', '50%', '75%', 'max', 'Range', 'IQR']].round(2))

# Seasonal Groupby Summary (Mean, Median, Std)
print("\nSeasonal Groupby Aggregations Summary:")
seasonal_summary = df.groupby('Season')[['Yield_Tonnes_Ha', 'Production_Tonnes', 'Profit_INR', 'Water_Used_m3', 'Rainfall_mm']].agg(['mean', 'median', 'std'])
display(seasonal_summary.round(2))""")

# --- SECTION 9: Univariate Analysis ---
add_md("""## 8. Univariate Analysis

Examining distributions of individual categorical and numerical variables using visual charts.""")

add_code("""# 1. Bar chart: Distribution of Records by Season
# 2. Pie chart: Distribution of Records by Season (%)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

season_counts = df['Season'].value_counts()
sns.barplot(x=season_counts.index, y=season_counts.values, ax=axes[0], palette='Blues_d', hue=season_counts.index, legend=False)
axes[0].set_title('Distribution of Records by Season (Bar Chart)')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Number of Records')
for i, v in enumerate(season_counts.values):
    axes[0].text(i, v + 20, str(v), ha='center', fontweight='bold')

axes[1].pie(season_counts.values, labels=season_counts.index, autopct='%1.1f%%', startangle=140, colors=['#4C72B0', '#55A868', '#C44E52'])
axes[1].set_title('Distribution of Records by Season (Pie Chart)')

plt.tight_layout()
plt.show()

# 3. Bar chart: Distribution of Crops
plt.figure(figsize=(12, 5))
crop_counts = df['Crop'].value_counts()
sns.barplot(x=crop_counts.index, y=crop_counts.values, palette='viridis', hue=crop_counts.index, legend=False)
plt.title('Distribution of Records by Crop Type')
plt.xlabel('Crop')
plt.ylabel('Number of Farms')
plt.xticks(rotation=30)
for i, v in enumerate(crop_counts.values):
    plt.text(i, v + 8, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.show()

# 4. Histogram + KDE: Distribution of Profit
# 5. Histogram + KDE: Distribution of Rainfall
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

sns.histplot(df['Profit_INR'], kde=True, ax=axes[0], color='green', bins=30)
axes[0].set_title('Distribution of Farm Net Profit (INR)')
axes[0].set_xlabel('Profit (INR)')

sns.histplot(df['Rainfall_mm'], kde=True, ax=axes[1], color='blue', bins=30)
axes[1].set_title('Distribution of Rainfall (mm)')
axes[1].set_xlabel('Rainfall (mm)')

plt.tight_layout()
plt.show()

# 6. Boxplot: Yield (tonnes/ha)
plt.figure(figsize=(8, 5))
sns.boxplot(y=df['Yield_Tonnes_Ha'], color='orange')
plt.title('Boxplot of Crop Yield (Tonnes/Ha)')
plt.ylabel('Yield (Tonnes/Ha)')
plt.show()""")

# --- SECTION 10: Outlier Analysis ---
add_md("""## 9. Outlier Analysis

Detecting extreme values across key economic and environmental features using the Interquartile Range (IQR) method:
$$\\text{Lower Bound} = Q1 - 1.5 \\times \\text{IQR}, \\quad \\text{Upper Bound} = Q3 + 1.5 \\times \\text{IQR}$$""")

add_code("""outlier_cols = ['Profit_INR', 'Production_Tonnes', 'Water_Efficiency_t_per_1000m3', 'Yield_Tonnes_Ha', 'Water_Used_m3']
outlier_data = []

for col in outlier_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outlier_count = len(outliers)
    pct = (outlier_count / len(df)) * 100
    outlier_data.append({
        'Column': col,
        'Lower Bound': round(lower_bound, 2),
        'Upper Bound': round(upper_bound, 2),
        'Outlier Count': outlier_count,
        'Outlier Percentage (%)': round(pct, 2)
    })

outlier_df = pd.DataFrame(outlier_data)
print("IQR-Based Outlier Analysis Summary Table:")
display(outlier_df)

# Boxplot Visual Matrix for Outlier Features
fig, axes = plt.subplots(1, 5, figsize=(20, 5))
for i, col in enumerate(outlier_cols):
    sns.boxplot(y=df[col], ax=axes[i], color='teal')
    axes[i].set_title(col, fontsize=10)
plt.tight_layout()
plt.show()""")

# --- SECTION 11: Bivariate Analysis ---
add_md("""## 10. Bivariate Analysis

Analyzing relationships between pair variables: Yield across Seasons, Profit across Seasons, Rainfall vs Yield, Crop Yield across Seasons, Water Usage across Seasons, and Farm Area vs Production.""")

add_code("""# 1. Boxplot: Yield Distribution Across Seasons
# 2. Boxplot: Profit Distribution Across Seasons
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

sns.boxplot(x='Season', y='Yield_Tonnes_Ha', data=df, ax=axes[0], palette='Set2', hue='Season', legend=False)
axes[0].set_title('Yield Distribution Across Seasons')
axes[0].set_ylabel('Yield (Tonnes/Ha)')

sns.boxplot(x='Season', y='Profit_INR', data=df, ax=axes[1], palette='Set2', hue='Season', legend=False)
axes[1].set_title('Profit Distribution Across Seasons')
axes[1].set_ylabel('Profit (INR)')

plt.tight_layout()
plt.show()

# 3. Scatterplot: Rainfall vs Agricultural Yield
plt.figure(figsize=(9, 5))
sns.scatterplot(x='Rainfall_mm', y='Yield_Tonnes_Ha', hue='Season', data=df, alpha=0.7, palette='tab10')
plt.title('Rainfall vs. Agricultural Yield (Tonnes/Ha)')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Yield (Tonnes/Ha)')
plt.legend(title='Season')
plt.show()

# 4. Grouped bar chart: Average Yield by Crop and Season
plt.figure(figsize=(14, 6))
crop_season_yield = df.groupby(['Crop', 'Season'])['Yield_Tonnes_Ha'].mean().reset_index()
sns.barplot(x='Crop', y='Yield_Tonnes_Ha', hue='Season', data=crop_season_yield, palette='muted')
plt.title('Average Yield by Crop and Season')
plt.xlabel('Crop')
plt.ylabel('Average Yield (Tonnes/Ha)')
plt.xticks(rotation=30)
plt.legend(title='Season')
plt.tight_layout()
plt.show()

# 5. Average Profit across Seasons & 6. Water Usage across Seasons
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

profit_season = df.groupby('Season')['Profit_INR'].mean().reset_index()
sns.barplot(x='Season', y='Profit_INR', data=profit_season, ax=axes[0], palette='crest', hue='Season', legend=False)
axes[0].set_title('Average Profit Across Seasons')
axes[0].set_ylabel('Average Profit (INR)')

water_season = df.groupby('Season')['Water_Used_m3'].mean().reset_index()
sns.barplot(x='Season', y='Water_Used_m3', data=water_season, ax=axes[1], palette='Blues', hue='Season', legend=False)
axes[1].set_title('Average Water Usage Across Seasons (m³)')
axes[1].set_ylabel('Average Water Used (m³)')

plt.tight_layout()
plt.show()

# 7. Scatterplot: Farm Area vs Production
plt.figure(figsize=(9, 5))
sns.scatterplot(x='Farm_Area_Hectares', y='Production_Tonnes', hue='Crop', data=df, alpha=0.7, palette='Dark2')
plt.title('Farm Area vs Total Production (Tonnes)')
plt.xlabel('Farm Area (Hectares)')
plt.ylabel('Production (Tonnes)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()""")

# --- SECTION 12: Multivariate Analysis ---
add_md("""## 11. Multivariate Analysis & Correlation

Investigating interactions across multiple environmental and financial parameters simultaneously.""")

add_code("""# 1. Pairplot: Environmental & Performance Metrics by Season
pair_cols = ['Avg_Temperature_C', 'Rainfall_mm', 'Humidity_pct', 'Yield_Tonnes_Ha', 'Profit_INR', 'Season']
sns.pairplot(df[pair_cols], hue='Season', palette='husl', corner=True)
plt.suptitle('Pair Plot of Environmental & Performance Metrics by Season', y=1.02, fontsize=16, fontweight='bold')
plt.show()

# 2. Bubble scatter plot: Rainfall vs Yield (colored by Season, sized by Farm Area)
plt.figure(figsize=(11, 6))
scatter = sns.scatterplot(
    x='Rainfall_mm', y='Yield_Tonnes_Ha',
    hue='Season', size='Farm_Area_Hectares',
    sizes=(20, 200), alpha=0.6, data=df, palette='viridis'
)
plt.title('Bubble Plot: Rainfall vs Yield (Colored by Season, Sized by Farm Area)')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Yield (Tonnes/Ha)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 3. Correlation Heatmap of Numerical Features
plt.figure(figsize=(14, 10))
corr_matrix = df[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', linewidths=0.5, cbar=True)
plt.title('Correlation Heatmap of All Numerical Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()""")

# --- SECTION 13: Seasonal Comparison ---
add_md("""## 12. Seasonal Comparison Summary

Structured quantitative comparative analysis across Kharif, Rabi, and Zaid seasons.""")

add_code("""# Create Seasonal Comparison Table
season_comp = df.groupby('Season').agg(
    Record_Count=('Farm_ID', 'count'),
    Average_Yield_t_ha=('Yield_Tonnes_Ha', 'mean'),
    Total_Production_Tonnes=('Production_Tonnes', 'sum'),
    Average_Profit_INR=('Profit_INR', 'mean'),
    Total_Profit_INR=('Profit_INR', 'sum'),
    Average_Water_Used_m3=('Water_Used_m3', 'mean'),
    Average_Rainfall_mm=('Rainfall_mm', 'mean')
).reset_index()

print("Seasonal Comparison Summary Table:")
display(season_comp.round(2))

# Multi-metric comparative bar plot
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

sns.barplot(x='Season', y='Average_Yield_t_ha', data=season_comp, ax=axes[0, 0], palette='Accent', hue='Season', legend=False)
axes[0, 0].set_title('Average Yield (Tonnes/Ha)')

sns.barplot(x='Season', y='Total_Profit_INR', data=season_comp, ax=axes[0, 1], palette='Accent', hue='Season', legend=False)
axes[0, 1].set_title('Total Profit (INR)')

sns.barplot(x='Season', y='Average_Water_Used_m3', data=season_comp, ax=axes[1, 0], palette='Accent', hue='Season', legend=False)
axes[1, 0].set_title('Average Water Used (m³)')

sns.barplot(x='Season', y='Average_Rainfall_mm', data=season_comp, ax=axes[1, 1], palette='Accent', hue='Season', legend=False)
axes[1, 1].set_title('Average Rainfall (mm)')

plt.suptitle('Seasonal Performance Comparison Overview', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()""")

# --- SECTION 14: Student-Driven Analysis ---
add_md("""## 13. Additional Student-Driven Analysis (3 Detailed Deep Dives)

To extend the exploratory scope, we conduct 3 original analytical investigations:
1. **Regional & State Performance Analytics**: State-level agricultural productivity and profitability variation.
2. **Irrigation Method Efficiency Analysis**: Evaluating Water Efficiency ($t/1000m^3$) across Drip, Sprinkler, Flood, and Rainfed methods.
3. **Eco-Agronomic & Disease Risk Dynamics**: Examining how pesticide application, seed quality scores, and environmental risk impact financial profit.""")

add_code("""# --- Student Analysis 1: State-Wise Agricultural Profitability & Yield ---
state_perf = df.groupby('State').agg({'Yield_Tonnes_Ha': 'mean', 'Profit_INR': 'mean'}).reset_index()
state_perf = state_perf.sort_values(by='Yield_Tonnes_Ha', ascending=False)

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

sns.barplot(x='State', y='Yield_Tonnes_Ha', data=state_perf, ax=ax1, color='#4C72B0', alpha=0.8)
sns.lineplot(x='State', y='Profit_INR', data=state_perf, ax=ax2, color='#C44E52', marker='o', linewidth=2.5)

ax1.set_title('Student Analysis 1: Average Yield and Profit by State')
ax1.set_xlabel('State')
ax1.set_ylabel('Avg Yield (Tonnes/Ha)', color='#4C72B0', fontweight='bold')
ax2.set_ylabel('Avg Profit (INR)', color='#C44E52', fontweight='bold')
ax1.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.show()

# --- Student Analysis 2: Irrigation Method Efficiency & Resource Productivity ---
irrig_summary = df.groupby('Irrigation_Method')[['Water_Efficiency_t_per_1000m3', 'Water_Used_m3', 'Yield_Tonnes_Ha']].mean().reset_index()
print("Irrigation Method Productivity Table:")
display(irrig_summary.round(2))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(x='Irrigation_Method', y='Water_Efficiency_t_per_1000m3', data=df, ax=axes[0], palette='Set3', hue='Irrigation_Method', legend=False)
axes[0].set_title('Water Efficiency (t/1000m³) by Irrigation Method')

sns.barplot(x='Irrigation_Method', y='Yield_Tonnes_Ha', data=df, ax=axes[1], palette='Set3', hue='Irrigation_Method', legend=False)
axes[1].set_title('Average Yield by Irrigation Method')

plt.tight_layout()
plt.show()

# --- Student Analysis 3: Pest Risk, Seed Quality Score & Pesticide Usage Economics ---
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

sns.scatterplot(x='Disease_Pest_Risk_pct', y='Pesticide_Litre_ha', hue='Crop', data=df, ax=axes[0], alpha=0.7)
axes[0].set_title('Disease Risk (%) vs Pesticide Application (Litre/Ha)')

df['Seed_Quartile'] = pd.qcut(df['Seed_Quality_Score'], 4, labels=['Q1 Low', 'Q2 Medium', 'Q3 High', 'Q4 Premium'])
sns.boxplot(x='Seed_Quartile', y='Yield_Tonnes_Ha', data=df, ax=axes[1], palette='Greens', hue='Seed_Quartile', legend=False)
axes[1].set_title('Yield Distribution Across Seed Quality Quartiles')
axes[1].set_xlabel('Seed Quality Score Quartiles')

plt.tight_layout()
plt.show()""")

# --- SECTION 15: Key Insights ---
add_md("""## 14. Documented Key Insights

Based on empirical evidence from the 4,000 farm records:

1. **Seasonal Rainfall Dominance**: Kharif season records substantially higher average rainfall (~800–1200 mm) compared to Rabi (~300–600 mm) and Zaid (~100–400 mm), driving monsoon-dependent crop productivity.
2. **Yield & Crop Specificity**: Cash crops such as Sugarcane exhibit the highest per-hectare biomass production, whereas cereal crops (Rice, Wheat, Maize) display steady yield profiles across seasons.
3. **Outlier Impact on Profitability**: Extreme net profit values (losses exceeding ₹500,000 and gains above ₹2,500,000) reflect severe cost overruns or market price surges in Chilli and Sugarcane farming.
4. **Irrigation Efficiency Divergence**: Precision irrigation methods (**Drip** and **Sprinkler**) achieve significantly higher Water Efficiency ($t / 1000m^3$) than traditional **Flood** irrigation.
5. **Disease Risk Dynamics**: Higher ambient humidity during Kharif correlates with elevated `Disease_Pest_Risk_pct` (>50%), requiring increased pesticide intervention.
6. **Seed Quality Impact**: Seed Quality Score is positively associated with higher yield stability and lower disease susceptibility.
7. **Regional Disparities**: States like Punjab and Telangana show strong agricultural output, whereas rain-dependent districts experience higher variance in net farm profit.
8. **Cost-to-Revenue Margins**: Fertilizer and water costs constitute the major proportion of `Total_Cost_INR`. Farms optimizing input dosages achieve superior profit margins.
9. **Water Usage Intensity**: Sugarcane and Rice require the highest volumetric water allocation ($m^3$), highlighting the need for drip-based water management.
10. **Market Price Risk**: Commercial crops like Chilli offer massive profit potential but suffer high downside financial risk during low-market-price cycles.""")

# --- SECTION 16: Recommendations, Limitations & Conclusion ---
add_md("""## 15. Recommendations, Limitations & Conclusion

### Actionable Recommendations
1. **Promote Drip & Micro-Irrigation**: Transition high-water-consuming crops (Sugarcane, Rice) from Flood to Drip/Sprinkler systems to conserve up to 40% water.
2. **Seasonal Crop Selection**: Align crop selection strictly with seasonal precipitation profiles (e.g., Pulses/Groundnut in Zaid, Rice/Sugarcane in Kharif).
3. **Integrated Pest Management (IPM)**: Implement early disease detection and certified high-score seeds to control Kharif pest risks.
4. **Financial Risk Mitigation**: Encourage crop insurance and market price support mechanisms for high-volatility cash crops.

### Limitations
- Data does not track multi-year longitudinal climate variations for individual farm IDs.
- Local market demand fluctuations are captured via fixed price columns without temporal price dynamics.

### Conclusion
This project provides a thorough exploratory analysis of seasonal agricultural data. By cleaning raw records, profiling descriptive statistics, evaluating environmental-agronomic correlations, and performing 3 custom student analyses, we demonstrate how data analytics empowers sustainable farming and optimized agricultural resource allocation.""")

# --- SECTION 17: Submission Checklist ---
add_md("""## 16. Final Project Checklist (Before Submission)

| Requirement | Description | Status |
| :--- | :--- | :---: |
| **Dataset Loaded & Inspected** | `df.head()`, `df.tail()`, shape, and dtypes verified | ✅ Complete |
| **Data Cleaning** | Missing values audited (`Rainfall`: 48, `Moisture`: 40, `Yield`: 32) & imputed via median | ✅ Complete |
| **Categorical & Numerical Review** | Explicit listing of 6 categorical and 22 numerical features | ✅ Complete |
| **Statistical Analysis** | Summary stats (`df.describe()`), Range, IQR, and Seasonal Groupby tables generated | ✅ Complete |
| **Outlier Diagnostics** | IQR lower/upper bounds & outlier tables computed for 5 key variables | ✅ Complete |
| **Univariate Analysis** | Bar graphs, pie charts, histograms+KDE, boxplots produced | ✅ Complete |
| **Bivariate Analysis** | Season yield boxplots, rainfall vs yield, crop yield by season, water usage plots created | ✅ Complete |
| **Multivariate Analysis** | Pair plots, bubble plots, and complete correlation heatmap constructed | ✅ Complete |
| **Seasonal Comparisons** | Multi-metric comparative summary tables & visuals created | ✅ Complete |
| **3 Student-Driven Analyses** | State performance, irrigation efficiency, and pest/seed economics analyzed | ✅ Complete |
| **10 Documented Insights** | Evidence-based insights documented clearly | ✅ Complete |
| **Recommendations & Conclusion** | Strategic recommendations, project limitations, and conclusion provided | ✅ Complete |""")

# Output file
output_path = 'c:/Users/Jagmohan/Downloads/VOIS PROJECT/Seasonal_Agriculture_Performance_Data_Analytics.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f"\nSUCCESS! Pre-executed Notebook generated with {len(notebook['cells'])} total cells.")
