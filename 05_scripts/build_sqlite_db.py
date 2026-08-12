import sqlite3
import pandas as pd
import os

def create_sqlite_database():
    base_dir = "C:/Users/frank/Desktop/EVM"
    db_dir = os.path.join(base_dir, "02_databases")
    pbi_dir = os.path.join(base_dir, "03_power_bi")

    db_path = os.path.join(db_dir, "evm_transactional.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    print("=" * 80)
    print(f"Building Production SQLite Database ({db_path})...")
    print("=" * 80)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE Dim_WBS (
        Task_ID TEXT PRIMARY KEY,
        WBS_Code TEXT NOT NULL,
        WBS_Level_1 TEXT NOT NULL,
        WBS_Level_2 TEXT NOT NULL,
        Task_Name TEXT NOT NULL,
        CAM TEXT NOT NULL,
        TBC REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Dim_Date (
        Date_Key TEXT PRIMARY KEY,
        Year INTEGER NOT NULL,
        Month_Number INTEGER NOT NULL,
        Month_Name TEXT NOT NULL,
        Year_Month TEXT NOT NULL,
        Quarter TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Fact_EVM_Periodic (
        Fact_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Task_ID TEXT NOT NULL,
        Date_Key TEXT NOT NULL,
        Total_Budget_Cost REAL NOT NULL,
        PV_Incremental REAL NOT NULL,
        EV_Physical_Percent REAL NOT NULL,
        EV_Incremental_Calculated REAL NOT NULL,
        AC_Incremental REAL NOT NULL,
        FOREIGN KEY (Task_ID) REFERENCES Dim_WBS (Task_ID) ON DELETE CASCADE,
        FOREIGN KEY (Date_Key) REFERENCES Dim_Date (Date_Key) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE Fact_Gantt_Schedule (
        Task_ID TEXT PRIMARY KEY,
        Task_Name TEXT NOT NULL,
        WBS_Code TEXT NOT NULL,
        CAM TEXT NOT NULL,
        Baseline_Start TEXT NOT NULL,
        Baseline_End TEXT NOT NULL,
        Actual_Start TEXT NOT NULL,
        Actual_End TEXT NOT NULL,
        Predecessor_Task_ID TEXT,
        Predecessor_Name TEXT,
        Dependency_Type TEXT,
        Lag_Days INTEGER DEFAULT 0,
        Percent_Complete REAL NOT NULL,
        Critical_Path_Flag TEXT NOT NULL,
        Resource_Group TEXT NOT NULL,
        FOREIGN KEY (Task_ID) REFERENCES Dim_WBS (Task_ID) ON DELETE CASCADE
    );
    """)

    df_wbs = pd.read_csv(os.path.join(pbi_dir, "Dim_WBS.csv"))
    df_wbs.to_sql("Dim_WBS", conn, if_exists="append", index=False)
    print(f"[SQLite] Ingested {len(df_wbs)} rows into Dim_WBS.")

    df_date = pd.read_csv(os.path.join(pbi_dir, "Dim_Date.csv"))
    df_date.to_sql("Dim_Date", conn, if_exists="append", index=False)
    print(f"[SQLite] Ingested {len(df_date)} rows into Dim_Date.")

    df_fact = pd.read_csv(os.path.join(pbi_dir, "Fact_EVM_Periodic.csv"))
    df_fact.to_sql("Fact_EVM_Periodic", conn, if_exists="append", index=False)
    print(f"[SQLite] Ingested {len(df_fact)} rows into Fact_EVM_Periodic.")

    df_gantt = pd.read_csv(os.path.join(pbi_dir, "Fact_Gantt_Schedule.csv"))
    df_gantt.to_sql("Fact_Gantt_Schedule", conn, if_exists="append", index=False)
    print(f"[SQLite] Ingested {len(df_gantt)} rows into Fact_Gantt_Schedule.")

    cursor.execute("""
    CREATE VIEW View_EVM_Summary AS
    SELECT 
        w.Task_ID,
        w.Task_Name,
        w.WBS_Code,
        w.CAM,
        f.Date_Key,
        f.Total_Budget_Cost AS BAC,
        f.PV_Incremental,
        f.EV_Incremental_Calculated,
        f.AC_Incremental,
        ROUND(f.EV_Incremental_Calculated - f.AC_Incremental, 2) AS CV,
        ROUND(f.EV_Incremental_Calculated - f.PV_Incremental, 2) AS SV,
        CASE WHEN f.AC_Incremental = 0 THEN 1.0 ELSE ROUND(f.EV_Incremental_Calculated / f.AC_Incremental, 4) END AS CPI,
        CASE WHEN f.PV_Incremental = 0 THEN 1.0 ELSE ROUND(f.EV_Incremental_Calculated / f.PV_Incremental, 4) END AS SPI,
        CASE 
            WHEN (CASE WHEN f.AC_Incremental = 0 THEN 1.0 ELSE f.EV_Incremental_Calculated / f.AC_Incremental END) >= 1.0 THEN 'GREEN'
            WHEN (CASE WHEN f.AC_Incremental = 0 THEN 1.0 ELSE f.EV_Incremental_Calculated / f.AC_Incremental END) >= 0.90 THEN 'AMBER'
            ELSE 'RED'
        END AS CPI_RAG_Status,
        CASE 
            WHEN (CASE WHEN f.PV_Incremental = 0 THEN 1.0 ELSE f.EV_Incremental_Calculated / f.PV_Incremental END) >= 1.0 THEN 'GREEN'
            WHEN (CASE WHEN f.PV_Incremental = 0 THEN 1.0 ELSE f.EV_Incremental_Calculated / f.PV_Incremental END) >= 0.95 THEN 'AMBER'
            ELSE 'RED'
        END AS SPI_RAG_Status
    FROM Fact_EVM_Periodic f
    JOIN Dim_WBS w ON f.Task_ID = w.Task_ID
    JOIN Dim_Date d ON f.Date_Key = d.Date_Key;
    """)

    conn.commit()
    
    fk_errors = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    if not fk_errors:
        print("[SQLite] Foreign Key Integrity Audit: PASSED (Zero Errors).")
    else:
        print(f"[SQLite] Foreign Key Errors: {fk_errors}")

    conn.close()
    print("SQLite database successfully built at:", db_path)

if __name__ == "__main__":
    create_sqlite_database()
