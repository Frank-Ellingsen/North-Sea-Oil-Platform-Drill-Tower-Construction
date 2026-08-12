# 🚨 Project Risk Matrix & Quantitative Risk Register
**Project Name**: Offshore EPC Platform Drill Tower Project  
**Status Date**: August 31, 2026 (Month 8 / Status Week 36)  
**Author**: Frank Ellingsen, Lead Project Controller  

---

## 🎯 Executive Risk Heatmap Matrix (5x5 Grid)

The 5x5 Risk Heatmap Matrix plots project risks by **Probability (Likelihood 1-5)** versus **Impact (Severity 1-5)**. Total Risk Score = $Probability \times Impact$.

```
PROBABILITY
 (5) Almost Certain |  [5]   |  [10]  |  [15]  |  [20]  |  [25]  |
 (4) High           |  [4]   |  [8]   |  [12]  | 🚨 R02 | 🚨 R01 |  <-- CRITICAL ZONE
 (3) Moderate       |  [3]   |  [6]   | ⚠️ R04 | ⚠️ R03 |  [15]  |
 (2) Low            |  [2]   |  [4]   | 🟢 R05 |  [8]   |  [10]  |
 (1) Rare           |  [1]   |  [2]   |  [3]   |  [4]   |  [5]   |
                    +--------+--------+--------+--------+--------+
                       (1)      (2)      (3)      (4)      (5)
                       Negligible Minor Moderate Major Critical
                                      IMPACT
```

---

## 📋 Comprehensive Risk Register & Mitigation Action Plan

| Risk ID | Risk Category | Risk Event Description | WBS | Risk Owner (CAM) | Prob (1-5) | Imp (1-5) | Risk Score | Risk Exposure ($) | Actionable Mitigation Strategy | Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **R01** | **Fabrication** | **Egersund Mast Assembly Dimensional Out-of-Tolerance & Yard Labor Rework** | 1.3.2 | O. Eriksen | 4 | 5 | <span class="badge badge-red">20 (Critical)</span> | **$2,400,000** | Deploy 24/7 dual-shift NDT welding specialists; cap yard labor billing under a fixed-fee agreement. | **Active** |
| **R02** | **Offshore Marine** | **Heavy Lift Vessel Mobilization Delay & North Sea Weather Standby** | 1.4.1 | K. Solberg | 4 | 4 | <span class="badge badge-red">16 (Critical)</span> | **$1,800,000** | Negotiate flexible weather window with Heerema; monitor 7-day wave height ($Hs < 2.5m$). | **Active** |
| **R03** | **Procurement** | **High-Grade Subsea Tubular Steel Mill Delivery Lags & Price Inflation** | 1.2.1 | M. Berg | 3 | 4 | <span class="badge badge-amber">12 (High)</span> | **$1,200,000** | Dual-source tubular steel from European backup mills; arrange expedited hot-shot freight. | **Monitored** |
| **R04** | **Offshore Hook-Up** | **Topside Lifting & Mating Mechanical Interface Interference** | 1.4.2 | T. Nygård | 3 | 3 | <span class="badge badge-amber">9 (Medium)</span> | **$600,000** | Perform 3D laser scan trial fit at Egersund yard prior to offshore mobilization. | **Monitored** |
| **R05** | **Engineering** | **Structural Detail Engineering Interface Errors & AFC Revisions** | 1.1.1 | H. Lindqvist | 2 | 3 | <span class="badge badge-green">6 (Low)</span> | **$300,000** | Enforce 100% 3D CAD clash detection and third-party DNV class design verification. | **Closed** |

---

## 💰 Quantitative Financial Risk Summary

- **Total Unmitigated Financial Exposure**: **$6,300,000**
- **Post-Mitigation Expected Monetary Value (EMV)**: **$3,410,000**
- **Recommended Management Risk Reserve**: **$3,500,000** (Aligned with P90 Monte Carlo simulation reserve of $+\$401,598$ above $35.41\text{M}$ outturn).

---

## 🛡️ Risk Governance & Escalation Triggers

1. **Red Risk Escalation (Score $\ge 15$)**: Weekly review with Project Director & CFO. Immediate CAM intervention required.
2. **Amber Risk Monitoring (Score $8 - 14$)**: Bi-weekly review at Project Control Meetings.
3. **Green Risk Tracking (Score $\le 7$)**: Monthly review by CAMs.
