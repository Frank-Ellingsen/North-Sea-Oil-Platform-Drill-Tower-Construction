# Enterprise Full-Stack Earned Value Management (EVM) Project Guide
### *Bridging Excel Wide-Format Tracking & Power BI Relational Star Schemas for Automated, Live Project Controls Reporting*

---

## 1. Executive Summary & Project Context

In modern capital programs and enterprise project controls, tracking project progress simply by comparing cumulative actual spend against planned budgets is a critical structural blind spot [cite: 178, 232]. If a project is under budget, it could mean the team is operating highly efficiently, or it could mean they are severely behind schedule and have simply not executed the planned work [cite: 200, 276]. 

**Earned Value Management (EVM)** resolves this ambiguity by integrating **Scope, Schedule, and Cost** into a single, unified performance-led tracking framework [cite: 178, 232]. EVM introduces the concept of **Earned Value (EV)**—the budgeted cost of work actually performed [cite: 134, 154]. By comparing Planned Value (PV), Earned Value (EV), and Actual Cost (AC) as a combined system, project managers can identify early-warning signals, evaluate cost efficiency, and mathematically forecast final outturns before small variances compound into irreversible overruns [cite: 28, 130, 201].

This guide serves as a comprehensive blueprint for intermediate project analysts to construct a production-ready, automated **Full-Stack EVM System**. This architecture segregates localized, structured data entry in **Microsoft Excel** from a highly optimized relational **Star Schema** data model and interactive dashboard in **Microsoft Power BI** [cite: 233, 234].

---

## 2. Excel Wide-Format Schema & Parametric S-Curves

### 2.1 The Strategic Excel Data Schema
For field teams, entering transaction-level or periodic data into complex databases can be a significant administrative barrier. To reduce data-entry friction, we establish three clean, standardized, wide-format Excel worksheets representing the baseline plan, physical progress, and expenditures [cite: 238, 302].

#### Worksheet 1: Planned Value (PV) Baseline
This worksheet contains the time-phased baseline budget representing the Budgeted Cost of Work Scheduled (BCWS) [cite: 32, 238]. The sum of all planned values across the timeline defines the **Budget at Completion (BAC)** [cite: 32, 685].
*   **Item_ID:** Unique alphanumeric task identifier (Primary Key) [cite: 236].
*   **WBS_Code:** Work Breakdown Structure hierarchical path (e.g., `1.1.1`) [cite: 236, 239].
*   **Task_Name:** Descriptive name of the deliverable [cite: 239].
*   **Total_Budget_Cost (TBC):** The approved baseline budget for that task [cite: 238, 239].
*   **Month_1 to Month_N:** Time-phased planned value allocated to each period [cite: 238, 239].

```csv
Item_ID,WBS_Code,Task_Name,TBC,Month_1,Month_2,Month_3,Month_4,Month_5,Month_6
T101,1.1.1,Systems Engineering,120000,40000,50000,30000,0,0,0
T102,1.1.2,Procurement,300000,100000,150000,50000,0,0,0
T103,1.2.1,Site Excavation,180000,0,20000,80000,60000,20000,0
T104,1.2.2,Foundation Concrete,240000,0,0,40000,120000,80000,0
T105,1.3.1,Structural Assembly,360000,0,0,0,60000,200000,100000
```

#### Worksheet 2: Progress Tracking (EV % Complete)
At the close of each reporting period, the project controller or Cost Account Manager (CAM) records the cumulative physical % Complete for each active task based on pre-defined objective milestones [cite: 36, 239, 240].
```csv
Item_ID,WBS_Code,Task_Name,TBC,Month_1_%,Month_2_%,Month_3_%,Month_4_%,Month_5_%,Month_6_%
T101,1.1.1,Systems Engineering,120000,0.333,0.750,1.000,1.000,1.000,1.000
T102,1.1.2,Procurement,300000,0.100,0.500,0.800,0.800,0.900,1.000
T103,1.2.1,Site Excavation,180000,0.000,0.111,0.556,0.889,1.000,1.000
T104,1.2.2,Foundation Concrete,240000,0.000,0.000,0.100,0.400,0.800,1.000
T105,1.3.1,Structural Assembly,360000,0.000,0.000,0.000,0.150,0.600,0.900
```

