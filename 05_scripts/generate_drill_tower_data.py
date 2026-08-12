import pandas as pd
import numpy as np
import datetime
import os
import duckdb
import sqlite3

def generate_drill_tower_dataset():
    print("=" * 80)
    print("Generating North Sea Drill Tower Construction Project Dataset...")
    print("=" * 80)

    base_dir = "C:/Users/frank/Desktop/EVM"
    raw_dir = os.path.join(base_dir, "01_raw_data")
    db_dir = os.path.join(base_dir, "02_databases")
    pbi_dir = os.path.join(base_dir, "03_power_bi")

    # 1. WBS Dimension (Dim_WBS.csv)
    wbs_data = [
        {"Task_ID": "T101", "WBS_Code": "1.1.1", "WBS_Level_1": "1.0 Engineering", "WBS_Level_2": "1.1 Design", "Task_Name": "Structural Steel Detail Engineering", "CAM": "H. Lindqvist", "TBC": 1200000},
        {"Task_ID": "T102", "WBS_Code": "1.1.2", "WBS_Level_1": "1.0 Engineering", "WBS_Level_2": "1.1 Design", "Task_Name": "Piping & Drilling Package Design", "CAM": "H. Lindqvist", "TBC": 1800000},
        {"Task_ID": "T103", "WBS_Code": "1.2.1", "WBS_Level_1": "2.0 Procurement", "WBS_Level_2": "2.1 Materials", "Task_Name": "High-Grade Tubular Steel Procurement", "CAM": "M. Berg", "TBC": 3500000},
        {"Task_ID": "T104", "WBS_Code": "1.2.2", "WBS_Level_1": "2.0 Procurement", "WBS_Level_2": "2.2 Machinery", "Task_Name": "Mud Pumps & Top Drive Equipment", "CAM": "M. Berg", "TBC": 4200000},
        {"Task_ID": "T105", "WBS_Code": "1.3.1", "WBS_Level_1": "3.0 Fabrication", "WBS_Level_2": "3.1 Sub-Structure", "Task_Name": "Yard Sub-Structure Fabrication (Verdal)", "CAM": "O. Eriksen", "TBC": 4000000},
        {"Task_ID": "T106", "WBS_Code": "1.3.2", "WBS_Level_1": "3.0 Fabrication", "WBS_Level_2": "3.2 Derrick Mast", "Task_Name": "Derrick Tower Mast Assembly (Egersund)", "CAM": "O. Eriksen", "TBC": 4800000},
        {"Task_ID": "T107", "WBS_Code": "1.4.1", "WBS_Level_1": "4.0 Offshore Lift", "WBS_Level_2": "4.1 Heavy Lift", "Task_Name": "Heavy Lift Vessel Mobilization (Heerema)", "CAM": "K. Solberg", "TBC": 2500000},
        {"Task_ID": "T108", "WBS_Code": "1.4.2", "WBS_Level_1": "4.0 Offshore Lift", "WBS_Level_2": "4.2 Installation", "Task_Name": "Offshore Topside Lifting & Mating", "CAM": "K. Solberg", "TBC": 2000000},
        {"Task_ID": "T109", "WBS_Code": "1.5.1", "WBS_Level_1": "5.0 Integration", "WBS_Level_2": "5.1 Hook-Up", "Task_Name": "Structural Hook-up & NDT Inspection", "CAM": "T. Nygård", "TBC": 1000000},
        {"Task_ID": "T110", "WBS_Code": "1.5.2", "WBS_Level_1": "5.0 Integration", "WBS_Level_2": "5.2 Commissioning", "Task_Name": "System Pre-Commissioning & Handover", "CAM": "T. Nygård", "TBC": 1500000}
    ]
    df_wbs = pd.DataFrame(wbs_data)
    df_wbs.to_csv(os.path.join(raw_dir, "04_Dim_WBS.csv"), index=False)
    df_wbs.to_csv(os.path.join(pbi_dir, "Dim_WBS.csv"), index=False)

    # 2. Gantt Schedule & Dependencies Table (Fact_Gantt_Schedule.csv)
    gantt_data = [
        {"Task_ID": "T101", "Task_Name": "Structural Steel Detail Engineering", "WBS_Code": "1.1.1", "CAM": "H. Lindqvist", "Baseline_Start": "2026-01-05", "Baseline_End": "2026-02-28", "Actual_Start": "2026-01-05", "Actual_End": "2026-03-15", "Predecessor_Task_ID": None, "Predecessor_Name": None, "Dependency_Type": None, "Lag_Days": 0, "Percent_Complete": 1.00, "Critical_Path_Flag": "Yes", "Resource_Group": "Engineering Team"},
        {"Task_ID": "T102", "Task_Name": "Piping & Drilling Package Design", "WBS_Code": "1.1.2", "CAM": "H. Lindqvist", "Baseline_Start": "2026-02-01", "Baseline_End": "2026-03-31", "Actual_Start": "2026-02-01", "Actual_End": "2026-04-15", "Predecessor_Task_ID": "T101", "Predecessor_Name": "Structural Steel Detail Engineering", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 1.00, "Critical_Path_Flag": "No", "Resource_Group": "Engineering Team"},
        {"Task_ID": "T103", "Task_Name": "High-Grade Tubular Steel Procurement", "WBS_Code": "1.2.1", "CAM": "M. Berg", "Baseline_Start": "2026-03-01", "Baseline_End": "2026-04-30", "Actual_Start": "2026-03-15", "Actual_End": "2026-05-31", "Predecessor_Task_ID": "T101", "Predecessor_Name": "Structural Steel Detail Engineering", "Dependency_Type": "FS", "Lag_Days": 5, "Percent_Complete": 1.00, "Critical_Path_Flag": "Yes", "Resource_Group": "Procurement Team"},
        {"Task_ID": "T104", "Task_Name": "Mud Pumps & Top Drive Equipment", "WBS_Code": "1.2.2", "CAM": "M. Berg", "Baseline_Start": "2026-03-15", "Baseline_End": "2026-06-30", "Actual_Start": "2026-04-01", "Actual_End": "2026-07-31", "Predecessor_Task_ID": "T102", "Predecessor_Name": "Piping & Drilling Package Design", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.85, "Critical_Path_Flag": "No", "Resource_Group": "Procurement Team"},
        {"Task_ID": "T105", "Task_Name": "Yard Sub-Structure Fabrication (Verdal)", "WBS_Code": "1.3.1", "CAM": "O. Eriksen", "Baseline_Start": "2026-05-01", "Baseline_End": "2026-07-31", "Actual_Start": "2026-06-01", "Actual_End": "2026-08-31", "Predecessor_Task_ID": "T103", "Predecessor_Name": "High-Grade Tubular Steel Procurement", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.90, "Critical_Path_Flag": "Yes", "Resource_Group": "Verdal Fabrication Yard"},
        {"Task_ID": "T106", "Task_Name": "Derrick Tower Mast Assembly (Egersund)", "WBS_Code": "1.3.2", "CAM": "O. Eriksen", "Baseline_Start": "2026-06-01", "Baseline_End": "2026-08-31", "Actual_Start": "2026-07-01", "Actual_End": "2026-09-30", "Predecessor_Task_ID": "T105", "Predecessor_Name": "Yard Sub-Structure Fabrication (Verdal)", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.65, "Critical_Path_Flag": "Yes", "Resource_Group": "Egersund Rigging Yard"},
        {"Task_ID": "T107", "Task_Name": "Heavy Lift Vessel Mobilization (Heerema)", "WBS_Code": "1.4.1", "CAM": "K. Solberg", "Baseline_Start": "2026-08-15", "Baseline_End": "2026-09-15", "Actual_Start": "2026-09-15", "Actual_End": "2026-10-15", "Predecessor_Task_ID": "T106", "Predecessor_Name": "Derrick Tower Mast Assembly (Egersund)", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.30, "Critical_Path_Flag": "Yes", "Resource_Group": "Offshore Marine Fleet"},
        {"Task_ID": "T108", "Task_Name": "Offshore Topside Lifting & Mating", "WBS_Code": "1.4.2", "CAM": "K. Solberg", "Baseline_Start": "2026-09-15", "Baseline_End": "2026-10-15", "Actual_Start": "2026-10-15", "Actual_End": "2026-11-15", "Predecessor_Task_ID": "T107", "Predecessor_Name": "Heavy Lift Vessel Mobilization (Heerema)", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.00, "Critical_Path_Flag": "Yes", "Resource_Group": "Offshore Marine Fleet"},
        {"Task_ID": "T109", "Task_Name": "Structural Hook-up & NDT Inspection", "WBS_Code": "1.5.1", "CAM": "T. Nygård", "Baseline_Start": "2026-10-15", "Baseline_End": "2026-11-15", "Actual_Start": "2026-11-15", "Actual_End": "2026-12-15", "Predecessor_Task_ID": "T108", "Predecessor_Name": "Offshore Topside Lifting & Mating", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.00, "Critical_Path_Flag": "Yes", "Resource_Group": "Offshore Hook-Up Crew"},
        {"Task_ID": "T110", "Task_Name": "System Pre-Commissioning & Handover", "WBS_Code": "1.5.2", "CAM": "T. Nygård", "Baseline_Start": "2026-11-15", "Baseline_End": "2026-12-31", "Actual_Start": "2026-12-15", "Actual_End": "2027-01-31", "Predecessor_Task_ID": "T109", "Predecessor_Name": "Structural Hook-up & NDT Inspection", "Dependency_Type": "FS", "Lag_Days": 0, "Percent_Complete": 0.00, "Critical_Path_Flag": "Yes", "Resource_Group": "Commissioning Team"}
    ]
    df_gantt = pd.DataFrame(gantt_data)
    df_gantt.to_csv(os.path.join(pbi_dir, "Fact_Gantt_Schedule.csv"), index=False)

    # 3. Monthly Fact_EVM_Periodic.csv (12 Months Jan-Dec 2026)
    dates = pd.date_range(start="2026-01-31", periods=12, freq="ME")
    periodic_records = []

    # Monthly Planned Value Allocations ($26.5M Total BAC)
    pv_matrix = {
        "T101": [300000, 500000, 400000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "T102": [0, 400000, 800000, 600000, 0, 0, 0, 0, 0, 0, 0, 0],
        "T103": [0, 0, 1000000, 2000000, 500000, 0, 0, 0, 0, 0, 0, 0],
        "T104": [0, 0, 500000, 1200000, 1500000, 1000000, 0, 0, 0, 0, 0, 0],
        "T105": [0, 0, 0, 0, 1000000, 2000000, 1000000, 0, 0, 0, 0, 0],
        "T106": [0, 0, 0, 0, 0, 1000000, 2000000, 1800000, 0, 0, 0, 0],
        "T107": [0, 0, 0, 0, 0, 0, 0, 1000000, 1500000, 0, 0, 0],
        "T108": [0, 0, 0, 0, 0, 0, 0, 0, 1000000, 1000000, 0, 0],
        "T109": [0, 0, 0, 0, 0, 0, 0, 0, 0, 500000, 500000, 0],
        "T110": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500000, 1000000]
    }

    # Cumulative Physical % Complete through Month 8 (Status Date: Aug 31, 2026)
    ev_percent_matrix = {
        "T101": [0.25, 0.65, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
        "T102": [0.00, 0.20, 0.60, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
        "T103": [0.00, 0.00, 0.20, 0.70, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
        "T104": [0.00, 0.00, 0.10, 0.35, 0.60, 0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85],
        "T105": [0.00, 0.00, 0.00, 0.00, 0.20, 0.55, 0.80, 0.90, 0.90, 0.90, 0.90, 0.90],
        "T106": [0.00, 0.00, 0.00, 0.00, 0.00, 0.15, 0.40, 0.65, 0.65, 0.65, 0.65, 0.65],
        "T107": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.30, 0.30, 0.30, 0.30],
        "T108": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        "T109": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        "T110": [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    }

    # Monthly Incremental Actual Spend ($ AC)
    ac_matrix = {
        "T101": [320000, 540000, 430000, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "T102": [0, 410000, 850000, 620000, 0, 0, 0, 0, 0, 0, 0, 0],
        "T103": [0, 0, 1100000, 2150000, 520000, 0, 0, 0, 0, 0, 0, 0],
        "T104": [0, 0, 520000, 1280000, 1600000, 1100000, 450000, 0, 0, 0, 0, 0],
        "T105": [0, 0, 0, 0, 1100000, 2200000, 1150000, 450000, 0, 0, 0, 0],
        "T106": [0, 0, 0, 0, 0, 1150000, 2250000, 2050000, 0, 0, 0, 0],
        "T107": [0, 0, 0, 0, 0, 0, 0, 1200000, 0, 0, 0, 0],
        "T108": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "T109": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "T110": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    for m_idx, dt in enumerate(dates):
        date_str = dt.strftime("%Y-%m-%d")
        for task in wbs_data:
            tid = task["Task_ID"]
            tbc = task["TBC"]
            pv_inc = pv_matrix[tid][m_idx]
            cum_pct = ev_percent_matrix[tid][m_idx]
            prev_pct = ev_percent_matrix[tid][m_idx - 1] if m_idx > 0 else 0.0
            inc_pct = cum_pct - prev_pct
            ev_inc = round(inc_pct * tbc, 2)
            ac_inc = ac_matrix[tid][m_idx]

            periodic_records.append({
                "Task_ID": tid,
                "Date_Key": date_str,
                "Total_Budget_Cost": tbc,
                "PV_Incremental": pv_inc,
                "EV_Physical_Percent": cum_pct,
                "EV_Incremental_Calculated": ev_inc,
                "AC_Incremental": ac_inc
            })

    df_fact_evm = pd.DataFrame(periodic_records)
    df_fact_evm.to_csv(os.path.join(pbi_dir, "Fact_EVM_Periodic.csv"), index=False)

    # 4. Dim_Date.csv
    date_records = []
    for dt in dates:
        date_records.append({
            "Date_Key": dt.strftime("%Y-%m-%d"),
            "Year": dt.year,
            "Month_Number": dt.month,
            "Month_Name": dt.strftime("%B"),
            "Year_Month": dt.strftime("%Y-%m"),
            "Quarter": f"Q{(dt.month-1)//3 + 1}"
        })
    df_dim_date = pd.DataFrame(date_records)
    df_dim_date.to_csv(os.path.join(pbi_dir, "Dim_Date.csv"), index=False)

    # Export Wide-Format CSVs to 01_raw_data/
    pv_rows = []
    ev_rows = []
    ac_rows = []
    months_header = [f"Month_{i}" for i in range(1, 13)]

    for task in wbs_data:
        tid = task["Task_ID"]
        wbs = task["WBS_Code"]
        tname = task["Task_Name"]
        tbc = task["TBC"]

        # PV Row
        pv_row = {"Item_ID": tid, "WBS_Code": wbs, "Task_Name": tname, "TBC": tbc}
        for i, val in enumerate(pv_matrix[tid], start=1):
            pv_row[f"Month_{i}"] = val
        pv_rows.append(pv_row)

        # EV % Row
        ev_row = {"Item_ID": tid, "WBS_Code": wbs, "Task_Name": tname, "TBC": tbc}
        for i, val in enumerate(ev_percent_matrix[tid], start=1):
            ev_row[f"Month_{i}_%"] = val
        ev_rows.append(ev_row)

        # AC Row
        ac_row = {"Item_ID": tid, "WBS_Code": wbs, "Task_Name": tname, "TBC": tbc}
        for i, val in enumerate(ac_matrix[tid], start=1):
            ac_row[f"Month_{i}_AC"] = val
        ac_rows.append(ac_row)

    pd.DataFrame(pv_rows).to_csv(os.path.join(raw_dir, "01_PV_Baseline.csv"), index=False)
    pd.DataFrame(ev_rows).to_csv(os.path.join(raw_dir, "02_EV_Progress.csv"), index=False)
    pd.DataFrame(ac_rows).to_csv(os.path.join(raw_dir, "03_AC_Actuals.csv"), index=False)

    print(f"[SUCCESS] Drill Tower Mockup Dataset Generated:")
    print(f"  - Dim_WBS.csv ({len(df_wbs)} Control Accounts)")
    print(f"  - Fact_Gantt_Schedule.csv ({len(df_gantt)} Schedule Tasks with Predecessors)")
    print(f"  - Fact_EVM_Periodic.csv ({len(df_fact_evm)} Monthly Periodic Postings)")
    print(f"  - Dim_Date.csv ({len(df_dim_date)} Calendar Periods)")

if __name__ == "__main__":
    generate_drill_tower_dataset()
