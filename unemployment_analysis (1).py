"""
=====================================================================
 UNEMPLOYMENT ANALYSIS WITH PYTHON
=====================================================================
A complete, beginner-friendly Data Analysis project examining India's
unemployment rate, the impact of COVID-19, and seasonal patterns.

Academic / Internship / College Submission

DATASET USED:
"Unemployment in India" — a real, publicly available dataset
(state-wise, rural/urban split, monthly, May 2019 - June 2020).
File expected at: data/Unemployment_in_India.csv

WHAT THIS SCRIPT DOES (in order):
 1. Imports libraries
 2. Loads and inspects the raw dataset
 3. Cleans the data (missing values, duplicates, dtypes, column names)
 4. Performs Exploratory Data Analysis (EDA)
 5. Creates visualizations (trend lines, bar charts, heatmap, etc.)
 6. Analyzes COVID-19 impact (pre-COVID vs COVID-period)
 7. Analyzes seasonal/monthly trends
 8. Prints key, data-driven findings
 9. Saves every chart + a cleaned CSV + a findings summary to /outputs

Run it with:   python unemployment_analysis.py
=====================================================================
"""

# =====================================================================
# SECTION 1: IMPORT LIBRARIES
# =====================================================================
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # save plots to file without needing a display
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

DATA_PATH = "data/Unemployment_in_India.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =====================================================================
# SECTION 2: LOAD & FIRST INSPECTION OF THE RAW DATA
# =====================================================================
print("=" * 70)
print("SECTION 2: LOADING & FIRST INSPECTION")
print("=" * 70)

raw_df = pd.read_csv(DATA_PATH)

print(f"\nRaw shape (rows, columns): {raw_df.shape}")
print(f"\nRaw column names:\n{list(raw_df.columns)}")
print(f"\nRaw data types:\n{raw_df.dtypes}")
print(f"\nMissing values per column (raw):\n{raw_df.isnull().sum()}")
print(f"\nFully-duplicated rows (raw): {raw_df.duplicated().sum()}")
print("\nFirst 5 raw rows:")
print(raw_df.head())


# =====================================================================
# SECTION 3: DATA CLEANING
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 3: DATA CLEANING")
print("=" * 70)

df = raw_df.copy()

# --- 3.1 Clean column names -----------------------------------------
# The raw file has extra spaces in column names (e.g. " Date",
# " Frequency"). We strip whitespace and rename to short, consistent,
# snake_case names so the rest of the code is easy to read.
df.columns = [c.strip() for c in df.columns]
print("\nStep 1: Stripped whitespace from column names.")

rename_map = {
    "Region": "region",
    "Date": "date",
    "Frequency": "frequency",
    "Estimated Unemployment Rate (%)": "unemployment_rate",
    "Estimated Employed": "employed",
    "Estimated Labour Participation Rate (%)": "labour_participation_rate",
    "Area": "area",
}
df.rename(columns=rename_map, inplace=True)
print(f"Step 2: Renamed columns to: {list(df.columns)}")

# --- 3.2 Drop fully-empty rows ---------------------------------------
# The raw CSV file ends with a block of completely blank rows (a common
# artifact of how the file was exported). These carry no information
# and must be removed before any analysis.
empty_rows_before = df.isnull().all(axis=1).sum()
df.dropna(how="all", inplace=True)
print(f"\nStep 3: Removed {empty_rows_before} fully-empty rows.")

# --- 3.3 Strip whitespace from text/string columns --------------------
# Values like " Andhra Pradesh" or " Rural" have leading spaces because
# of how the CSV was written (space after each comma). This would make
# groupby()/value_counts() treat "Rural" and " Rural" as different
# categories, so we strip every text column.
text_cols = df.select_dtypes(include=["object", "str"]).columns.tolist()
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
print(f"Step 4: Stripped whitespace from text columns: {text_cols}")

# --- 3.4 Handle remaining missing values -------------------------------
missing_after_dropna = df.isnull().sum()
print(f"\nStep 5: Missing values after removing empty rows:\n{missing_after_dropna}")
# Any row still missing the core unemployment_rate value cannot be used
# for rate-based analysis, so such rows (if any) are dropped. Numeric
# columns are NOT filled with fake/guessed values — that would fabricate
# data, so we only remove rows that are unusable.
before_rate_drop = len(df)
df = df.dropna(subset=["unemployment_rate", "date"])
print(f"Step 6: Dropped {before_rate_drop - len(df)} rows still missing "
      f"'unemployment_rate' or 'date' (cannot be analyzed).")