#### Worksheet 3: Actual Costs (AC) Incurred
This worksheet records the raw, incremental monthly expenditures posted directly from the ERP accounting ledger (labor, materials, subcontracts, and equipment) [cite: 8, 240, 241].
```csv
Item_ID,WBS_Code,Task_Name,TBC,Month_1_AC,Month_2_AC,Month_3_AC,Month_4_AC,Month_5_AC,Month_6_AC
T101,1.1.1,Systems Engineering,120000,42000,51000,32000,0,0,0
T102,1.1.2,Procurement,300000,95000,160000,55000,5000,12000,28000
T103,1.2.1,Site Excavation,180000,0,22000,85000,45000,21000,0
T104,1.2.2,Foundation Concrete,240000,0,0,38000,92000,84000,41000
T105,1.3.1,Structural Assembly,360000,0,0,0,55000,185000,96000
```

---

### 2.2 Advanced Excel Parametric S-Curve Formulation
When establishing baseline spending profiles, project managers avoid flat, linear distributions in favor of **Sigmoidal (S-Curves)**, which mathematically represent slow initial mobilization, peak productivity, and gradual closeout deceleration [cite: 2, 247, 494].

To make these S-curves fully dynamic in Excel, we leverage **Liam Bastick’s Parametric S-Curve Model** utilizing Excel 365 dynamic arrays to spill baseline distributions automatically [cite: 3, 14, 26]:

```excel
=Initial_Percentage_Completed+(Target_Percentage-Initial_Percentage_Completed)/
(1+Exp_Factor^((Exp_Growth_Start_Month_No+Exp_Duration_in_Months/2-J$40#)/Exp_Duration_in_Months))
```

#### Formula Variables Explained:
*   **`Initial_Percentage_Completed`:** The starting progress point (e.g., `20%` if retrospectively tracking) [cite: 3, 14].
*   **`Target_Percentage`:** Typically set to `100%` at project completion [cite: 7].
*   **`Exp_Factor`:** The exponential growth multiplier that determines the "characteristic bend" or curvature of the sigmoidal rapid-acceleration phase [cite: 5, 16].
*   **`Exp_Growth_Start_Month_No`:** The specific month number marking the start of the accelerated development envelope [cite: 4, 15].
*   **`Exp_Duration_in_Months`:** The duration of the peak rapid execution segment [cite: 5, 16].
*   **`J$40#`:** The spilled dynamic array range containing a horizontal sequence counter generated via `=SEQUENCE(1, No_of_Periods)` [cite: 6, 17, 248].

#### Automating Dynamic S-Curve Visualizations in Excel via OFFSET:
To prevent manual chart range resizing when the project duration (`No_of_Periods`) changes, project analysts create **Dynamic Named Ranges** in the Excel Formulas ribbon [cite: 9, 19]:
*   **`Dyn_Counter`:** `=OFFSET('S-Curve Assumptions'!$J$40,,,,No_of_Periods)` [cite: 9, 20]
*   **`Dyn_Date`:** `=OFFSET('S-Curve Assumptions'!$J$41,,,,No_of_Periods)` [cite: 9, 20]
*   **`Dyn_Cost_Amt`:** `=OFFSET('S-Curve Assumptions'!$J$44,,,,No_of_Periods)` [cite: 9, 20]

These ranges automatically contract or expand, updating Excel chart axes instantaneously when inputs shift [cite: 8, 18].

---

## 3. Power Query ETL Normalization Pipeline

While wide-format data structures are optimal for manual human entry in Excel, they are highly inefficient and logically flawed for dimensional BI reporting [cite: 233, 549]. Power BI cannot calculate cumulative running totals or process time intelligence over horizontal arrays of period columns [cite: 102, 233, 235]. 

To bridge this gap, we build an automated **Power Query ETL Pipeline** to ingest, cleanse, unpivot, and normalize Excel files into a vertical, transactional dataset [cite: 245, 547].

```
Excel Wide-Format Files              Power Query Transformations            Power BI Semantic Model
[PV Baseline (Month 1-12)]   ───►   [1. Ingest Raw Sheets]         ───►   [Normalized Fact Table]
[EV Progress (% Complete)]   ───►   [2. Unpivot Monthly Columns]   ───►   `Fact_EVM_Periodic`
[Actual Costs (Raw Spend)]   ───►   [3. Merge & Cast Data Types]   ───►   `Dim_Date` & `Dim_WBS`
```

