# Unemployment Analysis with Python

A complete, data-driven analysis of unemployment in India, focused on measuring
the impact of COVID-19 and checking for seasonal patterns — built for a
BCA internship / academic submission.

---

## 1. Project Title

**Unemployment Analysis with Python**

---

## 2. Introduction

Unemployment is one of the most important indicators used to judge the health
of an economy. It represents the percentage of people who are actively
looking for work but unable to find it. Tracking unemployment over time,
across regions, and around major events (like a pandemic) helps governments,
economists, and policymakers understand where support is needed most.

This project analyzes a real, publicly available Indian unemployment dataset
using Python, with the specific goal of understanding how COVID-19 affected
joblessness, whether unemployment follows any repeating seasonal pattern, and
which regions were hit hardest.

---

## 3. Problem Statement

India's labour market experienced a dramatic shock in early-to-mid 2020 due
to COVID-19 lockdowns. This project investigates:

- How much did unemployment actually change during the COVID period, and can
  this be measured precisely rather than assumed?
- Which Indian states/regions were affected the most, and which the least?
- Does unemployment show a recurring seasonal (monthly) pattern, independent
  of the COVID-19 shock?
- What data-driven insights can be drawn that are useful for economic and
  social policy discussions?

---

## 4. Objectives

1. Load and clean a real unemployment dataset.
2. Explore the data statistically (averages, extremes, distribution by
   region and time).
3. Visualize trends clearly using line charts, bar charts, and a heatmap.
4. Quantify the COVID-19 impact on unemployment using an actual pre/during
   comparison — not an assumption.
5. Check whether the data supports a genuine seasonal trend.
6. Summarize key findings and connect them to real-world policy relevance.

---

## 5. Dataset Description

**Dataset used:** *Unemployment in India* — a real, publicly available
dataset (state-wise, monthly, split by Rural/Urban area), sourced from a
public GitHub mirror of a well-known Kaggle dataset on Indian unemployment.
File location in this project: `data/Unemployment_in_India.csv`.

| Property | Value |
|---|---|
| Raw rows | 768 |
| Raw columns | 7 |
| Cleaned rows (after removing blanks/duplicates) | 740 |
| Date range (after cleaning) | 31 May 2019 – 30 June 2020 |
| Unique regions/states | 28 |
| Area categories | Rural, Urban |
| Frequency | Monthly |

**Original columns (raw):**
- `Region` — Indian state/union territory
- ` Date` — the reporting date (had a leading space in the raw file)
- ` Frequency` — reporting frequency (Monthly)
- ` Estimated Unemployment Rate (%)` — % of the labour force unemployed
- ` Estimated Employed` — estimated number of people employed
- ` Estimated Labour Participation Rate (%)` — % of population in the labour force
- `Area` — Rural or Urban

The raw file, as downloaded, contained real-world messiness: 28 completely
blank trailing rows, 27 duplicate rows, inconsistent spacing in column names,
and leading spaces in text values — all handled explicitly in the
cleaning step (Section 7) rather than being pre-cleaned.

---

## 6. Technologies Used

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| pandas | Data loading, cleaning, grouping, and aggregation |
| numpy | Numeric operations |
| matplotlib | Chart plotting |
| seaborn | Statistical visualizations (heatmap, styled bar/line charts) |

No machine learning libraries are needed — this is a pure data analysis
(EDA) project.

---

## 7. Data Cleaning

Every cleaning step below was actually applied to the raw file, in this order:

1. **Cleaned column names** — stripped extra whitespace (e.g. `" Date"` → `"date"`)
   and renamed all columns to short, consistent `snake_case` names.
2. **Removed 28 fully-empty rows** — a block of blank rows at the end of the
   raw CSV export, containing no data at all.
3. **Stripped whitespace from text values** — e.g. `" Andhra Pradesh"` →
   `"Andhra Pradesh"`, `" Rural"` → `"Rural"`, since the raw file had a space
   after every comma.
4. **Checked and handled missing values** — after removing the blank rows,
   0 missing values remained in the core columns; any row still missing a
   `date` or `unemployment_rate` (which would make it unusable) would have
   been dropped, but none were found beyond the blank rows already removed.
5. **Removed duplicate rows** — 27 exact duplicate rows were removed (0 more
   were found after the blank-row cleanup, since most duplicates were within
   the blank-row block already dropped).
6. **Converted `date` to a proper datetime type** (from text in `dd-mm-yyyy`
   format), enabling time-based analysis.
7. **Converted numeric columns** (`unemployment_rate`, `employed`,
   `labour_participation_rate`) to proper numeric types.