# --- 3.5 Remove duplicate rows -----------------------------------------
dupes = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"\nStep 7: Removed {dupes} exact duplicate rows.")

# --- 3.6 Fix data types --------------------------------------------------
# Convert the date column (currently text, format dd-mm-yyyy) into a
# proper datetime type, which allows time-based analysis (sorting,
# resampling by month, extracting year/month, etc.)
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
bad_dates = df["date"].isnull().sum()
df = df.dropna(subset=["date"])
print(f"\nStep 8: Converted 'date' to datetime format. "
      f"Dropped {bad_dates} rows with unparseable dates.")

df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")
df["employed"] = pd.to_numeric(df["employed"], errors="coerce")
df["labour_participation_rate"] = pd.to_numeric(df["labour_participation_rate"], errors="coerce")
print("Step 9: Ensured numeric columns are proper float/int types.")

# --- 3.7 Standardize categorical text (inconsistent casing/labels) ------
df["region"] = df["region"].str.title()
df["area"] = df["area"].str.title()
df["frequency"] = df["frequency"].str.title()
print("Step 10: Standardized text casing for region/area/frequency "
      "(e.g. 'RURAL' and 'rural' both become 'Rural').")

# --- 3.8 Derived time columns -------------------------------------------
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.strftime("%b")
df.sort_values("date", inplace=True)
df.reset_index(drop=True, inplace=True)
print("Step 11: Added 'year', 'month', and 'month_name' columns derived "
      "from 'date' for time-based grouping.")