### 3.1 Step-by-Step Power Query ETL Protocol
For each of the three wide-format Excel worksheets, establish the following extraction query:

1.  **Ingestion:** Select `Get Data > Excel Workbook` and load the respective worksheet [cite: 245, 377].
2.  **Cleansing:** Promote headers and filter out blank summary rows or footer notes [cite: 245].
3.  **Unpivoting (The Core Transformation):**
    *   Select the non-timeline columns: `Item_ID`, `WBS_Code`, and `Task_Name` [cite: 245].
    *   Right-click the selected column headers and choose **Unpivot Other Columns** [cite: 21, 245].
    *   Rename the newly created `Attribute` column to `Date_Period` and the `Value` column to its respective metric name (e.g., `PV_Incremental`, `EV_Physical_Percent`, or `AC_Incremental`) [cite: 20, 245].
4.  **Date Alignment:**
    *   Format `Date_Period` as a standard text string (e.g., "Month_1", "Month_2").
    *   Convert this period string into a contiguous Date type by mapping it to a calendar dimension or using a calculated custom column, e.g., `= Date.EndOfMonth(Date.AddMonths(Start_Date, Number.From(Text.AfterDelimiter([Date_Period], "_")) - 1))` [cite: 15, 17, 245].
5.  **Type Casting:** Cast all ID columns to Text, and all monetary/percentage columns to Decimal or Currency (`Double` and `Currency` types) [cite: 21, 245].

### 3.2 Consolidating into the Sales Fact Query
Once the three queries are unpivoted, they must be combined into a single, vertical transaction query using a **Left Outer Join** on the compound keys `Item_ID` and `Date_Period` [cite: 6, 245]:

```powerquery
let
    // Source: Ingest the unpivoted Planned Value base table
    Source = PowerQuery.Database("Planned_Value_Unpivoted"),
    
    // Merge the Actual Cost table on Item_ID and Period
    MergeAC = Table.NestedJoin(Source, {"Item_ID", "Date_Period"}, Actual_Cost_Unpivoted, {"Item_ID", "Date_Period"}, "AC_Table", JoinKind.LeftOuter),
    ExpandAC = Table.ExpandTableColumn(MergeAC, "AC_Table", {"AC_Incremental"}, {"AC_Incremental"}),
    
    // Merge the Progress (EV % Complete) table
    MergeEV = Table.NestedJoin(ExpandAC, {"Item_ID", "Date_Period"}, Progress_Unpivoted, {"Item_ID", "Date_Period"}, "EV_Table", JoinKind.LeftOuter),
    ExpandEV = Table.ExpandTableColumn(MergeEV, "EV_Table", {"EV_Physical_Percent"}, {"EV_Physical_Percent"}),
    
    // Join the WBS master directory to retrieve the Total Budget Cost (TBC) for each task
    MergeWBS = Table.NestedJoin(ExpandEV, {"Item_ID"}, Dim_WBS, {"Task_ID"}, "WBS_Table", JoinKind.LeftOuter),
    ExpandWBS = Table.ExpandTableColumn(MergeWBS, "WBS_Table", {"TBC"}, {"Total_Budget_Cost"}),

    // Calculate Incremental Earned Value on-the-fly
    // Formula: (Current Period % Complete - Previous Period % Complete) * Total_Budget_Cost
    SortRows = Table.Sort(ExpandWBS, {{"Item_ID", Order.Ascending}, {"Date", Order.Ascending}}),
    AddEVIncremental = Table.AddColumn(SortRows, "EV_Incremental_Calculated", each 
        let
            CurrentRowID = [Item_ID],
            CurrentDate = [Date],
            CurrentPercent = [EV_Physical_Percent],
            // Lookup the previous period percent complete for same task
            PrevPercent = try Table.Last(Table.SelectRows(SortRows, each [Item_ID] = CurrentRowID and [Date] < CurrentDate))[EV_Physical_Percent] otherwise 0,
            IncrementalPercent = CurrentPercent - PrevPercent
        in
            IncrementalPercent * [Total_Budget_Cost]
    )
in
    AddEVIncremental
```