8. **Standardized text casing** for `region`, `area`, and `frequency` (e.g.
   ensuring `"RURAL"` and `"rural"` are treated as the same category).
9. **Added derived time columns** — `year`, `month`, and `month_name` — to
   support grouping and seasonal analysis.
10. **Investigated outliers using the IQR method**, rather than blindly
    removing them. 35 of 740 rows (4.7%) fell outside the statistical
    "normal" range. These were **kept**, because they correspond almost
    entirely to the April–May 2020 COVID lockdown period — the exact event
    this project is studying. Removing them would have hidden the real
    signal in the data.

The cleaned dataset (740 rows × 10 columns) is saved to
`outputs/cleaned_unemployment_data.csv`.

---

## 8. Exploratory Data Analysis (actual results)

| Metric | Value |
|---|---|
| Overall average unemployment rate | **11.79%** |
| Minimum unemployment rate recorded | 0.00% (Puducherry, Rural, May 2019) |
| Maximum unemployment rate recorded | 76.74% (Puducherry, Urban, April 2020) |
| Highest average-unemployment month | May 2020 → 24.88% |
| Lowest average-unemployment month | May 2019 → 8.87% |

**Average unemployment rate by region — 5 highest:**

| Region | Avg. Unemployment Rate |
|---|---|
| Tripura | 28.35% |
| Haryana | 26.28% |
| Jharkhand | 20.59% |
| Bihar | 18.92% |
| Himachal Pradesh | 18.54% |

**Average unemployment rate by region — 5 lowest:**

| Region | Avg. Unemployment Rate |
|---|---|
| Gujarat | 6.66% |
| Uttarakhand | 6.58% |
| Assam | 6.43% |
| Odisha | 5.66% |
| Meghalaya | 4.80% |

**Rural vs Urban:**

| Area | Avg. Unemployment Rate |
|---|---|
| Urban | 13.17% |
| Rural | 10.32% |

Urban unemployment was, on average, noticeably higher than rural unemployment
across this dataset — consistent with the fact that urban jobs (retail,
services, hospitality, manufacturing) were more directly disrupted by
lockdown restrictions than agriculture-based rural livelihoods.

---

## 9. Data Visualization

All charts below are generated by the script and saved in `outputs/`:

| File | Chart |
|---|---|
| `1_overall_trend.png` | Overall unemployment trend line (monthly, all-India average) |
| `2_regional_trend_top6.png` | Trend lines for the 6 highest-average states |
| `3_avg_unemployment_by_region.png` | Bar chart — average unemployment by region (all 28) |
| `4_rural_vs_urban.png` | Bar chart — Rural vs Urban average comparison |
| `5_seasonal_monthwise.png` | Bar chart — average unemployment by calendar month |
| `6_region_month_heatmap.png` | Heatmap — region × month unemployment rate |
| `7_covid_comparison.png` | Bar chart — Pre-COVID vs COVID-period average |
| `8_most_affected_regions.png` | Bar chart — top 10 most-affected regions during COVID |

Every chart includes a clear title, labeled X/Y axes, and a legend where more
than one series is plotted.

The overall trend line (`1_overall_trend.png`) is the single most important
chart in the project — it shows unemployment holding steady around 9%
through 2019 and early 2020, then spiking sharply to ~24% in April–May 2020,
before beginning to fall back in June 2020. The heatmap
(`6_region_month_heatmap.png`) shows this same spike occurring across nearly
every state simultaneously in the April–May 2020 columns.

---

## 10. COVID-19 Impact Analysis

India's nationwide COVID-19 lockdown began on **25 March 2020**. Based on
this, the dataset was split into:

- **Pre-COVID period:** 31 May 2019 – 29 Feb 2020 (536 records)
- **COVID period:** 31 Mar 2020 – 30 Jun 2020 (204 records)

> **Note on scope:** this dataset ends on 30 June 2020, so there is not
> enough data beyond mid-2020 to separately analyze a "post-COVID recovery"
> phase. This limitation is stated explicitly rather than inventing
> recovery-phase figures.

**Actual calculated averages:**

| Period | Average Unemployment Rate |
|---|---|
| Pre-COVID | 9.51% |
| COVID period | 17.77% |
| **Change** | **+8.26 percentage points (+86.9% relative increase)** |

**Conclusion: unemployment clearly increased during the COVID period**,
nearly doubling relative to the pre-COVID baseline.

**Regions with the largest increase (most affected):**

