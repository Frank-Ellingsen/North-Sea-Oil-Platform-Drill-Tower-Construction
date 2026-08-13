import numpy as np

capex = 35413604.0  # Forecast EAC Outturn
annual_cf = 8000000.0  # Net Annual Operating Cash Flow
salvage = 3000000.0  # Terminal Residual Value
years = 10
r = 0.10  # 10% Hurdle Rate / WACC

cash_flows = [-capex] + [annual_cf]*9 + [annual_cf + salvage]

# 1. Net Present Value (NPV)
npv = sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows))

# 2. Internal Rate of Return (IRR)
def get_npv(rate):
    return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cash_flows))

low, high = 0.0, 1.0
for _ in range(100):
    mid = (low + high) / 2
    if get_npv(mid) > 0:
        low = mid
    else:
        high = mid
irr = mid

# 3. Payback Period
payback = capex / annual_cf

# 4. Return on Investment (ROI)
total_inflow = sum(cash_flows[1:])
simple_roi = ((total_inflow - capex) / capex) * 100
annualized_roi = ((total_inflow / capex) ** (1/years) - 1) * 100

# 5. Profitability Index (PI) / Benefit-Cost Ratio
pv_inflows = sum(cf / ((1 + r) ** t) for t, cf in enumerate(cash_flows[1:], 1))
pi = pv_inflows / capex

# 6. Future Value (FV) & Net Future Value (NFV)
fv_capex = capex * ((1 + r) ** years)
fv_cashflows = sum(cf * ((1 + r) ** (years - t)) for t, cf in enumerate(cash_flows[1:], 1))
net_fv = fv_cashflows - fv_capex

# 7. EVM Performance Indices & Critical Ratio (CR)
ev = 17540000.0
pv = 20500000.0
ac = 23440000.0
cpi = ev / ac
spi = ev / pv
cr = cpi * spi

print("================================================================================")
print("COMMERCIAL CAPITAL BUDGETING & APPRAISAL METRICS (DRILL TOWER PROJECT)")
print("================================================================================")
print(f"CAPEX Outturn (EAC Forecast) : ${capex:,.2f}")
print(f"Annual Net Operating Cash Flow: ${annual_cf:,.2f}/year (Years 1-10)")
print(f"Discount Rate / WACC (r)      : {r*100:.1f}%")
print(f"Project Lifetime             : {years} Years")
print("--------------------------------------------------------------------------------")
print(f"1. Net Present Value (NPV)    : +${npv:,.2f}")
print(f"2. Internal Rate of Return    : {irr*100:.2f}% (Hurdle Rate: 10.0%)")
print(f"3. Simple Payback Period      : {payback:.2f} Years ({payback*12:.1f} Months)")
print(f"4. Total Simple ROI           : {simple_roi:.2f}%")
print(f"5. Annualized ROI (CAGR)      : {annualized_roi:.2f}%")
print(f"6. Profitability Index (PI)   : {pi:.2f} (Benefit-Cost Ratio)")
print(f"7. Present Value of Inflows   : ${pv_inflows:,.2f}")
print(f"8. Future Value (FV at Yr 10) : ${fv_cashflows:,.2f}")
print(f"9. Net Future Value (NFV)     : +${net_fv:,.2f}")
print("--------------------------------------------------------------------------------")
print(f"EVM Cost Performance (CPI)   : {cpi:.4f} ($0.75 Earned per $1.00 Spent)")
print(f"EVM Schedule Velocity (SPI)  : {spi:.4f} (Scope Progress Lag)")
print(f"EVM Critical Ratio (CR=CPI*SPI): {cr:.4f} (Critical Red < 0.90)")
print("================================================================================")