### 3.3 Relational Schema Auditing & QA Validation
For capital programs operating under strict regulatory compliance (such as the ANSI/EIA-748 standards for federal defense procurement), our data transformations must be rigorously audited [cite: 35, 133, 246]. 

Project controllers test the relational integrity of their ETL unpivot pipelines by processing open-source **EVM Validation reference datasets** (such as figshare arrays) [cite: 24, 246]:
*   **`ewpass.csv`:** Captures raw Work Authorization transactions to verify budget authorizations [cite: 246].
*   **`itemcor.csv`:** Verifies accurate mapping alignment between the Work Breakdown Structure (WBS) and Organizational Breakdown Structure (OBS) [cite: 246].
*   **`FinalPattern.csv` & `InitialPattern.csv`:** Serves as S-curve pattern templates to ensure that unpivoted values correctly accumulate without mathematical drift [cite: 246].

---

## 4. Power BI Relational Star Schema Model

Once the unpivoted data is loaded, we configure the **Model View** inside Power BI Desktop to build the **Relational Star Schema**. This schema is highly optimized for the VertiPaq columnar database engine, compressing redundant values and ensuring rapid filter propagation [cite: 234, 365, 370].

```
           ┌──────────────────────┐
           │      Dim_Date        │
           │                      │
           │  PK: Date_Key        │
           └──────────┬───────────┘
                      │ 1
                      │
                      │ * (Date_Key)
            ┌─────────▼───────────┐
            │  Fact_EVM_Periodic  │
            │                     │
            │  FK: Date_Key       │
            │  FK: Task_ID        │
            └─────────▲───────────┘
                      │ * (Task_ID)
                      │
                      │ 1
           ┌──────────┴───────────┐
           │       Dim_WBS        │
           │                      │
           │  PK: Task_ID         │
           └──────────────────────┘
```

### 4.1 Schema Component Specifications
*   **The Centered Fact Table (`Fact_EVM_Periodic`):** This vertical table stores the incremental transactional postings of Planned Value, Actual Cost, and derived physical Earned Value by period [cite: 242]. Storing incremental periodic values—rather than pre-calculated cumulative metrics—allows Power BI to calculate cumulative S-curves dynamically across any custom timeline or categorical segment [cite: 12, 104].
*   **The Date Dimension (`Dim_Date`):** A contiguous Date table containing no gaps is mandatory to enable Power BI's time intelligence engine [cite: 102, 235]. We generate this using a calculated DAX table:
    ```dax
    Dim_Date = 
    VAR StartDate = DATE(2026, 01, 01)
    VAR EndDate = DATE(2026, 12, 31)
    RETURN
    ADDCOLUMNS(
        CALENDAR(StartDate, EndDate),
        "Year", YEAR([Date]),
        "Month", FORMAT([Date], "mmmm"),
        "Month_Number", MONTH([Date]),
        "Year_Month", FORMAT([Date], "yyyy-mm"),
        "Quarter", "Q" & ROUNDUP(MONTH([Date]) / 3, 0)
    )
    ```
*   **The Work Breakdown Structure Dimension (`Dim_WBS`):** Stores WBS hierarchical metadata, detailing Level 1 Codes, Level 2 Codes, Accountable Cost Account Managers (CAMs), and specific Task Names [cite: 244]. It forms the single unique lookup to filter the fact table [cite: 243, 244].

### 4.2 Structural Relationship Configuration
1.  **Link the Date Keys:** Join `Dim_Date[Date]` to `Fact_EVM_Periodic[Date_Key]` [cite: 379].
2.  **Link the WBS Keys:** Join `Dim_WBS[Task_ID]` to `Fact_EVM_Periodic[Task_ID_FK]` [cite: 242, 244].
3.  **Relationship Properties:**
    *   **Cardinality:** Set strictly to **Many-to-One (\* : 1)**, propagating from the Fact table (Many side, `*`) to the Dimension table (One side, `1`) [cite: 365].
    *   **Cross Filter Direction:** Set strictly to **Single (Unidirectional)** [cite: 365, 367]. This ensures filters cascade cleanly from lookup dimensions down to fact tables, preserving performance and avoiding circular path logical errors [cite: 110, 367].
