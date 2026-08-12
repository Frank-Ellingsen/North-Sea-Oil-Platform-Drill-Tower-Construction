# 🎯 EVM Final Outcome Predictions & Outturn Forecast Report
**Project Name**: Offshore EPC Platform Drill Tower Project  
**Status Date**: August 31, 2026 (Month 8 / Status Week 36)  
**Author**: Frank Ellingsen, Lead Project Controller  

---

## Executive Summary & Outturn Prediction Matrix

At Status Month 8, the project has achieved **66.19% physical completion** ($EV = \$17.54\text{M}$) against a cumulative budget spent of **$23.44M** ($AC$) and a baseline plan of **$20.50M** ($PV$).

Based on standard Earned Value Management (PMI EVM Practice Standard) and Earned Schedule ($ES$) statistical modeling, the project **will not achieve its original $26.50M budget or December 31, 2026 completion date**.

### 📊 Summary of Final Outcome Scenarios

| Forecast Scenario | Metric | Outturn Cost ($EAC$) | Variance ($VAC$) | Completion Date | Schedule Delay ($TV$) | Probability | Primary Driving Assumptions |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Best Case (Idealistic)** | $EAC_2$ | **$32.40M** | -$5.90M (-22.3%) | **Jan 15, 2027** | +15 Days | 5% | Future work performed strictly at 100% budget efficiency ($CPI_{future} = 1.00$). |
| **Most Likely (Standard EVM)** | $EAC_1$ | **$35.41M** | **-$8.91M (-33.6%)** | **Jan 31, 2027** | **+31 Days** | **70%** | **Remaining work performed at current cumulative efficiency ($CPI = 0.75$, $SPI_t = 0.925$).** |
| **Worst Case (Composite)** | $EAC_3$ | **$37.43M** | -$10.93M (-41.3%) | **Feb 15, 2027** | +46 Days | 25% | Cumulative cost & schedule compounding ($CPI \times SPI = 0.64$). |

---

## 1. Cost Predictions ($EAC$ & $VAC$)

### Status Metrics at Month 8 ($M8$)
- **Budget at Completion ($BAC$)**: $\$26,500,000$
- **Planned Value ($PV$)**: $\$20,500,000$
- **Earned Value ($EV$)**: $\$17,540,000$ ($66.19\%$ physical complete)
- **Actual Cost ($AC$)**: $\$23,440,000$
- **Cost Performance Index ($CPI$)**: $0.7483$ ($-25.2\%$ cost efficiency)

### Detailed $EAC$ Calculations

1. **Standard EVM Forecast ($EAC_1$ - Most Likely)**:
   $$EAC_1 = \frac{BAC}{CPI} = \frac{\$26,500,000}{0.74829} = \$35,413,604$$
   - **Cost Overrun ($VAC_1$)**: $-\$8,913,604$ ($+33.6\%$ cost overrun).
   - **Root Cause**: Unbudgeted subsea structural steel rework ($WBS\text{ }1.3.2$) and crane barge standby rates ($WBS\text{ }1.4.1$).

2. **Floor / Baseline Forecast ($EAC_2$ - Best Case)**:
   $$EAC_2 = AC + (BAC - EV) = \$23,440,000 + \$8,960,000 = \$32,400,000$$
   - **Cost Overrun ($VAC_2$)**: $-\$5,900,000$ (Freeze current overrun; zero future variance).

3. **Composite Risk Forecast ($EAC_3$ - Worst Case)**:
   $$EAC_3 = AC + \frac{BAC - EV}{CPI \times SPI} = \$23,440,000 + \frac{\$8,960,000}{0.7483 \times 0.8556} = \$37,433,522$$
   - **Cost Overrun ($VAC_3$)**: $-\$10,933,522$ ($+41.3\%$ cost overrun).

---

## 2. Schedule & Completion Date Predictions ($EAC_t$)

### Time-Based Status Metrics ($ES$ Lipke Theory)
- **Actual Time ($AT$)**: $8.00\text{ Months}$ ($240\text{ Days}$)
- **Earned Schedule ($ES$)**: $7.40\text{ Months}$ ($222\text{ Days}$)
- **Schedule Performance Index ($SPI_t$)**: $0.9250$ ($-7.5\%$ time efficiency)
- **Time Variance ($SV_t$)**: $-0.60\text{ Months} \approx -18.2\text{ Days}$

### Completion Date Predictions

1. **Earned Schedule Forecast ($EAC_t$ - Time Estimate at Completion)**:
   $$EAC_t = \frac{PD}{SPI_t} = \frac{12.00\text{ Months}}{0.9250} = 12.97\text{ Months} \approx 13.0\text{ Months}$$
   - **Forecast Finish Date**: **January 31, 2027**
   - **Project Delay**: **+31 Calendar Days** ($1.0\text{ Month}$)

2. **Critical Path Schedule Driving Logic**:
   - **Driving Task**: $WBS\text{ }1.3.2$ Derrick Tower Mast Assembly (Egersund Yard).
   - **Constraint**: Heavy Lift Vessel (*Heerema Sleipnir*) mobilization window is locked from **Sep 15 to Oct 15**.
   - **Cascade Risk**: A 30-day delay in mast assembly shifts vessel mobilization into Oct 15–Nov 15, exposing offshore installation to North Sea winter weather downtime ($+$15-20 days severe weather standby risk).

---

## 3. To-Complete Performance Index ($TCPI$) Feasibility Analysis

| Baseline Metric | Target | Required Efficiency ($TCPI$) | Feasibility Evaluation | Operational Action |
| :--- | :---: | :---: | :---: | :--- |
| **Original Budget ($BAC$)** | $\$26.50\text{M}$ | **$2.93$ (or $6.07$ peak)** | **UNVIABLE** | Impossible to achieve. Abandon $BAC$ as financial control baseline. |
| **Revised Forecast ($EAC_1$)** | $\$35.41\text{M}$ | **$1.00$ ($0.75$)** | **ACHIEVABLE** | Standard target. Requires strict cost control on remaining $\$8.96\text{M}$ work. |

---

## 4. Key Project Controller Recommendations

1. **Formal Baseline Revision (Re-baseline EAC)**:
   - Formally submit a Change Order to the Steering Committee updating the baseline $BAC$ from **$26.50M** to **$35.41M** and extending target completion to **January 31, 2027**.

2. **Yard Rework Clampdown at Egersund ($WBS\text{ }1.3.2$)**:
   - Issue a fixed-fee cap on Egersund assembly yard labor. Require 2-shift operations (16 hrs/day) to complete mast assembly by **September 30**.

3. **Heerema Vessel Standby Mitigation ($WBS\text{ }1.4.1$)**:
   - Re-negotiate Heavy Lift Mobilization window with Heerema Marine Contractors to avoid $150,000/day standby penalties during weather delays.

4. **Bi-Weekly Earned Schedule ($ES$) Tracking**:
   - Track $SPI_t$ bi-weekly. If $SPI_t$ drops below $0.90$, immediately trigger emergency double-shift welding crews.