| Region | Pre-COVID Avg | COVID Avg | Change |
|---|---|---|---|
| Puducherry | 1.59% | 38.96% | +37.36 pp |
| Tamil Nadu | 2.84% | 25.40% | +22.57 pp |
| Jharkhand | 14.28% | 36.35% | +22.07 pp |
| Bihar | 13.83% | 31.63% | +17.80 pp |
| Karnataka | 3.23% | 15.28% | +12.05 pp |

**Regions with the smallest change (least affected / improved):**

| Region | Pre-COVID Avg | COVID Avg | Change |
|---|---|---|---|
| Assam | 6.37% | 6.58% | +0.21 pp |
| Chandigarh | 16.32% | 14.32% | -2.00 pp |
| Himachal Pradesh | 19.13% | 17.07% | -2.06 pp |
| Tripura | 29.01% | 26.70% | -2.31 pp |
| Jammu & Kashmir | 17.22% | 12.89% | -4.33 pp |

Interestingly, some regions that already had **high pre-COVID unemployment**
(Tripura, Himachal Pradesh, J&K) show little change or even a slight
decrease during COVID, while regions with **low pre-COVID unemployment**
(Puducherry, Tamil Nadu, Karnataka) saw the sharpest relative jumps. This
suggests COVID hit urban-service-economy states disproportionately hard,
while some already-struggling regions were closer to a ceiling effect or
had different reporting dynamics.

---

## 11. Seasonal Trend Analysis

**Average unemployment rate by calendar month (all years combined):**

| Month | Avg. Rate | Month | Avg. Rate |
|---|---|---|---|
| Jan | 9.95% | Jul | 9.03% |
| Feb | 9.96% | Aug | 9.64% |
| Mar | 10.70% | Sep | 9.05% |
| Apr | 23.64% | Oct | 9.90% |
| May | 16.65% | Nov | 9.87% |
| Jun | 10.55% | Dec | 9.50% |

At first glance, April and May look like a strong "seasonal peak." **However,
this dataset only spans 14 months (May 2019 – June 2020), touching just 2
calendar years.** When checked properly:

- **Only May and June are actually covered in both 2019 and 2020** — every
  other month (Jan, Feb, Mar, Apr, Jul–Dec) has data from only a single
  year.
- Direct year-over-year comparison for the two repeating months:
  - **May:** 2019 = 8.87% vs 2020 = 24.88%
  - **June:** 2019 = 9.30% vs 2020 = 11.90%

Both repeating months show a **large jump in 2020 alone**, not a value that
naturally repeats every year — which is a strong sign this is the COVID-19
shock, not a recurring seasonal pattern.

**Conclusion: this dataset does NOT provide enough evidence to confirm a
genuine recurring seasonal trend across the year.** The apparent April/May
"peak" is best explained by the COVID-19 lockdown coinciding with those
months in 2020, rather than unemployment naturally rising every April/May.
A multi-year dataset (3+ full years) would be required to properly test for
seasonality.

---

## 12. Key Findings

*(Strictly data-driven — see `outputs/key_findings.txt` for the raw script output)*

1. The overall average unemployment rate across the full dataset is
   **11.79%**, ranging from 0.00% to a peak of 76.74%.
2. The single highest unemployment record was **76.74% in Puducherry
   (Urban), April 2020**.
3. The single lowest unemployment record was **0.00% in Puducherry (Rural),
   May 2019**.
4. **May 2020 was the worst month nationally**, averaging 24.88% —
   roughly 2.8× the lowest month (May 2019, 8.87%).
5. **Puducherry** saw the largest COVID-driven increase (+37.36 percentage
   points), followed by Tamil Nadu, Jharkhand, and Bihar.
6. **Jammu & Kashmir, Tripura, and Himachal Pradesh** — already high-
   unemployment regions before COVID — showed little further increase or
   even a slight decrease during the COVID period.
7. **Urban unemployment (13.17%) was consistently higher than rural
   unemployment (10.32%)** on average across the dataset.
8. Unemployment **increased by 86.9%** (relative) during the COVID period
   compared to pre-COVID.
9. **No confirmed seasonal trend** could be established — the dataset is
   too short (14 months) to distinguish genuine seasonality from the
   one-time COVID shock.
10. States with the lowest overall average unemployment were **Meghalaya,
    Odisha, Assam, Uttarakhand, and Gujarat** — all under 7% on average.

---

## 13. Economic and Social Policy Insights

> The points below are **interpretations and possible policy directions**
> based on the findings above — they are recommendations, not additional
> data findings.

- **Employment-generation programs:** Since unemployment nearly doubled
  during the COVID period, targeted short-term job-creation programs
  (public works, MSME support, gig-economy support) would have been
  especially valuable for urban service-sector workers, who were affected
  more than rural workers.