4.  **Protecting the Semantic Layer:** To prevent direct querying of raw records and ensure dashboard authors pull columns exclusively from dimensions, we **Hide** all foreign keys in the Fact table, and completely hide intermediate ETL Queries (like the raw wide-format staging tables) in Report View [cite: 563, 564].

---

## 5. Comprehensive DAX Measures Specification

With our database relationships active, we construct the analytical brain of the EVMS using **Data Analysis Expressions (DAX)** [cite: 99, 232].

### 5.1 Defining the Status Date (The Performance Stoppage point)
EVM requires a baseline cutoff or "Data Date" to isolate historical actuals from future baseline planning [cite: 52, 231]. We construct a dynamic Status Date measure:
```dax
Status_Date = MAX(Fact_EVM_Periodic[Date_Key])
```

### 5.2 Core S-Curve Time-Intelligence Metrics

#### S-Curve Option A: The Classic CALCULATE + ALLSELECTED Pattern
This standard pattern works across all legacy Power BI versions. It forces the VertiPaq engine to iterate over the Date dimension to accumulate point-to-point values [cite: 250, 414]:
```dax
PV_S_Curve_Classic = 
CALCULATE(
    SUM(Fact_EVM_Periodic[PV_Incremental]),
    FILTER(
        ALLSELECTED(Dim_Date[Date]),
        Dim_Date[Date] <= MAX(Dim_Date[Date])
    )
)
```

#### S-Curve Option B: The Optimized WINDOW Pattern (Power BI 2024+)
For large datasets exceeding millions of rows, the newer `WINDOW` function computes S-curves with significantly reduced memory consumption, bypassing nested row scans in the storage engine [cite: 15, 251, 403]:
```dax
PV_S_Curve_WINDOW = 
CALCULATE(
    SUM(Fact_EVM_Periodic[PV_Incremental]),
    WINDOW(
        1, ABS,       -- Start at absolute position 1 (first date)
        0, REL,       -- End at the current relative date
        ORDERBY(Dim_Date[Date])
    )
)
```

#### The Progress S-Curves (Constrained to the Status Date)
The cumulative S-curves for Earned Value and Actual Cost are structurally truncated at the Status Date to ensure that no future actuals are plotted in the forecast horizon [cite: 52, 251]:
```dax
EV_S_Curve = 
VAR CurrentDate = MAX(Dim_Date[Date])
RETURN
IF(
    CurrentDate <= [Status_Date],
    CALCULATE(
        SUM(Fact_EVM_Periodic[EV_Incremental_Calculated]),
        WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date]))
    ),
    BLANK()
)

AC_S_Curve = 
VAR CurrentDate = MAX(Dim_Date[Date])
RETURN
IF(
    CurrentDate <= [Status_Date],
    CALCULATE(
        SUM(Fact_EVM_Periodic[AC_Incremental]),
        WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date]))
    ),
    BLANK()
)
```

---

### 5.3 Health Indicators & Forecasting DAX Reference

Once cumulative curves are active, we calculate primary variances, efficiency ratios, and forecasts [cite: 130, 201].

#### Cost Variance (CV) & Cost Performance Index (CPI)
Measures physical cost performance to date. A negative CV or a CPI under 1.0 indicates a budget overrun [cite: 154, 157]:
```dax
Cost_Variance = [EV_S_Curve] - [AC_S_Curve]

Cost_Performance_Index = DIVIDE([EV_S_Curve], [AC_S_Curve], 0)
```

#### Schedule Variance (SV) & Schedule Performance Index (SPI)
Measures execution velocity against the baseline. A negative SV or an SPI under 1.0 indicates a schedule delay [cite: 154, 157]:
```dax
Schedule_Variance = [EV_S_Curve] - [PV_S_Curve_WINDOW]

Schedule_Performance_Index = DIVIDE([EV_S_Curve], [PV_S_Curve_WINDOW], 0)
```

#### Estimate at Completion (EAC) & Variance at Completion (VAC)
Forecasts overall outturn cost and projected deficit assuming the current spend efficiency (CPI) persists through completion [cite: 216, 253]:
```dax
Estimate_at_Completion_Trend = DIVIDE(SUM(Fact_EVM_Periodic[PV_Incremental]), [Cost_Performance_Index], 0)

Variance_at_Completion = SUM(Fact_EVM_Periodic[PV_Incremental]) - [Estimate_at_Completion_Trend]
```

