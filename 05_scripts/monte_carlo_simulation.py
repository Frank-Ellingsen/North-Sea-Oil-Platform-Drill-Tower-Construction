import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
N_SIMULATIONS = 10000

print("================================================================================")
print(f"RUNNING MONTE CARLO RISK SIMULATION ({N_SIMULATIONS:,} ITERATIONS)")
print("PROJECT: Offshore EPC Platform Drill Tower Project")
print("STATUS DATE: August 31, 2026 (Month 8 / Status Week 36)")
print("================================================================================")

# ------------------------------------------------------------------------------
# 1. COST DISTRIBUTION INPUTS (Triangular Distributions: Optimistic, Most Likely, Pessimistic)
# ------------------------------------------------------------------------------
# Baseline Budget (BAC) = $26.50M, Outturn Forecast = $35.41M
wbs_cost_params = {
    "1.1 Engineering": (3.10, 3.50, 4.20),
    "1.2 Procurement": (8.20, 9.10, 10.80),
    "1.3.1 Verdal Sub-Structure": (4.80, 5.20, 6.00),
    "1.3.2 Egersund Mast Rework": (5.50, 7.20, 9.50),  # High volatility
    "1.4.1 Heavy Lift Vessel Mobilization": (3.20, 4.50, 6.80),  # Weather standby risk
    "1.4.2 Topside Lifting & Mating": (1.10, 1.40, 2.10),
    "1.5 Hook-up & Commissioning": (1.70, 1.90, 2.50)
}

simulated_costs = np.zeros(N_SIMULATIONS)
for wbs, (opt, ml, pess) in wbs_cost_params.items():
    simulated_costs += np.random.triangular(opt, ml, pess, N_SIMULATIONS)

simulated_costs *= 1e6  # Convert $M to $

# ------------------------------------------------------------------------------
# 2. SCHEDULE DURATION INPUTS (Remaining Critical Path Work from Month 8 / Aug 31)
# ------------------------------------------------------------------------------
# Elapsed Time at Month 8 = 240 Days (Jan 01 - Aug 31)
# Remaining baseline duration = 125 Days (Sep 01 - Dec 31 -> Total 365 Days)
wbs_schedule_params = {
    "T106 Derrick Mast Assembly (Egersund)": (20, 30, 45),   # Target Sep 30 (30 days remaining)
    "T107 Heavy Lift Mobilization": (25, 30, 50),           # Target Oct 15
    "T108 Topside Lifting & Mating": (25, 31, 45),          # Target Nov 15
    "T109 Structural Hook-up & NDT": (25, 30, 45),          # Target Dec 15
    "T110 Pre-Commissioning & Handover": (35, 47, 65)       # Target Jan 31
}

elapsed_days = 240
simulated_remaining_days = np.zeros(N_SIMULATIONS)
for task, (opt, ml, pess) in wbs_schedule_params.items():
    simulated_remaining_days += np.random.triangular(opt, ml, pess, N_SIMULATIONS)

simulated_total_days = elapsed_days + simulated_remaining_days

# ------------------------------------------------------------------------------
# 3. PERCENTILE STATISTICAL CALCULATIONS
# ------------------------------------------------------------------------------
percentiles = [10, 50, 80, 90, 95]
cost_p = {p: np.percentile(simulated_costs, p) for p in percentiles}
days_p = {p: np.percentile(simulated_total_days, p) for p in percentiles}

# Convert days to completion dates from Jan 1, 2026
base_date = datetime(2026, 1, 1)
dates_p = {p: (base_date + timedelta(days=float(days_p[p]))).strftime("%Y-%m-%d") for p in percentiles}

bac = 26500000.0
eac_base = 35413604.0

# Build Results Dataframe
df_results = pd.DataFrame({
    "Percentile": [f"P{p}" for p in percentiles],
    "Confidence Level": ["10% (Optimistic)", "50% (Median)", "80% (Standard Budget)", "90% (P90 High Confidence)", "95% (Extreme Risk)"],
    "Outturn Cost (EAC)": [f"${cost_p[p]:,.2f}" for p in percentiles],
    "Cost Overrun vs BAC": [f"-${cost_p[p] - bac:,.2f}" for p in percentiles],
    "Contingency Reserve Needed": [f"+${max(0, cost_p[p] - eac_base):,.2f}" for p in percentiles],
    "Total Duration (Days)": [f"{days_p[p]:.1f} Days" for p in percentiles],
    "Predicted Completion Date": [dates_p[p] for p in percentiles],
    "Schedule Delay vs Dec 31": [f"+{days_p[p] - 365:.1f} Days" for p in percentiles]
})

print("\n--- MONTE CARLO COST & SCHEDULE PERCENTILE OUTCOMES ---")
print(df_results.to_string(index=False))

print("\n--------------------------------------------------------------------------------")
print(f"P90 HIGH CONFIDENCE COST FORECAST  : ${cost_p[90]:,.2f} (Overrun: -${cost_p[90] - bac:,.2f})")
print(f"P90 HIGH CONFIDENCE FINISH DATE   : {dates_p[90]} ({days_p[90]:.1f} Days total / +{days_p[90] - 365:.1f} Days delay)")
print(f"P90 CONTINGENCY RESERVE REQUIRED  : +${max(0, cost_p[90] - eac_base):,.2f} above $35.41M EAC")
print("================================================================================")

# Export summary CSV
df_results.to_csv("03_power_bi/Monte_Carlo_Simulation_Results.csv", index=False)
print("Saved summary to 03_power_bi/Monte_Carlo_Simulation_Results.csv")
