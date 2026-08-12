# Executive EVM Variance Explanations & Corrective Action Plan

**Project:** North Sea Oil Platform Drill Tower Construction ($26.5M EPC Program)  
**Status Date:** August 31, 2026 (Month 8 / Status Date)  
**Target Role:** Project Controller (Frank Ellingsen) / Executive Steering Committee  

---

## 📌 Executive Summary & Red Indicator Audit

At Status Month 8, the North Sea Drill Tower program exhibits critical cost overruns ($CPI = 0.75$) and critical path schedule delays ($+31\text{ Days}$, $SPI = 0.86$). The table below outlines the root cause explanations and recommended corrective action plans for all active red performance indicators.

| Red Indicator | Status Metric | Threshold | Root Cause Explanation | Recommended Actionable Next Steps | Accountable CAM |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **Cost Variance ($CV$)** | **-$5,900,000** | $CPI = 0.75$ ($< 0.90$) | Structural steel fitting rework, unbudgeted welding labor hours, and premium overtime rates at Verdal and Egersund yards. | Enforce Design Change Freeze on WBS 1.3 deliverables. Convert open T&M subcontracts to fixed unit-rate capped milestones. | O. Eriksen |
| **Outturn Deficit ($VAC$)** | **-$8,913,604** | $EAC = \$35.41\text{M}$ | Linear extrapolation of poor historical cost performance ($CPI = 0.75$) indicates $33.6\%$ budget overrun against $BAC$. | Submit formal EAC re-baseline proposal to Executive Steering Committee. Request $3.5\text{M}$ drawdown from Management Reserve. | Frank Ellingsen |
| **Target Efficiency ($TCPI_{BAC}$)** | **6.07 (BAC)** | Unviable ($> 1.10$) | Original $BAC$ budget target requires impossible cost efficiency of $607\%$ for remaining work. | Formally transition operational target to $TCPI_{EAC} = 1.00$. Enforce weekly EVM gate reviews for CAMs with $TCPI_{EAC} > 1.05$. | Frank Ellingsen |
| **Schedule Slippage ($SV$)** | **-$2,960,000** | $+31\text{ Days}$ Delay | Procurement delay on Tubular Steel (T103) cascaded to Verdal (T105) and Egersund (T106), threatening Heavy Lift window. | Fast-track Egersund rigging with parallel work-fronts. Re-sequence pre-commissioning tasks. Negotiate 10-day vessel window extension. | M. Berg / K. Solberg |
| **WBS 1.3.2 Mast Assembly** | **-$2,330,000** | $CPI = 0.57$ | Egersund rigging yard productivity bottleneck; high sub-tier contractor churn and excessive rework hours. | Deploy resident Project Controller to Egersund full-time. Audit daily labor timecards and enforce weld quality gates. | O. Eriksen |

---

## 🔍 Detailed Variance Analysis & Recommended Actions

### 1. 🔴 Cost Variance ($CV = -\$5,900,000$, $CPI = 0.75$)
- **Root Cause Explanation**: Actual expenditure ($AC = \$23.44\text{M}$) severely exceeds Earned Value ($EV = \$17.54\text{M}$). Major cost growth originated in WBS 1.3.1 (Verdal Yard Sub-Structure Fabrication, $CV = -\$850\text{k}$) and WBS 1.3.2 (Egersund Derrick Mast Assembly, $CV = -\$2.33\text{M}$). Key drivers include engineering change notices during fabrication, out-of-sequence welding, and high overtime premiums.
- **Recommended Action Plan**:
  1. **Design Change Freeze**: Formally freeze all pending Engineering Change Requests (CRs) for WBS 1.3 until offshore installation completion.
  2. **Subcontract Conversion**: Convert open Time & Materials (T&M) subcontracts with yard fabrication suppliers into fixed unit-rate capped milestones.
  3. **On-site Controller Audit**: Station a dedicated Project Controller at Egersund yard to approve daily man-hour timecards and verify physical milestone completion before payment release.

### 2. 🔴 Outturn Forecast Deficit ($VAC = -\$8,913,604$, $EAC = \$35,413,604$)
- **Root Cause Explanation**: Extrapolating historical efficiency ($CPI = 0.75$) yields a cumulative $EAC_{CPI}$ of $\$35.41\text{M}$ against the baseline $BAC$ of $\$26.50\text{M}$, creating an outturn deficit of $\$8.91\text{M}$.
- **Recommended Action Plan**:
  1. **EAC Re-baseline Proposal**: Prepare an executive re-baseline submission for the Steering Committee to adjust the project budget baseline to $\$35.41\text{M}$.
  2. **Management Reserve (MR) Drawdown**: Formally request a $\$3.50\text{M}$ allocation from corporate Management Reserve to absorb non-recoverable raw material price inflation.
  3. **ETC Ceiling Enforcement**: Set strict Estimate-to-Complete ($ETC = \$11.97\text{M}$) expenditure caps per WBS control account.

### 3. 🔴 Target Cost Efficiency ($TCPI_{BAC} = 6.07$)
- **Root Cause Explanation**: $TCPI_{BAC} = \frac{BAC - EV}{BAC - AC} = \frac{26.50 - 17.54}{26.50 - 23.44} = 6.07$. Achieving the remaining work within the original $\$26.50\text{M}$ budget is mathematically unviable, requiring $607\%$ cost efficiency.
- **Recommended Action Plan**:
  1. **Pivot Operational Metric**: Cease using $TCPI_{BAC}$ as an operational performance target.
  2. **Enforce $TCPI_{EAC}$ Tracking**: Monitor remaining work against $TCPI_{EAC} = \frac{BAC - EV}{EAC - AC} = \frac{26.50 - 17.54}{35.41 - 23.44} = 1.00$.
  3. **Weekly CAM Reviews**: Implement mandatory weekly EVM variance gate reviews for any Control Account Manager whose $TCPI_{EAC}$ exceeds $1.05$.

### 4. 🟡/🔴 Critical Path Schedule Delay ($SV = -\$2,960,000$, $+31\text{ Days}$)
- **Root Cause Explanation**: Procurement delays on High-Grade Tubular Steel (T103, $+31$ days) delayed Verdal Sub-Structure Fabrication (T105) and Egersund Derrick Assembly (T106). This pushes Heavy Lift Mobilization (T107) into late September/October, risking autumn North Sea weather windows.
- **Recommended Action Plan**:
  1. **Rigging Fast-Tracking**: Parallelize structural mast assembly work-fronts at Egersund by deploying additional heavy lift cranes.
  2. **Pre-Commissioning Re-sequencing**: Shift 14 days of pre-commissioning testing (T110) post-mating to shorten the critical path prior to vessel mobilization.
  3. **Marine Fleet Contingency**: Negotiate a 10-day weather-window extension agreement with Heerema Marine Contractors to prevent standby penalty charges ($150\text{k}/day$).

---

## 🌐 Web Dashboard Integration

The interactive web dashboard at [`04_dashboard/index.html`](file:///C:/Users/frank/Desktop/EVM/04_dashboard/index.html) and [`04_dashboard/drill_tower_web_report.html`](file:///C:/Users/frank/Desktop/EVM/04_dashboard/drill_tower_web_report.html) features:
- **Red Indicator Audit Table**: Direct table highlighting root causes, actions, and accountable CAMs.
- **Interactive Badges & Audit Modal**: Clicking any red status metric badge launches an interactive modal popup with detailed root causes, step-by-step action plans, and accountable owner contact info.
- **S-Curve Dynamic Layer Toggles**: Allows switching between Cost Variance ($CV$), Schedule Variance ($SV$), and Earned Schedule ($ES$).