#### To-Complete Performance Index (TCPI)
Determines the mandatory cost efficiency required from this day forward to achieve the original baseline budget [cite: 135, 254]. If TCPI is more than 0.10 higher than cumulative CPI, the target is mathematically unviable [cite: 136, 254]:
```dax
TCPI_BAC = 
VAR BAC = SUM(Fact_EVM_Periodic[PV_Incremental])
VAR EV = [EV_S_Curve]
VAR AC = [AC_S_Curve]
RETURN
DIVIDE(BAC - EV, BAC - AC, 0)
```

---

### 5.4 Advanced Time-Based S-Curve Modeling: Earned Schedule
A major limitation of traditional, cost-based EVM is **Schedule Decay** [cite: 33, 255]. At project completion, cumulative Planned Value always equals Earned Value (both equal BAC) [cite: 255]. Consequently, the traditional cost-based SPI gradually drifts back to `1.0` even if the project is finished months behind schedule [cite: 255].

To resolve late-stage schedule index decay, we calculate **Earned Schedule (ES)** in units of time (months) rather than currency, by finding the exact point on the calendar timeline when our current Earned Value was *planned* to be achieved [cite: 33, 255]:

$$\text{Earned Schedule (ES)} = C + I$$
*   **$C$:** The last completed period where the cumulative Planned Value is less than or equal to the current cumulative Earned Value [cite: 255].
*   **$I$:** The linear interpolation fraction representing progress through the subsequent active period [cite: 255]:
$$I = \frac{\text{EV} - \text{PV}_C}{\text{PV}_{C+1} - \text{PV}_C}$$

We implement this advanced time-based schedule calculation in DAX [cite: 255]:

```dax
Earned_Schedule_Months = 
VAR CurrentEV = [EV_S_Curve]
VAR DateTableWithPV = 
    FILTER(
        ALL(Dim_Date),
        [PV_S_Curve_WINDOW] <= CurrentEV
    )
VAR C_MonthDate = MAXX(DateTableWithPV, Dim_Date[Date])
VAR C_MonthNumber = MAXX(DateTableWithPV, Dim_Date[Month_Number])
VAR PV_At_C = CALCULATE([PV_S_Curve_WINDOW], Dim_Date[Date] = C_MonthDate)
VAR PV_At_C_Plus_1 = CALCULATE([PV_S_Curve_WINDOW], DATEADD(Dim_Date[Date], 1, MONTH))
VAR Interpolation = DIVIDE(CurrentEV - PV_At_C, PV_At_C_Plus_1 - PV_At_C, 0)
RETURN
IF(
    CurrentEV >= SUM(Fact_EVM_Periodic[PV_Incremental]),
    MAX(Dim_Date[Month_Number]),
    C_MonthNumber + Interpolation
)
```

By substituting calendar time for budget dollars, we calculate the time-based **Schedule Performance Index (SPI(t))** [cite: 33, 255]:
```dax
SPI_Time_Based = DIVIDE([Earned_Schedule_Months], MAX(Dim_Date[Month_Number]), 0)
```
Unlike cost-based SPI, this metric remains mathematically accurate through project completion, providing a robust timeline health check [cite: 255].

---

## 6. Interface Design & Visual Wireframes

