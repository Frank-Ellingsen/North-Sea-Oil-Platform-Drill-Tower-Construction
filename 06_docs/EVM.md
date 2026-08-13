Core Components of EVM
Scope – The defined work that must be completed.

Schedule – The planned timeline for completing the work.

Cost – The budget allocated to complete the work.

EVM analyzes these components together, enabling project managers to make informed decisions and keep projects on track and within budget.

📊 Key Value Metrics
Planned Value (PV) – The authorized budget for the work scheduled to be completed by a specific time.

Actual Cost (AC) – The actual cost incurred for the work performed by that same time.

Earned Value (EV) – The budgeted value of the work actually completed.

Value Metric Formulas
PV = Planned % Complete × BAC

EV = Actual % Complete × BAC

AC = Actual cost spent to date

📉 Variance Analysis
Variance metrics show whether the project is ahead or behind in cost or schedule.

Cost Variance (CV) = EV − AC

Positive → under budget

Negative → over budget

Schedule Variance (SV) = EV − PV

Positive → ahead of schedule

Negative → behind schedule

📈 Performance Indexes
Performance indexes measure efficiency.

Cost Performance Index (CPI) = EV / AC

CPI < 1 → cost overrun

CPI > 1 → cost efficiency

Schedule Performance Index (SPI) = EV / PV

SPI < 1 → schedule delay

SPI > 1 → schedule efficiency

Critical Ratio (CR) = CPI × SPI

CR < 0.90 → critical combined risk (cost overrun + schedule delay)

0.90 ≤ CR < 1.00 → warning / moderate deficit

CR ≥ 1.00 → healthy overall project health

📅 Forecasting Metrics
BAC (Budget at Completion) – Total approved project budget.

EAC (Estimate at Completion) – Forecasted total project cost based on current performance.

Common EAC Formulas
If current cost performance continues:  
EAC = BAC / CPI

If future work will follow the original plan:  
EAC = AC + (BAC − EV)

If both cost and schedule performance affect remaining work:  
EAC = AC + [(BAC − EV) / (CPI × SPI)]

Variance at Completion (VAC) = BAC − EAC

Positive → expected underrun

Negative → expected overrun

1. Purpose of EVM
   A project management technique that integrates scope, schedule, and cost to measure project performance and forecast future outcomes. EVM compares planned progress with actual progress to identify variances early and support corrective action.

2. Core Components
   Scope — Defined work to be completed

Schedule — Timeline for completing the work

Cost — Budget allocated to the work

3. Key Value Metrics
   Planned Value (PV)  
   Budgeted cost of work scheduled to be completed by a specific date
   PV = Planned % Complete × BAC

Actual Cost (AC)  
Actual cost incurred for work performed to date
AC = Actual cost spent to date

Earned Value (EV)  
Budgeted cost of work actually completed
EV = Actual % Complete × BAC

4. Variance Metrics
   Cost Variance (CV)  
   CV = EV − AC  
   Positive → under budget
   Negative → over budget

Schedule Variance (SV)  
SV = EV − PV  
Positive → ahead of schedule
Negative → behind schedule

5. Performance Indexes
   Cost Performance Index (CPI)  
   CPI = EV / AC

Measures cost efficiency

Schedule Performance Index (SPI)  
SPI = EV / PV

Measures schedule efficiency

6. Budget & Forecasting
   BAC (Budget at Completion)  
   Total approved project budget

EAC (Estimate at Completion)  
Forecasted total project cost

Common EAC Formulas
If current CPI continues:  
EAC = BAC / CPI

If future work follows original plan:  
EAC = AC + (BAC − EV)

If CPI and SPI both influence remaining work:  
EAC = AC + [(BAC − EV) / (CPI × SPI)]

Variance at Completion (VAC)  
VAC = BAC − EAC  
Positive → expected underrun
Negative → expected overrun

7. Quick Interpretation Guide
   CPI < 1 → cost overrun

CPI > 1 → cost efficiency

SPI < 1 → behind schedule

SPI > 1 → ahead of schedule

CV / SV negative → trouble

VAC negative → project expected to exceed budget

Earned Value Management (EVM) — Study Sheet with Color Coding + Graph Example

1. CPI/SPI Color‑Coded Interpretation
   Cost Performance Index (CPI)
   Range Meaning Color
   CPI ≥ 1.00 Cost‑efficient; under budget 🟩 Green
   0.90 ≤ CPI < 1.00 Mild cost overrun; monitor closely 🟨 Yellow
   CPI < 0.90 Significant cost overrun; corrective action needed 🟥 Red