# --- 3.9 Outlier investigation (not automatic removal) -------------------
# We only INVESTIGATE outliers here, we do not blindly delete them.
# An unusually high unemployment rate during COVID-19 (e.g. 70%+ in a
# specific state in April/May 2020) is a REAL economic event, not a
# data-entry error, so removing it would hide the very signal this
# project is trying to study. We use the IQR method purely to report
# how many such extreme points exist.
q1 = df["unemployment_rate"].quantile(0.25)
q3 = df["unemployment_rate"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df[(df["unemployment_rate"] < lower_bound) | (df["unemployment_rate"] > upper_bound)]
print(f"\nStep 12: Outlier check (IQR method) on unemployment_rate:")
print(f"  Normal range approx: {lower_bound:.2f}% to {upper_bound:.2f}%")
print(f"  Data points flagged as statistical outliers: {len(outliers)} "
      f"out of {len(df)} rows ({len(outliers)/len(df)*100:.1f}%).")
print("  These are KEPT in the dataset because they largely correspond to "
      "the COVID-19 lockdown months, which is exactly the event this "
      "project studies — deleting them would hide the real pattern.")

print(f"\nFinal cleaned shape (rows, columns): {df.shape}")
print(f"Final date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Number of unique regions/states: {df['region'].nunique()}")
print(f"Area categories: {df['area'].unique().tolist()}")

# Save the cleaned dataset for transparency / reuse
df.to_csv(f"{OUTPUT_DIR}/cleaned_unemployment_data.csv", index=False)
print(f"\nCleaned dataset saved to {OUTPUT_DIR}/cleaned_unemployment_data.csv")


# =====================================================================
# SECTION 4: EXPLORATORY DATA ANALYSIS (EDA)
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 4: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

overall_avg = df["unemployment_rate"].mean()
overall_min = df["unemployment_rate"].min()
overall_max = df["unemployment_rate"].max()

print(f"\nOverall average unemployment rate: {overall_avg:.2f}%")
print(f"Minimum unemployment rate recorded: {overall_min:.2f}%")
print(f"Maximum unemployment rate recorded: {overall_max:.2f}%")

min_row = df.loc[df["unemployment_rate"].idxmin()]
max_row = df.loc[df["unemployment_rate"].idxmax()]
print(f"\nLowest unemployment record  : {min_row['region']} "
      f"({min_row['area']}) on {min_row['date'].date()} -> {min_row['unemployment_rate']:.2f}%")
print(f"Highest unemployment record : {max_row['region']} "
      f"({max_row['area']}) on {max_row['date'].date()} -> {max_row['unemployment_rate']:.2f}%")

# Average unemployment by region (state)
region_avg = df.groupby("region")["unemployment_rate"].mean().sort_values(ascending=False)
print("\n--- Average unemployment rate by region (Top 5 highest) ---")
print(region_avg.head())
print("\n--- Average unemployment rate by region (Top 5 lowest) ---")
print(region_avg.tail())

# Average unemployment over time (monthly, across all regions)
monthly_avg = df.groupby(pd.Grouper(key="date", freq="MS"))["unemployment_rate"].mean()
print("\n--- Average unemployment rate by month (all regions combined) ---")
print(monthly_avg)

highest_month = monthly_avg.idxmax()
lowest_month = monthly_avg.idxmin()
print(f"\nHighest average-unemployment month: {highest_month.strftime('%B %Y')} "
      f"-> {monthly_avg.max():.2f}%")
print(f"Lowest average-unemployment month : {lowest_month.strftime('%B %Y')} "
      f"-> {monthly_avg.min():.2f}%")

# Rural vs Urban comparison, if the area column has real data
area_avg = None
if df["area"].nunique() > 1:
    area_avg = df.groupby("area")["unemployment_rate"].mean().sort_values(ascending=False)
    print("\n--- Average unemployment rate by Area (Rural vs Urban) ---")
    print(area_avg)


# =====================================================================
# SECTION 5: DATA VISUALIZATION
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 5: DATA VISUALIZATION (charts saved to /outputs)")
print("=" * 70)

# 5.1 Overall unemployment trend line (monthly average, all India)
plt.figure(figsize=(10, 5))
plt.plot(monthly_avg.index, monthly_avg.values, marker="o", color="#2c6e91", linewidth=2)
plt.title("Overall Unemployment Rate Trend Over Time (India, Monthly Average)")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/1_overall_trend.png")
plt.close()

# 5.2 Regional comparison - trend lines for a readable subset (top 6 by avg)
top_regions = region_avg.head(6).index.tolist()
plt.figure(figsize=(11, 6))
for region in top_regions:
    sub = df[df["region"] == region].groupby("date")["unemployment_rate"].mean()
    plt.plot(sub.index, sub.values, marker=".", label=region)
plt.title("Unemployment Rate Over Time — Top 6 Highest-Average States")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend(title="Region", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/2_regional_trend_top6.png")
plt.close()

# 5.3 Bar chart: average unemployment rate by region (all states)
plt.figure(figsize=(9, 10))
region_avg.sort_values().plot(kind="barh", color="#4c8caf")
plt.title("Average Unemployment Rate by Region")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/3_avg_unemployment_by_region.png")
plt.close()

# 5.4 Rural vs Urban comparison bar chart (if available)
if area_avg is not None:
    plt.figure(figsize=(6, 5))
    area_avg.plot(kind="bar", color=["#e07a5f", "#3d5a80"])
    plt.title("Average Unemployment Rate: Rural vs Urban")
    plt.xlabel("Area")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/4_rural_vs_urban.png")
    plt.close()

# 5.5 Seasonal / monthly trend visualization (average by calendar month)
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthwise_avg = df.groupby("month_name")["unemployment_rate"].mean().reindex(month_order).dropna()
plt.figure(figsize=(9, 5))
sns.barplot(x=monthwise_avg.index, y=monthwise_avg.values, hue=monthwise_avg.index,
            palette="viridis", legend=False)
plt.title("Average Unemployment Rate by Calendar Month (Seasonality Check)")
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/5_seasonal_monthwise.png")
plt.close()

# 5.6 Heatmap: Region x Month average unemployment rate
pivot = df.pivot_table(index="region", columns=df["date"].dt.strftime("%Y-%m"),
                        values="unemployment_rate", aggfunc="mean")
plt.figure(figsize=(14, 10))
sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.3, linecolor="white",
            cbar_kws={"label": "Unemployment Rate (%)"})
plt.title("Heatmap: Unemployment Rate by Region and Month")
plt.xlabel("Month")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/6_region_month_heatmap.png")
plt.close()

print("Saved 6 charts: overall trend, regional trend, region bar chart,")
print("rural-vs-urban bar chart, seasonal month-wise chart, and heatmap.")


# =====================================================================
# SECTION 6: COVID-19 IMPACT ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 6: COVID-19 IMPACT ANALYSIS")
print("=" * 70)

# India's nationwide COVID-19 lockdown began 25 March 2020. We define:
#   Pre-COVID  : all dates before 2020-03-25
#   COVID period: 2020-03-25 onward (all remaining data in this dataset,
#                 since the dataset ends in mid-2020, there isn't enough
#                 later data to separate a distinct "post-COVID recovery"
#                 phase — this limitation is stated honestly below)
covid_start = pd.Timestamp("2020-03-25")

pre_covid = df[df["date"] < covid_start]
covid_period = df[df["date"] >= covid_start]

pre_covid_avg = pre_covid["unemployment_rate"].mean()
covid_avg = covid_period["unemployment_rate"].mean()
pct_change = ((covid_avg - pre_covid_avg) / pre_covid_avg) * 100

print(f"\nPre-COVID period   : {pre_covid['date'].min().date()} to {pre_covid['date'].max().date()}"
      f"  ({len(pre_covid)} records)")
print(f"COVID period        : {covid_period['date'].min().date()} to {covid_period['date'].max().date()}"
      f"  ({len(covid_period)} records)")

print(f"\nAverage unemployment rate — Pre-COVID : {pre_covid_avg:.2f}%")
print(f"Average unemployment rate — COVID     : {covid_avg:.2f}%")
print(f"Change: {covid_avg - pre_covid_avg:+.2f} percentage points "
      f"({pct_change:+.1f}% relative change)")

if covid_avg > pre_covid_avg:
    direction = "INCREASED"
else:
    direction = "DECREASED"
print(f"\nConclusion: unemployment {direction} during the COVID period "
      f"compared to pre-COVID, based on this dataset.")

# Note on post-COVID data availability
last_date = df["date"].max()
print(f"\nNote: This dataset only extends to {last_date.date()}. There is not "
      f"enough data beyond mid-2020 to reliably analyze a separate "
      f"'post-COVID recovery' phase, so this analysis is limited to a "
      f"pre-COVID vs COVID-period comparison. This limitation is stated "
      f"explicitly rather than inventing recovery-phase numbers.")

# Region-wise COVID impact: which regions were hit hardest?
region_pre = pre_covid.groupby("region")["unemployment_rate"].mean()
region_covid = covid_period.groupby("region")["unemployment_rate"].mean()
region_impact = pd.DataFrame({
    "pre_covid_avg": region_pre,
    "covid_avg": region_covid,
}).dropna()
region_impact["change_pp"] = region_impact["covid_avg"] - region_impact["pre_covid_avg"]
region_impact["pct_change"] = (region_impact["change_pp"] / region_impact["pre_covid_avg"]) * 100
region_impact.sort_values("change_pp", ascending=False, inplace=True)

print("\n--- Regions with the LARGEST increase in unemployment (COVID vs Pre-COVID) ---")
print(region_impact.head(5)[["pre_covid_avg", "covid_avg", "change_pp"]].round(2))

print("\n--- Regions with the SMALLEST change / least affected ---")
print(region_impact.tail(5)[["pre_covid_avg", "covid_avg", "change_pp"]].round(2))

# COVID impact visualization
plt.figure(figsize=(7, 5))
comparison_data = pd.Series({"Pre-COVID": pre_covid_avg, "COVID Period": covid_avg})
comparison_data.plot(kind="bar", color=["#3d5a80", "#e07a5f"])
plt.title("Average Unemployment Rate: Pre-COVID vs COVID Period")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=0)
for i, v in enumerate(comparison_data.values):
    plt.text(i, v + 0.3, f"{v:.2f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/7_covid_comparison.png")
