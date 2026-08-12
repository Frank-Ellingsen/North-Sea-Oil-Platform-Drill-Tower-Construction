import duckdb
import pandas as pd
import os

def run_evm_etl():
    print("=" * 80)
    print("Starting DuckDB EVM ETL & Analytical Engine...")
    print("=" * 80)

    base_dir = "C:/Users/frank/Desktop/EVM"
    raw_dir = os.path.join(base_dir, "01_raw_data")
    db_dir = os.path.join(base_dir, "02_databases")
    pbi_dir = os.path.join(base_dir, "03_power_bi")

    db_path = os.path.join(db_dir, "evm_analytics.duckdb")
    con = duckdb.connect(db_path)

    # 1. Read Raw Wide-Format CSVs into DuckDB Tables
    con.execute(f"CREATE OR REPLACE TABLE raw_pv AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, '01_PV_Baseline.csv').replace('\\', '/')}');")
    con.execute(f"CREATE OR REPLACE TABLE raw_ev AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, '02_EV_Progress.csv').replace('\\', '/')}');")
    con.execute(f"CREATE OR REPLACE TABLE raw_ac AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, '03_AC_Actuals.csv').replace('\\', '/')}');")
    con.execute(f"CREATE OR REPLACE TABLE dim_wbs AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, '04_Dim_WBS.csv').replace('\\', '/')}');")

    print("[ETL 1/5] Raw wide-format tables ingested into DuckDB.")

    # 2. Unpivot PV Baseline
    con.execute("""
    CREATE OR REPLACE TABLE unpivoted_pv AS
    UNPIVOT raw_pv
    ON Month_1, Month_2, Month_3, Month_4, Month_5, Month_6, Month_7, Month_8, Month_9, Month_10, Month_11, Month_12
    INTO
        NAME Period_Raw
        VALUE PV_Incremental;
    """)

    # 3. Unpivot EV Progress % Complete
    con.execute("""
    CREATE OR REPLACE TABLE unpivoted_ev AS
    UNPIVOT raw_ev
    ON "Month_1_%", "Month_2_%", "Month_3_%", "Month_4_%", "Month_5_%", "Month_6_%", "Month_7_%", "Month_8_%", "Month_9_%", "Month_10_%", "Month_11_%", "Month_12_%"
    INTO
        NAME Period_Raw
        VALUE EV_Physical_Percent;
    """)

    con.execute("""
    UPDATE unpivoted_ev
    SET Period_Raw = REPLACE(Period_Raw, '_%', '');
    """)

    # 4. Unpivot AC Actuals
    con.execute("""
    CREATE OR REPLACE TABLE unpivoted_ac AS
    UNPIVOT raw_ac
    ON Month_1_AC, Month_2_AC, Month_3_AC, Month_4_AC, Month_5_AC, Month_6_AC, Month_7_AC, Month_8_AC, Month_9_AC, Month_10_AC, Month_11_AC, Month_12_AC
    INTO
        NAME Period_Raw
        VALUE AC_Incremental;
    """)

    con.execute("""
    UPDATE unpivoted_ac
    SET Period_Raw = REPLACE(Period_Raw, '_AC', '');
    """)

    print("[ETL 2/5] Wide-format columns unpivoted successfully.")

    # 5. Create Calendar Dimension (Dim_Date)
    con.execute("""
    CREATE OR REPLACE TABLE dim_date AS
    WITH Dates AS (
        SELECT CAST(UNNEST(generate_series(DATE '2026-01-01', DATE '2026-12-01', INTERVAL 1 MONTH)) AS DATE) AS Month_Start
    )
    SELECT
        LAST_DAY(Month_Start) AS Date_Key,
        YEAR(Month_Start) AS Year,
        MONTH(Month_Start) AS Month_Number,
        STRFTIME(Month_Start, '%B') AS Month_Name,
        STRFTIME(Month_Start, '%Y-%m') AS Year_Month,
        'Q' || CAST(CEIL(MONTH(Month_Start) / 3.0) AS INT) AS Quarter,
        'Month_' || CAST(MONTH(Month_Start) AS VARCHAR) AS Period_Raw
    FROM Dates;
    """)

    print("[ETL 3/5] Dim_Date calendar dimension created.")

    # 6. Join Unpivoted Fact Tables & Compute Incremental EV
    con.execute("""
    CREATE OR REPLACE TABLE fact_evm_staged AS
    SELECT 
        pv.Item_ID AS Task_ID,
        d.Date_Key,
        d.Period_Raw,
        w.TBC AS Total_Budget_Cost,
        COALESCE(pv.PV_Incremental, 0) AS PV_Incremental,
        COALESCE(ev.EV_Physical_Percent, 0) AS EV_Physical_Percent,
        COALESCE(ac.AC_Incremental, 0) AS AC_Incremental
    FROM unpivoted_pv pv
    JOIN dim_date d ON pv.Period_Raw = d.Period_Raw
    JOIN dim_wbs w ON pv.Item_ID = w.Task_ID
    LEFT JOIN unpivoted_ev ev ON pv.Item_ID = ev.Item_ID AND pv.Period_Raw = ev.Period_Raw
    LEFT JOIN unpivoted_ac ac ON pv.Item_ID = ac.Item_ID AND pv.Period_Raw = ac.Period_Raw
    ORDER BY pv.Item_ID, d.Date_Key;
    """)

    con.execute("""
    CREATE OR REPLACE TABLE fact_evm_periodic AS
    WITH LaggedPercent AS (
        SELECT 
            Task_ID,
            Date_Key,
            Period_Raw,
            Total_Budget_Cost,
            PV_Incremental,
            EV_Physical_Percent,
            COALESCE(LAG(EV_Physical_Percent, 1) OVER (PARTITION BY Task_ID ORDER BY Date_Key), 0.0) AS Prev_EV_Percent,
            AC_Incremental
        FROM fact_evm_staged
    )
    SELECT
        Task_ID,
        Date_Key,
        Period_Raw,
        Total_Budget_Cost,
        PV_Incremental,
        EV_Physical_Percent,
        (EV_Physical_Percent - Prev_EV_Percent) AS EV_Incremental_Percent,
        ROUND((EV_Physical_Percent - Prev_EV_Percent) * Total_Budget_Cost, 2) AS EV_Incremental_Calculated,
        AC_Incremental
    FROM LaggedPercent;
    """)

    print("[ETL 4/5] Fact_EVM_Periodic synthesized with incremental Earned Value calculations.")

    # Export clean CSV files for Power BI ingestion
    fact_csv = os.path.join(pbi_dir, "Fact_EVM_Periodic.csv").replace('\\', '/')
    wbs_csv = os.path.join(pbi_dir, "Dim_WBS.csv").replace('\\', '/')
    date_csv = os.path.join(pbi_dir, "Dim_Date.csv").replace('\\', '/')

    con.execute(f"COPY (SELECT Task_ID, Date_Key, Total_Budget_Cost, PV_Incremental, EV_Physical_Percent, EV_Incremental_Calculated, AC_Incremental FROM fact_evm_periodic) TO '{fact_csv}' (HEADER, DELIMITER ',');")
    con.execute(f"COPY (SELECT * FROM dim_wbs) TO '{wbs_csv}' (HEADER, DELIMITER ',');")
    con.execute(f"COPY (SELECT Date_Key, Year, Month_Number, Month_Name, Year_Month, Quarter FROM dim_date) TO '{date_csv}' (HEADER, DELIMITER ',');")

    print("\n[SUCCESS] Relational Star Schema exported to 03_power_bi/:")
    print(f"  - {fact_csv}")
    print(f"  - {wbs_csv}")
    print(f"  - {date_csv}")
    print(f"  - {db_path} (DuckDB analytical database)")

    con.close()

if __name__ == "__main__":
    run_evm_etl()