Schedule Performance Index (SPI)
Range Meaning Color
SPI ≥ 1.00 Ahead of schedule 🟩 Green
0.95 ≤ SPI < 1.00 Slight delay; manageable 🟨 Yellow
SPI < 0.95 Behind schedule; intervention required 🟥 Red

These thresholds align with common PMO dashboards and can be directly mapped into conditional formatting in Excel.

2. Second Worked Example (with Graphs)
   Scenario
   A project has a BAC of $500,000.
   At month 6:

Planned % Complete: 60%

Actual % Complete: 55%

Actual Cost (AC): $310,000

Step 1 — Value Metrics
PV = 0.60 × 500,000 = $300,000

EV = 0.55 × 500,000 = $275,000

AC = $310,000

Step 2 — Variances
CV = EV − AC = 275,000 − 310,000 = −$35,000

SV = EV − PV = 275,000 − 300,000 = −$25,000

Step 3 — Performance Indexes
CPI = EV / AC = 275,000 / 310,000 ≈ 0.887 → 🟥 Red

SPI = EV / PV = 275,000 / 300,000 ≈ 0.917 → 🟥 Red

Step 4 — Forecasting
EAC = BAC / CPI = 500,000 / 0.887 ≈ $563,700

VAC = BAC − EAC = −$63,700

3. Visual Graphs (ASCII‑style)
   These are designed so you can drop them into Markdown, Notion, or documentation.

A. CPI/SPI Trend Graph (Example)
Code
Performance Index Trend
Month → 1 2 3 4 5 6
CPI |1.02|0.98|0.95|0.93|0.90|0.89|
SPI |1.05|1.01|0.99|0.97|0.95|0.92|

Color Bands:
1.00+ → █████ Green
0.95–1 → █████ Yellow
<0.95 → █████ Red
Interpretation:
Both CPI and SPI have crossed into red, indicating compounding cost and schedule inefficiency.

B. PV vs EV vs AC Line Graph (ASCII)
Code
Budget Progress (USD)
Month 6 Snapshot

$350k | AC ●
$300k | PV ●
$275k | EV ●
$250k |
$200k |
$150k |
$100k |
$50k |
$0 +---------------------------------
M1 M2 M3 M4 M5 M6
Interpretation:

AC > EV → Cost overrun

EV < PV → Behind schedule

C. Cumulative Cost Curve (S‑Curve)
Code
S‑Curve (Cumulative)

$500k | BAC ●
$400k | AC ●
$300k | PV ●
$275k | EV ●
$200k |
$100k |
$0 +---------------------------------
Planned -----
Actual -----
Earned ----- 7. Monte Carlo Forecasting Example (Print‑Ready)
Monte Carlo forecasting simulates thousands of possible project outcomes by varying uncertain inputs such as CPI, SPI, and remaining work effort.

Scenario
BAC = $1,000,000

Current EV = $400,000

Current AC = $450,000

Remaining work = $600,000 (budgeted)

Uncertainty Inputs (Distributions)
CPI ~ Normal(mean = 0.92, SD = 0.05)

SPI ~ Normal(mean = 0.95, SD = 0.04)

Remaining work effort multiplier ~ Triangular(0.9, 1.0, 1.2)

Simulation Logic (10,000 runs)
For each run:

Sample CPIᵢ

Sample SPIᵢ

Sample effort multiplier Eᵢ

Compute remaining cost:

Remaining Cost
𝑖
=
600
,
000
×
𝐸
𝑖
𝐶
𝑃
𝐼
𝑖
×
𝑆
𝑃
𝐼
𝑖
Compute EACᵢ:

𝐸
𝐴
𝐶
𝑖
=
𝐴
𝐶

- Remaining Cost
  𝑖
  Monte Carlo Results
  After 10,000 simulations:

Statistic Value
Mean EAC $1,185,000
Median EAC $1,170,000
P90 EAC $1,260,000
Probability of Overrunning BAC 92%

Interpretation
The project is very likely to exceed its $1M budget.

A realistic expected final cost is $1.17M–$1.26M.

CPI/SPI uncertainty compounds significantly over remaining work.

PDF‑Friendly Histogram (ASCII)
Code
Monte Carlo EAC Distribution
(Each █ = ~50 simulations)

$1.05M | ████
$1.10M | █████████
$1.15M | ███████████████
$1.20M | █████████████████████
$1.25M | ███████████████
$1.30M | ████