plt.close()

plt.figure(figsize=(9, 8))
top_impact = region_impact.head(10).sort_values("change_pp")
top_impact["change_pp"].plot(kind="barh", color="#c1121f")
plt.title("Top 10 Most-Affected Regions (Increase in Unemployment, COVID vs Pre-COVID)")
plt.xlabel("Increase in Unemployment Rate (percentage points)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/8_most_affected_regions.png")
plt.close()

print("\nSaved: 7_covid_comparison.png, 8_most_affected_regions.png")


# =====================================================================
# SECTION 7: SEASONAL TREND ANALYSIS
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 7: SEASONAL TREND ANALYSIS")
print("=" * 70)

print("\nAverage unemployment rate by calendar month (across all available years):")
print(monthwise_avg.round(2))

seasonal_high = monthwise_avg.idxmax()
seasonal_low = monthwise_avg.idxmin()
print(f"\nHighest-average month : {seasonal_high} -> {monthwise_avg.max():.2f}%")
print(f"Lowest-average month  : {seasonal_low} -> {monthwise_avg.min():.2f}%")

n_years = df["year"].nunique()
years_per_month = df.groupby("month_name")["year"].nunique().reindex(month_order)
months_with_repeat = years_per_month[years_per_month >= 2].index.tolist()

print(f"\nNumber of distinct calendar years touched by the data: {n_years} "
      f"({sorted(df['year'].unique())})")
