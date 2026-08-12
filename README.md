# ⚓ Enterprise Earned Value Management (EVM) & Project Controlling System
### Offshore EPC Platform Drill Tower Construction Case Study

![EVM Status Date](https://img.shields.io/badge/Status_Date-August_31,_2026_(Month_8)-blue.svg)
![BAC Budget](https://img.shields.io/badge/BAC_Budget-%2426.50M-059669.svg)
![EAC Forecast](https://img.shields.io/badge/EAC_Forecast-%2435.41M-DC2626.svg)
![CPI Performance](https://img.shields.io/badge/CPI_Index-0.7483-red.svg)
![SPI_t Velocity](https://img.shields.io/badge/SPI__t_Velocity-0.9250-amber.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-Active-059669.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An enterprise-grade **Project Controlling & Earned Value Management (EVM) Analytics Architecture** designed for heavy engineering, maritime, and EPC offshore energy projects. Built around a realistic North Sea EPC Platform Drill Tower Construction Project ($BAC = \$26.50\text{M}$), this repository integrates relational data warehousing (DuckDB & SQLite), Power BI star schema DAX libraries, automated Monte Carlo risk simulations (10,000 runs), commercial capital budgeting appraisals (NPV, IRR, Payback, PI), interactive HTML5 executive dashboards, and publication-ready PDF handbooks and PowerPoint slide decks.

---

## 📌 Executive Dashboard & Performance Highlights (Month 8 / Status Week 36)

```
====================================================================================================
                        OFFSHORE EPC PLATFORM DRILL TOWER PERFORMANCE METRICS
====================================================================================================
Baseline Budget (BAC)        : $26,500,000.00
Planned Progress Value (PV)  : $20,500,000.00 (77.36% Planned Work)
Earned Physical Value (EV)   : $17,540,000.00 (66.19% Physical Completion)
Cumulative Actual Cost (AC)   : $23,440,000.00
Cost Variance (CV = EV - AC)  : -$5,900,000.00 (-33.6% Cost Overrun to Date)
Schedule Variance (SV_t)     : -18.2 Calendar Days (-0.60 Months Schedule Slippage)
Cost Efficiency (CPI)        : 0.7483 ($0.75 Earned Value per $1.00 Spent)
Schedule Velocity (SPI_t)    : 0.9250 (Lipke Earned Schedule Index)

OUTTURN PREDICTIONS & MONTE CARLO RISK ANALYSIS:
----------------------------------------------------------------------------------------------------
• Most Likely Cost Outturn (EAC_1)  : $35,413,604.17 (+$8,913,604.17 Overrun / +33.6%)
• Time-Based Completion Date (EAC_t): January 31, 2027 (+31 Days Delay past Dec 31, 2026 COD)
• Monte Carlo P90 High-Confidence   : $35,815,202.44 Outturn | March 14, 2027 Completion Date
• P90 Risk Reserve Needed           : +$401,598.44 Management Contingency Reserve
• 100% Budget Burn Out Date         : Month 9 (September 2026) — BAC Budget Exhaustion
====================================================================================================
```

---

## 🏛️ Commercial Capital Budgeting & Investment Appraisal

| Commercial Metric | Value | Hurdle Rate / Target | Practical Commercial Evaluation |
| :--- | :---: | :---: | :--- |
| **Net Present Value (NPV @ 10% WACC)** | **+$14,899,563** | **$0.00 Hurdle** | Generates +$14.90M net wealth above 10.0% WACC hurdle |
| **Internal Rate of Return (IRR)** | **18.86%** | **10.0% Hurdle Rate** | Outperforms hurdle target by +886 basis points |
| **Simple Payback Period** | **4.43 Years** | **< 5.0 Years Target** | 53.1 Months (May 2031 payback horizon) |
| **Profitability Index (PI)** | **1.42** | **> 1.0 Ratio** | Generates $1.42 Present Value per $1.00 spent |
| **Total Simple ROI** | **134.37%** | **100.0% Baseline** | 10-year cumulative return on outturn CAPEX |
| **Annualized ROI (CAGR)** | **8.89%/Year** | **5.0% Risk-Free Rate** | Compounded annual growth rate |
| **Gross Future Value (FV Year 10)** | **$130,499,397** | **CAPEX Base** | Total nominal operating cash flow across 10 years |

---

## 📂 Repository Architecture & Folder Sitemap

```
EVM/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml      # CI/CD deployment workflow for GitHub Pages
├── 01_raw_data/                  # Master data files, CSV baselines, and Excel workbooks
│   ├── 01_PV_Baseline.csv        # Monthly Planned Value baseline schedule ($26.50M)
│   ├── 02_EV_Progress.csv        # Physical completion progress by WBS element
│   ├── 03_AC_Actuals.csv         # Cumulative actual cost postings
│   ├── 04_Dim_WBS.csv            # WBS dimension (10 Control Accounts)
│   ├── Drill_Tower_EVM_Report.xlsx # Master Excel workbook with reporting tabs
│   └── EVM_Master_Data.xlsx      # Master raw data spreadsheet
├── 02_databases/                 # Relational SQL Database Engines
│   ├── evm_analytics.duckdb      # DuckDB analytical star schema database
│   └── evm_transactional.db      # SQLite transactional database (FK Integrity Enforced)
├── 03_power_bi/                  # Power BI Star Schema Data Feeds & DAX Libraries
│   ├── Dim_Date.csv              # Calendar dimension table
│   ├── Dim_WBS.csv               # WBS control account dimension
│   ├── Fact_EVM_Periodic.csv     # Fact table (120 periodic postings)
│   ├── Fact_Gantt_Schedule.csv   # Schedule tasks & predecessor dependencies
│   ├── Fact_Milestones.csv       # Milestone gates (M1 to M6)
│   ├── Fact_Risk_Register.csv    # 5x5 Risk Heatmap matrix data (R01 to R05)
│   ├── Fact_Waterfall_Bridge.csv # Cost variance waterfall bridge data
│   ├── Fact_Monthly_Burn_Rate.csv# Cash burn runway data
│   ├── Fact_Financial_Appraisal.csv # Commercial appraisal ratios
│   ├── Fact_Monte_Carlo.csv      # Monte Carlo percentile outcomes (P10 to P95)
│   ├── EVM_DAX_Measures.dax      # Master Power BI DAX measure library
│   ├── PowerBI_DAX_DrillTower.dax# Drill Tower DAX measures
│   └── PowerQuery_Import_Script.m# PowerQuery M script for automated ingestion
├── 04_dashboard/                 # Interactive HTML5 Web Applications
│   ├── index.html                # Executive EVM Controlling Dashboard
│   └── drill_tower_web_report.html# Platform Drill Tower Web Report
├── 05_scripts/                   # Automated Python Processing & Simulation Pipeline
│   ├── create_excel_master.py    # Generates master Excel files
│   ├── etl_pipeline.py           # Ingests CSVs and builds DuckDB star schema
│   ├── build_sqlite_db.py        # Constructs SQLite database
│   ├── generate_drill_tower_data.py # Synthesizes 10-task Drill Tower dataset
│   ├── calculate_financial_ratios.py # Computes NPV, IRR, Payback, PI, ROI
│   ├── monte_carlo_simulation.py # Runs 10,000 Monte Carlo risk iterations
│   ├── update_excel_and_powerbi_full.py # Syncs Excel & Power BI datasets
│   ├── generate_pdf_report.py    # Generates executive PDF report
│   ├── generate_powerpoint_presentation.py # Generates 16:9 PPTX slide deck
│   ├── generate_pm_handbook_pdf.py # Builds Project Manager's PDF Handbook
│   └── verify_model.py           # System-wide automated verification suite
├── 06_docs/                      # Reports, Diagrams, PDF Handbooks & Slide Decks
│   ├── Drill_Tower_Project_Executive_Report.pdf # Executive PDF status report
│   ├── Drill_Tower_Project_Steering_Presentation.pptx # 16:9 PowerPoint deck
│   ├── Project_Managers_EVM_and_Controlling_Handbook.pdf # PDF PM Handbook
│   ├── Executive_1Page_Project_Status_Report.md # 1-Page executive status report
│   ├── EVM_Final_Outcome_Predictions.md # EVM & Earned Schedule predictions
│   ├── EVM_Variance_Explanations_and_Action_Plan.md # Root cause explanations
│   ├── Project_Financial_Ratios_and_Appraisal.md # Financial appraisal report
│   ├── Monte_Carlo_P90_Risk_Analysis.md # Monte Carlo P90 simulation report
│   ├── Project_Risk_Matrix_and_Register.md # Risk Heatmap matrix & register
│   ├── Vertical_Swimlane_WBS_Breakdown.md # Category discipline swimlane report
│   ├── Project_Burn_Rate_and_Runway_Analysis.md # Cash burn runway report
│   ├── Project_Cost_Waterfall_Bridge.md # Waterfall cost bridge report
│   └── Project_Donut_Charts_Analysis.md # Donut charts analysis report
├── _config.yml                   # Jekyll site configuration & directory build exclusions
├── index.html                    # Root Executive Dashboard landing page for GitHub Pages
├── .gitignore                    # Git exclusion rules
├── LICENSE                       # MIT Open Source License
└── README.md                     # Repository documentation landing page
```

---

## ⚡ Quick Start Guide & Execution Instructions

### Prerequisites
Ensure Python 3.10+ is installed along with required packages:
```bash
pip install pandas openpyxl reportlab python-pptx duckdb
```

### 1. Execute Data Pipeline & Model Simulation
Run the automated end-to-end Python pipeline to update DuckDB, SQLite, Excel, Power BI CSVs, Monte Carlo simulations, and generate reports:
```bash
python 05_scripts/create_excel_master.py
python 05_scripts/etl_pipeline.py
python 05_scripts/build_sqlite_db.py
python 05_scripts/generate_drill_tower_data.py
python 05_scripts/calculate_financial_ratios.py
python 05_scripts/monte_carlo_simulation.py
python 05_scripts/update_excel_and_powerbi_full.py
python 05_scripts/generate_pdf_report.py
python 05_scripts/generate_powerpoint_presentation.py
python 05_scripts/generate_pm_handbook_pdf.py
```

### 2. Run Verification Suite
Verify system integrity, DuckDB star schema math, SQLite foreign keys, and dataset file existence:
```bash
python 05_scripts/verify_model.py
```

### 3. Launch Web Dashboard Applications
Open [`index.html`](file:///C:/Users/frank/Desktop/EVM/index.html) at the root directly in any web browser, or view via GitHub Pages deployment.

---

## 📄 Publications & Slide Decks

- 📄 **Project Manager's Handbook (PDF)**: [`06_docs/Project_Managers_EVM_and_Controlling_Handbook.pdf`](file:///C:/Users/frank/Desktop/EVM/06_docs/Project_Managers_EVM_and_Controlling_Handbook.pdf)
- 📊 **Steering Committee PowerPoint Presentation (PPTX)**: [`06_docs/Drill_Tower_Project_Steering_Presentation.pptx`](file:///C:/Users/frank/Desktop/EVM/06_docs/Drill_Tower_Project_Steering_Presentation.pptx)
- 📄 **Executive PDF Status Report (PDF)**: [`06_docs/Drill_Tower_Project_Executive_Report.pdf`](file:///C:/Users/frank/Desktop/EVM/06_docs/Drill_Tower_Project_Executive_Report.pdf)

---

## 🌐 Live GitHub Pages Dashboard

The executive dashboard is published directly on GitHub Pages:
- 🌐 **Live Web Application**: [https://frank-ellingsen.github.io/North-Sea-Oil-Platform-Drill-Tower-Construction/](https://frank-ellingsen.github.io/North-Sea-Oil-Platform-Drill-Tower-Construction/)

---

## 👤 Author & Licensing

- **Author**: Frank Ellingsen — Financial Controller & Project Control Specialist
- **License**: Released under the [MIT License](file:///C:/Users/frank/Desktop/EVM/LICENSE).