- **Skill-development programs:** States like Puducherry and Tamil Nadu,
  which had very low pre-COVID unemployment but were hit hardest, may
  benefit from diversified skill-training programs so their workforce isn't
  overly concentrated in COVID-vulnerable sectors (tourism, retail,
  hospitality).
- **Regional employment policies:** Chronically high-unemployment states
  (Tripura, Haryana, Jharkhand, Bihar, Himachal Pradesh) needed — and likely
  still need — sustained, long-term regional employment policy rather than
  only crisis-response measures, since their unemployment was already high
  before COVID.
- **Support for affected workers:** The sharp April–May 2020 spike suggests
  income-support and unemployment-benefit schemes are most urgently needed
  in exactly that narrow window after a shock — speed of response matters
  as much as scale.
- **Crisis-response policies:** Because the spike was sudden and nationwide
  (visible across nearly all 28 regions in the heatmap), a rapid, uniform
  national safety net responds better to this kind of shock than a purely
  region-by-region rollout.
- **Economic recovery planning:** Unemployment had already started falling
  by June 2020 (11.90%, down from 24.88% in May), suggesting recovery can
  happen relatively quickly once lockdown restrictions ease — but this
  dataset doesn't extend far enough to confirm a full return to pre-COVID
  levels, so continued monitoring is recommended.

---

## 14. Conclusion

This project analyzed real Indian unemployment data spanning May 2019 to
June 2020 and produced fully calculated, non-fabricated results. Unemployment
was stable around 9–10% before COVID-19, then rose sharply to a peak of
24.88% in May 2020 — an 86.9% relative increase compared to the pre-COVID
average — before beginning to decline by June 2020. Urban areas were more
affected than rural areas on average, and the impact varied significantly
by state, with Puducherry, Tamil Nadu, Jharkhand, and Bihar seeing the
steepest increases. No genuine seasonal trend could be confirmed, since the
dataset only spans 14 months; the visible April/May "peak" is best explained
by the COVID-19 shock rather than a recurring yearly pattern.

---

## 15. Future Scope

- Extend the dataset with **post-2020 data** to properly analyze the
  COVID-19 recovery phase and long-term trend, not just the initial shock.
- Use a **multi-year dataset (3+ years)** to properly test for genuine
  seasonal patterns, separate from one-time shocks.
- Add **state-wise population or GDP data** to normalize unemployment
  impact by economic size, not just percentage points.
- Perform **time-series forecasting** (e.g., ARIMA, Prophet) to predict
  future unemployment trends.
- Build an **interactive dashboard** (e.g., using Streamlit or Plotly Dash)
  so policymakers can explore the data by region and time period themselves.
- Incorporate **sector-wise unemployment data** (agriculture, manufacturing,
  services) to identify which industries were most affected.

---

## How to Run

```bash
pip install -r requirements.txt
python unemployment_analysis.py
```

All console output (cleaning steps, EDA, COVID analysis, findings) prints to
the terminal, and every chart + the cleaned dataset + a findings summary are
saved automatically inside the `outputs/` folder.

---

## Explaining This Project in a Viva (Simple Language)

**"What is this project about?"**
I analyzed real unemployment data for Indian states, from May 2019 to June
2020, using Python. The main goal was to see how COVID-19 affected
unemployment, and whether unemployment naturally goes up and down with the
seasons.

**"What data did you use?"**
A real public dataset with monthly unemployment rate, employed population,
and labour participation rate, for 28 Indian states, split by rural and
urban areas.

**"What did you do with the data first?"**
I cleaned it — removed blank rows, removed duplicate rows, fixed messy
column names, converted the date column into a proper date format, and
checked for missing values and unusual/outlier values.

**"What tools did you use?"**
Pandas for handling and analyzing the data as tables, and Matplotlib/Seaborn
for making charts like trend lines, bar charts, and a heatmap.

**"What did you find about COVID-19?"**
Unemployment averaged about 9.5% before COVID, then jumped to about 17.8%
during the COVID lockdown period — almost double. The single worst month was
May 2020, at nearly 25% nationally. States like Puducherry and Tamil Nadu
were hit the hardest, even though they had very low unemployment before
COVID.

**"Did you find a seasonal pattern?"**
Not a confirmed one. My dataset only covers about 14 months, which isn't
long enough to prove that unemployment rises every April and May every
single year. The spike I found is most likely a one-time COVID event, not a
repeating seasonal cycle — and I explain this honestly in the project
instead of overclaiming.

**"Why does this matter?"**
Understanding exactly when, where, and how much unemployment changed helps
governments target relief programs, support the right regions, and prepare
better for future economic shocks.