print(f"\nYears of coverage per calendar month:\n{years_per_month}")

if len(months_with_repeat) == 0:
    print("\nIMPORTANT: No calendar month is covered in more than one year "
          "in this dataset, so a genuine recurring seasonal pattern CANNOT "
          "be confirmed (a real seasonal claim needs the SAME month to "
          "repeat across multiple years). The month-wise averages above "
          "are reported as descriptive information only.")
else:
    print(f"\nIMPORTANT: Only {months_with_repeat} are covered in more than "
          f"one year ({years_per_month[months_with_repeat].to_dict()}); every "
          f"other month has data from only a single year. This means the "
          f"dataset is NOT long enough to reliably confirm a general "
          f"recurring seasonal cycle across all 12 months — the sharp "
          f"April/May spike visible above is very likely the COVID-19 "
          f"shock rather than normal seasonality, since it only exists in "
          f"the 2020 data. For the two months that do repeat "
          f"({months_with_repeat}), we can make a direct year-over-year "
          f"comparison:")
    for m in months_with_repeat:
        vals = df[df["month_name"] == m].groupby("year")["unemployment_rate"].mean()
        print(f"  {m}: {dict(vals.round(2))}")
    print("A longer, multi-year dataset would be needed to properly confirm "
          "or rule out seasonality for the remaining 10 months.")


# =====================================================================
# SECTION 8: KEY FINDINGS (data-driven, printed for the report)
# =====================================================================
print("\n" + "=" * 70)
print("SECTION 8: KEY FINDINGS")
print("=" * 70)

findings = f"""
1. Overall average unemployment rate across the dataset: {overall_avg:.2f}%
   (ranging from {overall_min:.2f}% to {overall_max:.2f}%).

2. The single highest unemployment record was {max_row['unemployment_rate']:.2f}%
   in {max_row['region']} ({max_row['area']}) on {max_row['date'].date()}.

3. The single lowest unemployment record was {min_row['unemployment_rate']:.2f}%
   in {min_row['region']} ({min_row['area']}) on {min_row['date'].date()}.

4. The month with the highest average unemployment (all regions) was
   {highest_month.strftime('%B %Y')} at {monthly_avg.max():.2f}%.

5. The month with the lowest average unemployment (all regions) was
   {lowest_month.strftime('%B %Y')} at {monthly_avg.min():.2f}%.

6. Most-affected region during COVID (largest increase):
   {region_impact.index[0]} (+{region_impact.iloc[0]['change_pp']:.2f} percentage points).

7. Least-affected region during COVID (smallest change):
   {region_impact.index[-1]} ({region_impact.iloc[-1]['change_pp']:+.2f} percentage points).

8. Unemployment {direction} during the COVID period vs pre-COVID
   ({pre_covid_avg:.2f}% -> {covid_avg:.2f}%, a change of {pct_change:+.1f}%).
"""
if area_avg is not None:
    findings += (f"\n9. Between Rural and Urban areas, "
                 f"{area_avg.index[0]} had the higher average unemployment "
                 f"rate ({area_avg.iloc[0]:.2f}%) compared to "
                 f"{area_avg.index[-1]} ({area_avg.iloc[-1]:.2f}%).\n")

findings += (f"\n10. Seasonal pattern: only {months_with_repeat if months_with_repeat else 'no months'} "
             f"of the calendar year are covered by more than one year of data in "
             f"this dataset, so a general recurring seasonal trend across all "
             f"12 months cannot be confirmed. The large April/May spike is most "
             f"likely the COVID-19 disruption, not normal seasonality, since it "
             f"appears only in the 2020 data.\n")

print(findings)

with open(f"{OUTPUT_DIR}/key_findings.txt", "w") as f:
    f.write("UNEMPLOYMENT ANALYSIS - KEY FINDINGS\n")
    f.write("=" * 50 + "\n")
    f.write(findings)

print(f"Key findings saved to {OUTPUT_DIR}/key_findings.txt")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE. All charts and outputs saved inside 'outputs/'.")
print("=" * 70)
