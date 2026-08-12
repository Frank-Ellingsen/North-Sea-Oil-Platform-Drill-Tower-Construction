# 🎲 Monte Carlo Risk Simulation & P90 Outturn Analysis Report
**Project Name**: Offshore EPC Platform Drill Tower Project  
**Simulation Iterations**: 10,000 Runs (Triangular Risk Sampling)  
**Status Date**: August 31, 2026 (Month 8 / Status Week 36)  
**Author**: Frank Ellingsen, Lead Project Controller  

---

## Executive Summary & P90 Risk Card

A quantitative cost and schedule risk analysis (QCRA / QSRA) was executed using 10,000 Monte Carlo iterations across all 7 Control Accounts and critical path schedule deliverables.

> [!IMPORTANT]
> **P90 Outturn Forecast Summary**:
> - **P90 Outturn Cost**: **$35,815,202** ($-9.32\text{M}$ / $+35.2\%$ variance vs. $26.50\text{M}$ baseline $BAC$).
> - **P90 Contingency Reserve Needed**: **+$401,598** added to current $35.41\text{M}$ deterministic $EAC$.
> - **P90 Completion Date**: **March 14, 2027** ($+72.5\text{ Days}$ / $+2.4\text{ Months}$ schedule delay vs. Dec 31, 2026).

---

## 📊 Summary Table of Monte Carlo Risk Percentiles

| Risk Percentile | Confidence Level | Outturn Cost ($EAC$) | Cost Variance vs $BAC$ | Contingency Needed vs $EAC$ | Total Duration | Predicted Completion Date | Schedule Delay vs Dec 31 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **P10** | 10% (Optimistic / Low Risk) | **$32,444,302** | -$5,944,302 (-22.4%) | $0.00 | 408.1 Days | **Feb 13, 2027** | +43.1 Days (+1.4 Mos) |
| **P50** | 50% (Median / Expected) | **$34,060,783** | -$7,560,783 (-28.5%) | $0.00 | 422.3 Days | **Feb 27, 2027** | +57.3 Days (+1.9 Mos) |
| **P80** | 80% (Standard Budget Baseline) | **$35,195,026** | -$8,695,026 (-32.8%) | $0.00 | 432.3 Days | **Mar 09, 2027** | +67.3 Days (+2.2 Mos) |
| **P90** | **90% (P90 High Confidence)** | **$35,815,202** | **-$9,315,202 (-35.2%)** | **+$401,598** | **437.5 Days** | **March 14, 2027** | **+72.5 Days (+2.4 Mos)** |
| **P95** | 95% (Extreme Risk Boundary) | **$36,272,986** | -$9,772,986 (-36.9%) | +$859,382 | 441.6 Days | **March 18, 2027** | +76.6 Days (+2.5 Mos) |

---

## 1. Simulation Methodology & Input Risk Distributions

The simulation applies triangular probability distributions $(Optimistic, Most\text{ }Likely, Pessimistic)$ to each Control Account:

### Cost Inputs ($M USD)
- **WBS 1.1 Detail Engineering**: $(3.10, 3.50, 4.20)$
- **WBS 1.2 Procurement**: $(8.20, 9.10, 10.80)$
- **WBS 1.3.1 Verdal Fabrication**: $(4.80, 5.20, 6.00)$
- **WBS 1.3.2 Egersund Mast Rework**: $(5.50, 7.20, 9.50)$ *(Primary Cost Risk)*
- **WBS 1.4.1 Heavy Lift Vessel Mobilization**: $(3.20, 4.50, 6.80)$ *(Primary Weather Standby Risk)*
- **WBS 1.4.2 Topside Lifting & Mating**: $(1.10, 1.40, 2.10)$
- **WBS 1.5 Hook-up & Commissioning**: $(1.70, 1.90, 2.50)$

### Schedule Duration Inputs (Remaining Days along Critical Path)
- **T106 Derrick Mast Assembly (Egersund)**: $(20, 30, 45\text{ Days})$
- **T107 Heavy Lift Mobilization**: $(25, 30, 50\text{ Days})$
- **T108 Topside Lifting & Mating**: $(25, 31, 45\text{ Days})$
- **T109 Structural Hook-up & NDT**: $(25, 30, 45\text{ Days})$
- **T110 Pre-Commissioning & Handover**: $(35, 47, 65\text{ Days})$

---

## 2. Risk Driver Sensitivity & Tornado Analysis

1. **Egersund Assembly Yard Rework ($WBS\text{ }1.3.2$)**: Accounts for **48.2% of total cost variance**. Structural pipe tolerance issues require 24/7 NDT inspection and specialized welding crews.
2. **Offshore Weather Standby ($WBS\text{ }1.4.1$)**: Accounts for **36.5% of total schedule variance**. Shifting vessel mobilization from September into October/November exposes the heavy lift crane barge (*Heerema Sleipnir*) to North Sea sea-state limits ($Hs > 2.5m$).

---

## 3. Project Controller Recommendations for Steering Committee

1. **Establish P80 / P90 Financial Reserve**:
   - Approve a revised Control Budget of **$35.82M** ($P90$) by allocating a **+$401,598 management contingency reserve** on top of the $35.41\text{M}$ deterministic $EAC$.
2. **Schedule Target & Buffer**:
   - Establish **March 14, 2027** as the P90 contractual handover date for offshore commissioning.
3. **CSV Export**:
   - Simulation raw dataset saved to [`03_power_bi/Monte_Carlo_Simulation_Results.csv`](file:///C:/Users/frank/Desktop/EVM/03_power_bi/Monte_Carlo_Simulation_Results.csv).
