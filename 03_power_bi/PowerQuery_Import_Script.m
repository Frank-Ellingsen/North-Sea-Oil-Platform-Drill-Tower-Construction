// ===============================================================================
// POWER QUERY M IMPORT SCRIPT - OFFSHORE EPC PLATFORM DRILL TOWER PROJECT
// Ingests Star Schema CSV Data feeds from 03_power_bi/ directory with Explicit Column Types
// ===============================================================================

let
    SourcePath = "C:\Users\frank\Desktop\EVM\03_power_bi\",
    
    // 1. Ingest Periodic EVM Fact Table
    Fact_EVM_Periodic_Csv = Csv.Document(File.Contents(SourcePath & "Fact_EVM_Periodic.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_EVM_Headers = Table.PromoteHeaders(Fact_EVM_Periodic_Csv, [PromoteAllScalars=true]),
    Fact_EVM_Periodic = Table.TransformColumnTypes(Fact_EVM_Headers, {
        {"Task_ID", type text},
        {"Date_Key", type date},
        {"Total_Budget_Cost", Currency.Type},
        {"PV_Incremental", Currency.Type},
        {"EV_Physical_Percent", type number},
        {"EV_Incremental_Calculated", Currency.Type},
        {"AC_Incremental", Currency.Type}
    }),
    
    // 2. Ingest Gantt Schedule Fact Table
    Fact_Gantt_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Gantt_Schedule.csv"),[Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Gantt_Headers = Table.PromoteHeaders(Fact_Gantt_Csv, [PromoteAllScalars=true]),
    Fact_Gantt_Schedule = Table.TransformColumnTypes(Fact_Gantt_Headers, {
        {"Task_ID", type text},
        {"Task_Name", type text},
        {"WBS_Code", type text},
        {"CAM", type text},
        {"Baseline_Start", type date},
        {"Baseline_End", type date},
        {"Actual_Start", type date},
        {"Actual_End", type date},
        {"Predecessor_Task_ID", type text},
        {"Predecessor_Name", type text},
        {"Dependency_Type", type text},
        {"Lag_Days", Int64.Type},
        {"Percent_Complete", type number},
        {"Critical_Path_Flag", type text},
        {"Resource_Group", type text}
    }),

    // 3. Ingest Key Milestones Table
    Fact_Milestones_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Milestones.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Milestones_Headers = Table.PromoteHeaders(Fact_Milestones_Csv, [PromoteAllScalars=true]),
    Fact_Milestones = Table.TransformColumnTypes(Fact_Milestones_Headers, {
        {"Milestone_ID", type text},
        {"Milestone_Name", type text},
        {"Target_Date", type date},
        {"Baseline_Date", type date},
        {"Status", type text},
        {"RAG", type text},
        {"WBS_Code", type text}
    }),

    // 4. Ingest Risk Register Table
    Fact_Risk_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Risk_Register.csv"),[Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Risk_Headers = Table.PromoteHeaders(Fact_Risk_Csv, [PromoteAllScalars=true]),
    Fact_Risk_Register = Table.TransformColumnTypes(Fact_Risk_Headers, {
        {"Risk_ID", type text},
        {"Risk_Title", type text},
        {"Category", type text},
        {"Probability", Int64.Type},
        {"Impact", Int64.Type},
        {"Risk_Score", Int64.Type},
        {"RAG_Level", type text},
        {"Financial_Exposure", Currency.Type},
        {"Expected_Monetary_Value", Currency.Type},
        {"Mitigation_Strategy", type text},
        {"CAM_Owner", type text}
    }),

    // 5. Ingest Cost Waterfall Bridge Table
    Fact_Waterfall_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Waterfall_Bridge.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Waterfall_Headers = Table.PromoteHeaders(Fact_Waterfall_Csv, [PromoteAllScalars=true]),
    Fact_Waterfall_Bridge = Table.TransformColumnTypes(Fact_Waterfall_Headers, {
        {"Step_ID", Int64.Type},
        {"Component_Name", type text},
        {"Type", type text},
        {"Incremental_Cost", Currency.Type},
        {"Cumulative_Cost", Currency.Type},
        {"Pct_Share", type number},
        {"Description", type text}
    }),

    // 6. Ingest Monthly Cash Burn Table
    Fact_Burn_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Monthly_Burn_Rate.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Burn_Headers = Table.PromoteHeaders(Fact_Burn_Csv, [PromoteAllScalars=true]),
    Fact_Monthly_Burn_Rate = Table.TransformColumnTypes(Fact_Burn_Headers, {
        {"Period", type text},
        {"Monthly_PV", Currency.Type},
        {"Monthly_EV", Currency.Type},
        {"Monthly_AC", Currency.Type},
        {"Cum_AC", Currency.Type},
        {"Remaining_BAC", Currency.Type},
        {"Runway_Status", type text}
    }),

    // 7. Ingest Financial Appraisal Table
    Fact_Appraisal_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Financial_Appraisal.csv"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Appraisal_Headers = Table.PromoteHeaders(Fact_Appraisal_Csv, [PromoteAllScalars=true]),
    Fact_Financial_Appraisal = Table.TransformColumnTypes(Fact_Appraisal_Headers, {
        {"Metric", type text},
        {"Value", type text},
        {"Numeric_Value", type number},
        {"Unit", type text},
        {"Evaluation", type text}
    }),

    // 8. Ingest Monte Carlo P90 Table
    Fact_Monte_Csv = Csv.Document(File.Contents(SourcePath & "Fact_Monte_Carlo.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Monte_Headers = Table.PromoteHeaders(Fact_Monte_Csv, [PromoteAllScalars=true]),
    Fact_Monte_Carlo = Table.TransformColumnTypes(Fact_Monte_Headers, {
        {"Percentile", type text},
        {"Confidence_Level", type text},
        {"Outturn_Cost_EAC", Currency.Type},
        {"Cost_Overrun_VAC", Currency.Type},
        {"Contingency_Reserve", Currency.Type},
        {"Duration_Days", type number},
        {"Completion_Date", type date},
        {"Schedule_Delay_Days", type number}
    }),

    // 9. Ingest Dim_WBS
    Dim_WBS_Csv = Csv.Document(File.Contents(SourcePath & "Dim_WBS.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Dim_WBS_Headers = Table.PromoteHeaders(Dim_WBS_Csv, [PromoteAllScalars=true]),
    Dim_WBS = Table.TransformColumnTypes(Dim_WBS_Headers, {
        {"Task_ID", type text},
        {"WBS_Code", type text},
        {"WBS_Level_1", type text},
        {"WBS_Level_2", type text},
        {"Task_Name", type text},
        {"CAM", type text},
        {"TBC", Currency.Type}
    }),

    // 10. Ingest Dim_Date
    Dim_Date_Csv = Csv.Document(File.Contents(SourcePath & "Dim_Date.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Dim_Date_Headers = Table.PromoteHeaders(Dim_Date_Csv, [PromoteAllScalars=true]),
    Dim_Date = Table.TransformColumnTypes(Dim_Date_Headers, {
        {"Date_Key", type date},
        {"Month_Name", type text},
        {"Month_Number", Int64.Type},
        {"Year", Int64.Type}
    })
in
    Fact_EVM_Periodic
