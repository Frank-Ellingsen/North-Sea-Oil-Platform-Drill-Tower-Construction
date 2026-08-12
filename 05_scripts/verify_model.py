import os
import duckdb
import sqlite3
import pandas as pd

def verify_all():
    print("=" * 80)
    print("Structured Workspace EVM Implementation Verification")
    print("=" * 80)

    base_dir = "C:/Users/frank/Desktop/EVM"

    files_to_check = [
        "01_raw_data/01_PV_Baseline.csv",
        "01_raw_data/02_EV_Progress.csv",
        "01_raw_data/03_AC_Actuals.csv",
        "01_raw_data/04_Dim_WBS.csv",
        "01_raw_data/EVM_Master_Data.xlsx",
        "01_raw_data/Drill_Tower_EVM_Report.xlsx",
        "02_databases/evm_analytics.duckdb",
        "02_databases/evm_transactional.db",
        "03_power_bi/Fact_EVM_Periodic.csv",
        "03_power_bi/Fact_Gantt_Schedule.csv",
        "03_power_bi/Dim_WBS.csv",
        "03_power_bi/Dim_Date.csv",
        "03_power_bi/EVM_DAX_Measures.dax",
        "03_power_bi/PowerBI_DAX_DrillTower.dax",
        "index.html",
        "04_dashboard/index.html",
        "04_dashboard/drill_tower_web_report.html",
        "05_scripts/create_excel_master.py",
        "05_scripts/etl_pipeline.py",
        "05_scripts/build_sqlite_db.py",
        "05_scripts/generate_drill_tower_data.py",
        "05_scripts/draw_erd.py",
        "05_scripts/test_and_revise_powerbi.py",
        "05_scripts/verify_model.py",
        "06_docs/erd_diagram.png",
        "06_docs/antigravity.md",
        "README.md"
    ]

    all_exist = True
    for f in files_to_check:
        full_path = os.path.join(base_dir, f)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f" [PASS] {f:<38} ({size:,} bytes)")
        else:
            print(f" [FAIL] {f:<38} MISSING!")
            all_exist = False

    print("\n--- Auditing DuckDB Star Schema Integrity ---")
    duck_path = os.path.join(base_dir, "02_databases/evm_analytics.duckdb")
    con = duckdb.connect(duck_path)
    
    fact_count = con.execute("SELECT COUNT(*) FROM fact_evm_periodic").fetchone()[0]
    wbs_count = con.execute("SELECT COUNT(*) FROM dim_wbs").fetchone()[0]
    date_count = con.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0]

    print(f" Fact_EVM_Periodic row count : {fact_count} (Expected: 120)")
    print(f" Dim_WBS row count            : {wbs_count} (Expected: 10)")
    print(f" Dim_Date row count           : {date_count} (Expected: 12)")

    bac_pv = con.execute("SELECT SUM(PV_Incremental) FROM fact_evm_periodic").fetchone()[0]
    bac_wbs = con.execute("SELECT SUM(TBC) FROM dim_wbs").fetchone()[0]
    print(f" Total Baseline Budget (BAC)  : ${bac_pv:,.2f}")
    
    if bac_pv == bac_wbs:
        print(" [PASS] Mathematical Check: Sum(PV_Incremental) == Sum(Dim_WBS.TBC)")
    else:
        print(f" [FAIL] Discrepancy between PV Incremental sum (${bac_pv:,.2f}) and Dim_WBS BAC (${bac_wbs:,.2f})!")

    con.close()

    print("\n--- Auditing SQLite Transactional Database Integrity ---")
    sqlite_path = os.path.join(base_dir, "02_databases/evm_transactional.db")
    s_conn = sqlite3.connect(sqlite_path)
    s_cur = s_conn.cursor()
    fk_errors = s_cur.execute("PRAGMA foreign_key_check;").fetchall()
    if not fk_errors:
        print(" [PASS] SQLite Foreign Key Integrity: PASSED (Zero Errors)")
    else:
        print(f" [FAIL] SQLite Foreign Key Errors: {fk_errors}")
    s_conn.close()

    if all_exist and bac_pv == bac_wbs and not fk_errors:
        print("\n>>> ALL STRUCTURED WORKSPACE CHECKS PASSED SUCCESSFULLY <<<")

if __name__ == "__main__":
    verify_all()
