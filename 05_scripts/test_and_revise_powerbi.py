import pandas as pd
import numpy as np
import os

def test_powerbi_project():
    print("=" * 80)
    print("Power BI Project Audit, Automated Testing & Verification")
    print("=" * 80)

    base_dir = "C:/Users/frank/Desktop/EVM"
    pbi_dir = os.path.join(base_dir, "03_power_bi")

    # Load Power BI Datasets
    df_wbs = pd.read_csv(os.path.join(pbi_dir, "Dim_WBS.csv"))
    df_date = pd.read_csv(os.path.join(pbi_dir, "Dim_Date.csv"))
    df_evm = pd.read_csv(os.path.join(pbi_dir, "Fact_EVM_Periodic.csv"))
    df_gantt = pd.read_csv(os.path.join(pbi_dir, "Fact_Gantt_Schedule.csv"))

    # Audit 1: Check Referential Integrity
    wbs_keys = set(df_wbs["Task_ID"])
    evm_task_keys = set(df_evm["Task_ID"])
    gantt_task_keys = set(df_gantt["Task_ID"])
    date_keys = set(df_date["Date_Key"])
    evm_date_keys = set(df_evm["Date_Key"])

    print("\n--- Test 1: Star Schema Referential Integrity Audit ---")
    assert evm_task_keys.issubset(wbs_keys), "[FAIL] Unmatched Task_ID in Fact_EVM_Periodic!"
    print(" [PASS] Fact_EVM_Periodic[Task_ID] -> Dim_WBS[Task_ID]")

    assert gantt_task_keys.issubset(wbs_keys), "[FAIL] Unmatched Task_ID in Fact_Gantt_Schedule!"
    print(" [PASS] Fact_Gantt_Schedule[Task_ID] -> Dim_WBS[Task_ID]")

    assert evm_date_keys.issubset(date_keys), "[FAIL] Unmatched Date_Key in Fact_EVM_Periodic!"
    print(" [PASS] Fact_EVM_Periodic[Date_Key] -> Dim_Date[Date_Key]")

    # Audit 2: Validate Gantt Schedule Dependencies
    print("\n--- Test 2: Gantt Schedule Dependencies & Predecessor Audit ---")
    predecessors = df_gantt["Predecessor_Task_ID"].dropna().unique()
    for pred in predecessors:
        # Predecessor might contain lag notes like "T101 (+5D)"
        clean_pred = pred.split()[0]
        assert clean_pred in wbs_keys, f"[FAIL] Predecessor {clean_pred} not found in Dim_WBS!"
    print(f" [PASS] All {len(predecessors)} Predecessor Dependencies validly map to WBS Primary Keys.")

    # Audit 3: Math Consistency Audit on Month 8 (Status Date: Aug 31, 2026)
    print("\n--- Test 3: DAX Performance Measure & Mathematical Outturn Audit ---")
    bac = df_wbs["TBC"].sum()
    pv_cum = df_evm[df_evm["Date_Key"] <= "2026-08-31"]["PV_Incremental"].sum()
    ev_cum = df_evm[df_evm["Date_Key"] <= "2026-08-31"]["EV_Incremental_Calculated"].sum()
    ac_cum = df_evm[df_evm["Date_Key"] <= "2026-08-31"]["AC_Incremental"].sum()

    cv = ev_cum - ac_cum
    sv = ev_cum - pv_cum
    cpi = round(ev_cum / ac_cum, 4)
    spi = round(ev_cum / pv_cum, 4)
    eac = round(bac / cpi, 2)
    vac = round(bac - eac, 2)

    print(f" Total Baseline BAC          : ${bac:,.2f}")
    print(f" Month 8 Cumulative PV       : ${pv_cum:,.2f}")
    print(f" Month 8 Cumulative EV       : ${ev_cum:,.2f}")
    print(f" Month 8 Cumulative AC       : ${ac_cum:,.2f}")
    print(f" Month 8 Cost Variance (CV)  : ${cv:,.2f}")
    print(f" Month 8 Schedule Var (SV)   : ${sv:,.2f}")
    print(f" Month 8 CPI Efficiency      : {cpi}")
    print(f" Month 8 SPI Velocity        : {spi}")
    print(f" Outturn Forecast EAC        : ${eac:,.2f}")
    print(f" Variance at Completion VAC  : ${vac:,.2f}")

    assert bac == 26500000.0, "[FAIL] BAC mismatch!"
    assert cpi == 0.7483, f"[FAIL] CPI calculation mismatch! Got {cpi}"
    print(" [PASS] Mathematical DAX calculations 100% verified.")

    print("\n>>> ALL POWER BI PROJECT AUDIT TESTS PASSED SUCCESSFULLY <<<")

if __name__ == "__main__":
    test_powerbi_project()