To maximize user adoption and ensure high executive utility, we apply a strategic, structured **F-Pattern Grid System** to design our Power BI report canvas [cite: 258, 261]:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  LOGO      [Project Name Selector]      welcome: User   refreshed: 10:26 AM   │
├──────────────────────────────────────────────────────────────────────────────┤
│  [KPI 1]          [KPI 2]          [KPI 3]          [KPI 4]          [KPI 5] │
│  Planned Value    Earned Value     Actual Cost      CPI (RAG)        SPI (RAG)│
├──────────────────────────────────────────────────────────────────────────────┤
│  [Visual 1: Combo Chart]                        │  [Visual 2: Breakdown]     │
│                                                 │                            │
│  PV vs EV vs AC Cumulative Lines                │  Variance by Work Package  │
│  Incremental Periodic Variance Bars             │  Decomposition Tree        │
├──────────────────────────────────────────────────────────────────────────────┤
│  [Visual 3: Risk Bullseye XY Scatter]           │  [Visual 4: Details Grid]  │
│                                                 │                            │
│  Concentric circles representing 5%/10%/15%     │  Tabular data matrix with  │
│  Cost vs Schedule Variance Coordinates          │  variance sparklines       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6.1 Core Dashboard Elements (F-Pattern Hierarchy)
1.  **The Header (Top Strip):** Features company branding, data-refresh timestamp, and a single global Project Slicer to ensure immediate page loading [cite: 311, 674].
2.  **The KPI summary row:** Placed strictly at the top to satisfy quick reading habits [cite: 311]. We limit this to exactly 5 high-yield performance index cards (PV, EV, AC, CPI, and SPI) to prevent visual clutter [cite: 262, 336].
3.  **The S-Curve Combo Chart:** Placed centrally, this *Line and Clustered Column Chart* plots cumulative metrics as trendlines (PV, EV, AC) and incremental monthly values as column bars to isolate periodic variances [cite: 258, 380]. 
    *   *Critical Rule:* The primary Y-axis (Incremental Columns) and the secondary Y-axis (Cumulative Lines) must be locked to start at exactly 0.00 to preserve accurate relative proportions [cite: 258].
4.  **The Risk Bullseye Chart:** An XY Scatter Plot mapped directly onto concentric circular boundary lines to allow executives to isolate outlying over-budget accounts at a single glance [cite: 259, 261].

---

### 6.2 Designing a Concentric "Bullseye" Scatter Plot
Because standard scatter plots lack intuitive scale boundaries, we plot coordinate points over concentric rings representing **5% (Green)**, **10% (Yellow)**, and **15% (Red)** variance limits [cite: 259].

To generate these circular background boundaries, we create a reference dataset of **360 degree points (theta $\theta$)** to calculate circle coordinates [cite: 260, 271]:

$$X_\theta = R \times \cos\left(\frac{\theta \times \pi}{180}\right)$$
$$Y_\theta = R \times \sin\left(\frac{\theta \times \pi}{180}\right)$$

#### Mapped Parameters:
*   **$\theta$:** Aligned sequence integer running from $1$ to $360$ representing the degrees of the circle [cite: 260, 271].
*   **$R$ (Radius):** Custom-scaled to define specific boundary rings (e.g., $R = 0.05$ for the 5% ring, $R = 0.10$ for the 10% ring, and $R = 0.15$ for the 15% ring) [cite: 260, 271].

The actual project/WBS coordinate points are plotted dynamically over the background circles using their percentage variance calculations as coordinates [cite: 261, 271]:

$$\text{Project } X = \text{Schedule Variance \%} = \frac{SV}{PV}$$
$$\text{Project } Y = \text{Cost Variance \%} = \frac{CV}{EV}$$

```
                Cost Overruns (+Y)
                       │
              Red (15% Ring)
          Amber (10% Ring) 
       Green (5% Ring) │
  Behind Schedule      │       Ahead of Schedule
  ─────────────────────┼──────────────────── (+X)
  (-X)                 │
                       │
                       │
                       │ Cost Savings (-Y)
```

Any task coordinate plotting outside the outer red boundary represents a severe double-overrun (late and over-budget) that triggers immediate escalation [cite: 116, 261].

---

## 7. Enterprise Governance & PMO Best Practices

Setting up unpivot pipelines and writing complex DAX formulas is only 20% of the battle [cite: 139]. To ensure successful, repeatable dashboard automation, PMO directors enforce strict project governance guidelines [cite: 262].

### 7.1 Baseline Integrity & Rebaselining Rules
*   **Performance Measurement Baseline (PMB):** Budget baselines (Planned Value) must remain locked once approved at project kickoff [cite: 256, 257]. 
*   **Change Control Integration:** Under ANSI/EIA-748, project baselines must not be overwritten or updated dynamically to mask cost overruns [cite: 36, 148]. Baseline Change Requests (BCRs) must only be processed for approved, client-directed changes in scope, which must be clearly segregated from normal schedule drift [cite: 36, 148].
*   **Management Reserve (MR):** Budgets withheld by the Project Director to manage unforeseen, un-estimated risks must sit outside the Performance Measurement Baseline and must never be used to supplement poor task performance [cite: 257].

