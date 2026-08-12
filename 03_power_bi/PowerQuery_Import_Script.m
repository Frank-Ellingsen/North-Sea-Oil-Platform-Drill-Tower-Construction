// ===============================================================================
// POWER QUERY M IMPORT SCRIPT - OFFSHORE EPC PLATFORM DRILL TOWER PROJECT
// Ingests Star Schema CSV Data feeds from 03_power_bi/ directory
// ===============================================================================

let
    SourcePath = "C:\Users\frank\Desktop\EVM\03_power_bi\",
    
    // 1. Ingest Periodic EVM Fact Table
    Fact_EVM_Periodic = Csv.Document(File.Contents(SourcePath & "Fact_EVM_Periodic.csv"),[Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_EVM_Headers = Table.PromoteHeaders(Fact_EVM_Periodic, [PromoteAllScalars=true]),
    
    // 2. Ingest Gantt Schedule Fact Table
    Fact_Gantt_Schedule = Csv.Document(File.Contents(SourcePath & "Fact_Gantt_Schedule.csv"),[Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Gantt_Headers = Table.PromoteHeaders(Fact_Gantt_Schedule, [PromoteAllScalars=true]),

    // 3. Ingest Key Milestones Table
    Fact_Milestones = Csv.Document(File.Contents(SourcePath & "Fact_Milestones.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Milestones_Headers = Table.PromoteHeaders(Fact_Milestones, [PromoteAllScalars=true]),

    // 4. Ingest Risk Register Table
    Fact_Risk_Register = Csv.Document(File.Contents(SourcePath & "Fact_Risk_Register.csv"),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Risk_Headers = Table.PromoteHeaders(Fact_Risk_Register, [PromoteAllScalars=true]),

    // 5. Ingest Cost Waterfall Bridge Table
    Fact_Waterfall_Bridge = Csv.Document(File.Contents(SourcePath & "Fact_Waterfall_Bridge.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Waterfall_Headers = Table.PromoteHeaders(Fact_Waterfall_Bridge, [PromoteAllScalars=true]),

    // 6. Ingest Monthly Cash Burn Table
    Fact_Monthly_Burn_Rate = Csv.Document(File.Contents(SourcePath & "Fact_Monthly_Burn_Rate.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Burn_Headers = Table.PromoteHeaders(Fact_Monthly_Burn_Rate, [PromoteAllScalars=true]),

    // 7. Ingest Financial Appraisal Table
    Fact_Financial_Appraisal = Csv.Document(File.Contents(SourcePath & "Fact_Financial_Appraisal.csv"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Appraisal_Headers = Table.PromoteHeaders(Fact_Financial_Appraisal, [PromoteAllScalars=true]),

    // 8. Ingest Monte Carlo P90 Table
    Fact_Monte_Carlo = Csv.Document(File.Contents(SourcePath & "Fact_Monte_Carlo.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Fact_Monte_Headers = Table.PromoteHeaders(Fact_Monte_Carlo, [PromoteAllScalars=true]),

    // 9. Ingest Dim_WBS
    Dim_WBS = Csv.Document(File.Contents(SourcePath & "Dim_WBS.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Dim_WBS_Headers = Table.PromoteHeaders(Dim_WBS, [PromoteAllScalars=true]),

    // 10. Ingest Dim_Date
    Dim_Date = Csv.Document(File.Contents(SourcePath & "Dim_Date.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Dim_Date_Headers = Table.PromoteHeaders(Dim_Date, [PromoteAllScalars=true])
in
    Dim_Date_Headers