### 7.2 Single-Point Responsibility Assignment
*   **The RAM Core:** Every WBS task and cost item in the database must map directly to a single, accountable Cost Account Manager (CAM) through a formal **Responsibility Assignment Matrix (RAM)** [cite: 236, 263]. 
*   **Traceable Approvals:** Cost accounts must map directly to signed Work Authorization Documents (WADs) and Control Account Plans (CAPs) to maintain a transparent, auditable trail from general ledger expenses to physical task status [cite: 257, 263].

### 7.3 Weekly and Monthly Reporting Cadence
EVM data becomes a decorative metric if it is reviewed on a stale monthly cycle [cite: 132, 208]. The PMO establishes a structured monthly drumbeat [cite: 266]:
1.  **Weekly Status Cycle:** Schedulers collect raw schedule updates from the field and import status dates directly into the scheduling environment (e.g., Primavera P6 or MS Project) [cite: 376, 632].
2.  **ERP Cost Accruals:** Actual costs are exported weekly from the accounting database to catch un-invoiced subcontractor accruals before they distort the cost performance index [cite: 208, 632].
3.  **Monthly PMO Performance Review:** Performance indexes are run at the control account level [cite: 266]. If rolling averages show that **TCPI vs. BAC is more than 0.10 higher than cumulative CPI**, an immediate recovery analysis is triggered to define a realistic, revised Estimate at Completion (EAC) [cite: 136, 254].

---

## 8. Summary of EVM Master Formulas

To maintain mathematical consistency across all Excel templates and Power BI calculated fields, use the following standardized formula reference:

| Parameter | Abbreviation | Mathematical Formula | Power BI DAX Expression | Action Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **Budget at Completion** | `BAC` | $\sum PV$ [cite: 685, 707] | `SUM(Fact_EVM_Periodic[PV_Incremental])` | Baseline Anchor [cite: 203] |
| **Planned Value** | `PV` | $\% \text{ Planned} \times \text{BAC}$ [cite: 154, 707] | `CALCULATE(SUM(PV_Incremental), WINDOW(...))` [cite: 251] | Standard baseline [cite: 32] |
| **Earned Value** | `EV` | $\% \text{ Complete} \times \text{BAC}$ [cite: 154, 708] | `CALCULATE(SUM(EV_Incremental_Calculated), WINDOW(...))` [cite: 251] | Progress anchor [cite: 134, 321] |
| **Actual Cost** | `AC` | $\sum \text{ ERP Costs}$ [cite: 154, 708] | `CALCULATE(SUM(AC_Incremental), WINDOW(...))` [cite: 251] | Financial ledger spend [cite: 36, 135] |
| **Cost Variance** | `CV` | $EV - AC$ [cite: 154, 156] | `[EV_S_Curve] - [AC_S_Curve]` | Negative = Over Budget [cite: 154, 156] |
| **Schedule Variance** | `SV` | $EV - PV$ [cite: 154, 156] | `[EV_S_Curve] - [PV_S_Curve]` | Negative = Behind Schedule [cite: 154, 156] |
| **Cost Performance Index** | `CPI` | $EV \div AC$ [cite: 156, 166] | `DIVIDE([EV_S_Curve], [AC_S_Curve], 0)` [cite: 252] | Under 0.90 = Critical Overrun [cite: 157] |
| **Schedule Performance Index** | `SPI` | $EV \div PV$ [cite: 156, 166] | `DIVIDE([EV_S_Curve], [PV_S_Curve], 0)` [cite: 253] | Under 0.95 = Schedule Delay [cite: 157] |
| **Estimate at Completion** | `EAC` | $BAC \div CPI$ [cite: 159, 253] | `DIVIDE([BAC], [Cost_Performance_Index], 0)` [cite: 253] | EAC > BAC = Budget Risk [cite: 135] |
| **To-Complete Performance Index** | `TCPI` | $\frac{BAC - EV}{BAC - AC}$ [cite: 254, 709] | `DIVIDE([BAC] - [EV], [BAC] - [AC], 0)` [cite: 254] | Over 1.10 = Unrealistic Target [cite: 135, 254] |
