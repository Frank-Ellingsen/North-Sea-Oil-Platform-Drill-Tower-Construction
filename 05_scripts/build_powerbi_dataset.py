import os
import sys
import json

# Ensure UTF-8 console output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_powerbi_solution():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pbi_dir = os.path.join(base_dir, "03_power_bi")
    os.makedirs(pbi_dir, exist_ok=True)

    print("=" * 80)
    print("Building Enterprise Power BI Tabular Data Model & Master Specification...")
    print("=" * 80)

    # 1. Complete TOM (Tabular Object Model) BIM Schema
    bim_model = {
        "name": "Drill_Tower_EVM_Master_Model",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "Dim_WBS",
                    "columns": [
                        {"name": "Task_ID", "dataType": "string", "isKey": True},
                        {"name": "WBS_Code", "dataType": "string"},
                        {"name": "WBS_Level_1", "dataType": "string"},
                        {"name": "WBS_Level_2", "dataType": "string"},
                        {"name": "Task_Name", "dataType": "string"},
                        {"name": "CAM", "dataType": "string"},
                        {"name": "TBC", "dataType": "decimal", "formatString": "$#,##0"},
                        {
                            "name": "WBS_Category",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "SWITCH(TRUE(), LEFT(Dim_WBS[WBS_Code], 3) = \"1.1\", \"Engineering\", LEFT(Dim_WBS[WBS_Code], 3) = \"1.2\", \"Procurement\", LEFT(Dim_WBS[WBS_Code], 3) = \"1.3\", \"Yard Fabrication\", LEFT(Dim_WBS[WBS_Code], 3) = \"1.4\", \"Offshore Installation\", LEFT(Dim_WBS[WBS_Code], 3) = \"1.5\", \"Commissioning\", \"General PMO\")"
                        }
                    ],
                    "measures": [
                        {
                            "name": "Total_Budget_at_Completion_BAC",
                            "expression": "SUM(Dim_WBS[TBC])",
                            "formatString": "$#,##0"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Dim_WBS.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Task_ID", type text}, {"WBS_Code", type text}, {"WBS_Level_1", type text}, {"WBS_Level_2", type text}, {"Task_Name", type text}, {"CAM", type text}, {"TBC", Currency.Type}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Date",
                    "columns": [
                        {"name": "Date_Key", "dataType": "dateTime", "formatString": "yyyy-MM-dd", "isKey": True},
                        {"name": "Month_Name", "dataType": "string"},
                        {"name": "Month_Number", "dataType": "int64"},
                        {"name": "Year", "dataType": "int64"}
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Dim_Date.csv"),[Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date_Key", type date}, {"Month_Name", type text}, {"Month_Number", Int64.Type}, {"Year", Int64.Type}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_EVM_Periodic",
                    "columns": [
                        {"name": "Task_ID", "dataType": "string"},
                        {"name": "Date_Key", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Total_Budget_Cost", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "PV_Incremental", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "EV_Physical_Percent", "dataType": "double", "formatString": "0.0%"},
                        {"name": "EV_Incremental_Calculated", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "AC_Incremental", "dataType": "decimal", "formatString": "$#,##0"}
                    ],
                    "measures": [
                        {
                            "name": "Status_Date",
                            "expression": "MAX(Fact_EVM_Periodic[Date_Key])",
                            "formatString": "yyyy-MM-dd"
                        },
                        {
                            "name": "PV_Incremental_Period",
                            "expression": "SUM(Fact_EVM_Periodic[PV_Incremental])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "EV_Incremental_Period",
                            "expression": "SUM(Fact_EVM_Periodic[EV_Incremental_Calculated])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "AC_Incremental_Period",
                            "expression": "SUM(Fact_EVM_Periodic[AC_Incremental])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "PV_S_Curve",
                            "expression": "CALCULATE(SUM(Fact_EVM_Periodic[PV_Incremental]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key])))",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "EV_S_Curve",
                            "expression": "VAR CurrentDate = MAX(Dim_Date[Date_Key]) RETURN IF(CurrentDate <= [Status_Date], CALCULATE(SUM(Fact_EVM_Periodic[EV_Incremental_Calculated]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key]))), BLANK())",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "AC_S_Curve",
                            "expression": "VAR CurrentDate = MAX(Dim_Date[Date_Key]) RETURN IF(CurrentDate <= [Status_Date], CALCULATE(SUM(Fact_EVM_Periodic[AC_Incremental]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key]))), BLANK())",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Cost_Variance_CV",
                            "expression": "[EV_S_Curve] - [AC_S_Curve]",
                            "formatString": "$#,##0;($#,##0);$0"
                        },
                        {
                            "name": "Cost_Variance_CV_Pct",
                            "expression": "DIVIDE([Cost_Variance_CV], [EV_S_Curve], 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "Schedule_Variance_SV",
                            "expression": "[EV_S_Curve] - [PV_S_Curve]",
                            "formatString": "$#,##0;($#,##0);$0"
                        },
                        {
                            "name": "Schedule_Variance_SV_Pct",
                            "expression": "DIVIDE([Schedule_Variance_SV], [PV_S_Curve], 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "Cost_Performance_Index_CPI",
                            "expression": "DIVIDE([EV_S_Curve], [AC_S_Curve], 1.0)",
                            "formatString": "0.0000"
                        },
                        {
                            "name": "Schedule_Performance_Index_SPI",
                            "expression": "DIVIDE([EV_S_Curve], [PV_S_Curve], 1.0)",
                            "formatString": "0.0000"
                        },
                        {
                            "name": "Critical_Ratio_CR",
                            "expression": "[Cost_Performance_Index_CPI] * [Schedule_Performance_Index_SPI]",
                            "formatString": "0.0000"
                        },
                        {
                            "name": "PM_Overall_Completion_Pct",
                            "expression": "DIVIDE([EV_S_Curve], [Total_Budget_at_Completion_BAC], 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "Estimate_at_Completion_EAC",
                            "expression": "DIVIDE([Total_Budget_at_Completion_BAC], [Cost_Performance_Index_CPI], [Total_Budget_at_Completion_BAC])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Variance_at_Completion_VAC",
                            "expression": "[Total_Budget_at_Completion_BAC] - [Estimate_at_Completion_EAC]",
                            "formatString": "$#,##0;($#,##0);$0"
                        },
                        {
                            "name": "TCPI_BAC",
                            "expression": "VAR BAC = [Total_Budget_at_Completion_BAC] VAR EV = [EV_S_Curve] VAR AC = [AC_S_Curve] RETURN DIVIDE(BAC - EV, BAC - AC, 1.0)",
                            "formatString": "0.00"
                        },
                        {
                            "name": "TCPI_EAC",
                            "expression": "VAR BAC = [Total_Budget_at_Completion_BAC] VAR EAC = [Estimate_at_Completion_EAC] VAR EV = [EV_S_Curve] VAR AC = [AC_S_Curve] RETURN DIVIDE(BAC - EV, EAC - AC, 1.0)",
                            "formatString": "0.00"
                        },
                        {
                            "name": "ETC_Remaining_Liquidity_Needed",
                            "expression": "[Estimate_at_Completion_EAC] - [AC_S_Curve]",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Earned_Schedule_Months",
                            "expression": "VAR CurrentEV = [EV_S_Curve] VAR DateTableWithPV = FILTER(ALL(Dim_Date), [PV_S_Curve] <= CurrentEV) VAR C_MonthDate = MAXX(DateTableWithPV, Dim_Date[Date_Key]) VAR C_MonthNumber = MAXX(DateTableWithPV, Dim_Date[Month_Number]) VAR PV_At_C = CALCULATE([PV_S_Curve], Dim_Date[Date_Key] = C_MonthDate) VAR PV_At_C_Plus_1 = CALCULATE([PV_S_Curve], DATEADD(Dim_Date[Date_Key], 1, MONTH)) VAR Interpolation = DIVIDE(CurrentEV - PV_At_C, PV_At_C_Plus_1 - PV_At_C, 0) RETURN IF(CurrentEV >= [Total_Budget_at_Completion_BAC], MAX(Dim_Date[Month_Number]), C_MonthNumber + Interpolation)",
                            "formatString": "0.00"
                        },
                        {
                            "name": "SPI_Time_Based",
                            "expression": "DIVIDE([Earned_Schedule_Months], MAX(Dim_Date[Month_Number]), 1.0)",
                            "formatString": "0.0000"
                        },
                        {
                            "name": "Time_Variance_Days",
                            "expression": "VAR ActualMonths = MAX(Dim_Date[Month_Number]) VAR ES_Months = [Earned_Schedule_Months] RETURN ROUND((ES_Months - ActualMonths) * 30.4375, 0)",
                            "formatString": "0"
                        },
                        {
                            "name": "Scatter_X_Schedule_Variance_Pct",
                            "expression": "DIVIDE([Schedule_Variance_SV], [PV_S_Curve], 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "Scatter_Y_Cost_Variance_Pct",
                            "expression": "DIVIDE([Cost_Variance_CV], [EV_S_Curve], 0)",
                            "formatString": "0.0%"
                        },
                        {
                            "name": "CPI_RAG_Color",
                            "expression": "VAR CPI = [Cost_Performance_Index_CPI] RETURN SWITCH(TRUE(), CPI < 0.90, \"#DC2626\", CPI < 1.00, \"#D97706\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "SPI_RAG_Color",
                            "expression": "VAR SPI = [Schedule_Performance_Index_SPI] RETURN SWITCH(TRUE(), SPI < 0.95, \"#DC2626\", SPI < 1.00, \"#D97706\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "CV_RAG_Color",
                            "expression": "VAR CV = [Cost_Variance_CV] RETURN IF(CV < 0, \"#DC2626\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "SV_RAG_Color",
                            "expression": "VAR SV = [Schedule_Variance_SV] RETURN IF(SV < 0, \"#D97706\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "VAC_RAG_Color",
                            "expression": "VAR VAC = [Variance_at_Completion_VAC] RETURN IF(VAC < 0, \"#DC2626\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "TCPI_RAG_Color",
                            "expression": "VAR TCPI = [TCPI_BAC] VAR CPI = [Cost_Performance_Index_CPI] RETURN IF(TCPI - CPI > 0.10, \"#DC2626\", \"#059669\")",
                            "formatString": "string"
                        },
                        {
                            "name": "CR_RAG_Color",
                            "expression": "VAR CR = [Critical_Ratio_CR] RETURN SWITCH(TRUE(), ISBLANK(CR), \"#737373\", CR < 0.90, \"#DC2626\", CR < 1.00, \"#D97706\", \"#059669\")",
                            "formatString": "string"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_EVM_Periodic.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Task_ID", type text}, {"Date_Key", type date}, {"Total_Budget_Cost", Currency.Type}, {"PV_Incremental", Currency.Type}, {"EV_Physical_Percent", type number}, {"EV_Incremental_Calculated", Currency.Type}, {"AC_Incremental", Currency.Type}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Gantt_Schedule",
                    "columns": [
                        {"name": "Task_ID", "dataType": "string", "isKey": True},
                        {"name": "Task_Name", "dataType": "string"},
                        {"name": "WBS_Code", "dataType": "string"},
                        {"name": "CAM", "dataType": "string"},
                        {"name": "Baseline_Start", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Baseline_End", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Actual_Start", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Actual_End", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Predecessor_Task_ID", "dataType": "string"},
                        {"name": "Predecessor_Name", "dataType": "string"},
                        {"name": "Dependency_Type", "dataType": "string"},
                        {"name": "Lag_Days", "dataType": "int64"},
                        {"name": "Percent_Complete", "dataType": "double", "formatString": "0.0%"},
                        {"name": "Critical_Path_Flag", "dataType": "string"},
                        {"name": "Resource_Group", "dataType": "string"},
                        {
                            "name": "Baseline_Duration_Days",
                            "dataType": "int64",
                            "type": "calculated",
                            "expression": "DATEDIFF(Fact_Gantt_Schedule[Baseline_Start], Fact_Gantt_Schedule[Baseline_End], DAY)"
                        },
                        {
                            "name": "Actual_Duration_Days",
                            "dataType": "int64",
                            "type": "calculated",
                            "expression": "DATEDIFF(Fact_Gantt_Schedule[Actual_Start], Fact_Gantt_Schedule[Actual_End], DAY)"
                        },
                        {
                            "name": "Schedule_Variance_Days",
                            "dataType": "int64",
                            "type": "calculated",
                            "expression": "DATEDIFF(Fact_Gantt_Schedule[Baseline_End], Fact_Gantt_Schedule[Actual_End], DAY)"
                        },
                        {
                            "name": "Start_Slippage_Days",
                            "dataType": "int64",
                            "type": "calculated",
                            "expression": "DATEDIFF(Fact_Gantt_Schedule[Baseline_Start], Fact_Gantt_Schedule[Actual_Start], DAY)"
                        },
                        {
                            "name": "Is_Critical_Path",
                            "dataType": "boolean",
                            "type": "calculated",
                            "expression": "IF(Fact_Gantt_Schedule[Critical_Path_Flag] = \"Yes\", TRUE(), FALSE())"
                        },
                        {
                            "name": "Is_Milestone",
                            "dataType": "boolean",
                            "type": "calculated",
                            "expression": "IF(LEFT(Fact_Gantt_Schedule[Task_ID], 1) = \"M\", TRUE(), FALSE())"
                        },
                        {
                            "name": "Milestone_Symbol",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "IF(LEFT(Fact_Gantt_Schedule[Task_ID], 1) = \"M\", \"◆\", \"\")"
                        }
                    ],
                    "measures": [
                        {
                            "name": "PM_Critical_Path_Task_Count",
                            "expression": "CALCULATE(COUNTROWS(Fact_Gantt_Schedule), Fact_Gantt_Schedule[Critical_Path_Flag] = \"Yes\")",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "PM_Critical_Path_Delayed_Tasks",
                            "expression": "CALCULATE(COUNTROWS(Fact_Gantt_Schedule), Fact_Gantt_Schedule[Critical_Path_Flag] = \"Yes\", Fact_Gantt_Schedule[Percent_Complete] < 1.0, Fact_Gantt_Schedule[Actual_End] > Fact_Gantt_Schedule[Baseline_End])",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "PM_Schedule_Slippage_Days_Max",
                            "expression": "MAXX(Fact_Gantt_Schedule, DATEDIFF(Fact_Gantt_Schedule[Baseline_End], Fact_Gantt_Schedule[Actual_End], DAY))",
                            "formatString": "+#,##0 Days"
                        },
                        {
                            "name": "Planner_Cascading_Delay_Tasks",
                            "expression": "CALCULATE(COUNTROWS(Fact_Gantt_Schedule), NOT(ISBLANK(Fact_Gantt_Schedule[Predecessor_Task_ID])), Fact_Gantt_Schedule[Actual_Start] > Fact_Gantt_Schedule[Baseline_Start])",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Planner_Avg_Task_Delay_Days",
                            "expression": "AVERAGEX(Fact_Gantt_Schedule, DATEDIFF(Fact_Gantt_Schedule[Baseline_End], Fact_Gantt_Schedule[Actual_End], DAY))",
                            "formatString": "+0.0 Days"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Gantt_Schedule.csv"),[Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Task_ID", type text}, {"Task_Name", type text}, {"WBS_Code", type text}, {"CAM", type text}, {"Baseline_Start", type date}, {"Baseline_End", type date}, {"Actual_Start", type date}, {"Actual_End", type date}, {"Predecessor_Task_ID", type text}, {"Predecessor_Name", type text}, {"Dependency_Type", type text}, {"Lag_Days", Int64.Type}, {"Percent_Complete", type number}, {"Critical_Path_Flag", type text}, {"Resource_Group", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Milestones",
                    "columns": [
                        {"name": "Milestone_ID", "dataType": "string", "isKey": True},
                        {"name": "Milestone_Name", "dataType": "string"},
                        {"name": "Target_Date", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Baseline_Date", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Status", "dataType": "string"},
                        {"name": "RAG", "dataType": "string"},
                        {"name": "WBS_Code", "dataType": "string"}
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Milestones.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Milestone_ID", type text}, {"Milestone_Name", type text}, {"Target_Date", type date}, {"Baseline_Date", type date}, {"Status", type text}, {"RAG", type text}, {"WBS_Code", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Risk_Register",
                    "columns": [
                        {"name": "Risk_ID", "dataType": "string", "isKey": True},
                        {"name": "Risk_Title", "dataType": "string"},
                        {"name": "Category", "dataType": "string"},
                        {"name": "Probability", "dataType": "int64"},
                        {"name": "Impact", "dataType": "int64"},
                        {"name": "Risk_Score", "dataType": "int64"},
                        {"name": "RAG_Level", "dataType": "string"},
                        {"name": "Financial_Exposure", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Expected_Monetary_Value", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Mitigation_Strategy", "dataType": "string"},
                        {"name": "CAM_Owner", "dataType": "string"},
                        {
                            "name": "Calculated_Risk_Score",
                            "dataType": "int64",
                            "type": "calculated",
                            "expression": "Fact_Risk_Register[Probability] * Fact_Risk_Register[Impact]"
                        },
                        {
                            "name": "Risk_Severity_Category",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "SWITCH(TRUE(), Fact_Risk_Register[Risk_Score] >= 15, \"Critical Red\", Fact_Risk_Register[Risk_Score] >= 8, \"High/Medium Amber\", \"Low Green\")"
                        },
                        {
                            "name": "Risk_RAG_Hex_Code",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "SWITCH(TRUE(), Fact_Risk_Register[Risk_Score] >= 15, \"#DC2626\", Fact_Risk_Register[Risk_Score] >= 8, \"#D97706\", \"#059669\")"
                        },
                        {
                            "name": "Heatmap_Coordinate",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "\"P\" & FORMAT(Fact_Risk_Register[Probability], \"0\") & \"-I\" & FORMAT(Fact_Risk_Register[Impact], \"0\")"
                        }
                    ],
                    "measures": [
                        {
                            "name": "Total_Risk_Count",
                            "expression": "COUNTROWS(Fact_Risk_Register)",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Critical_Risk_Count",
                            "expression": "CALCULATE(COUNTROWS(Fact_Risk_Register), Fact_Risk_Register[Risk_Score] >= 15)",
                            "formatString": "#,##0"
                        },
                        {
                            "name": "Total_Financial_Exposure",
                            "expression": "SUM(Fact_Risk_Register[Financial_Exposure])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Total_Expected_Monetary_Value",
                            "expression": "SUM(Fact_Risk_Register[Expected_Monetary_Value])",
                            "formatString": "$#,##0"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Risk_Register.csv"),[Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Risk_ID", type text}, {"Risk_Title", type text}, {"Category", type text}, {"Probability", Int64.Type}, {"Impact", Int64.Type}, {"Risk_Score", Int64.Type}, {"RAG_Level", type text}, {"Financial_Exposure", Currency.Type}, {"Expected_Monetary_Value", Currency.Type}, {"Mitigation_Strategy", type text}, {"CAM_Owner", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Waterfall_Bridge",
                    "columns": [
                        {"name": "Step_ID", "dataType": "int64", "isKey": True},
                        {"name": "Component_Name", "dataType": "string"},
                        {"name": "Type", "dataType": "string"},
                        {"name": "Incremental_Cost", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Cumulative_Cost", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Pct_Share", "dataType": "double", "formatString": "0.0%"},
                        {"name": "Description", "dataType": "string"},
                        {
                            "name": "Is_Overrun_Step",
                            "dataType": "boolean",
                            "type": "calculated",
                            "expression": "IF(Fact_Waterfall_Bridge[Type] = \"Variance\", TRUE(), FALSE())"
                        },
                        {
                            "name": "Waterfall_Bar_Color",
                            "dataType": "string",
                            "type": "calculated",
                            "expression": "SWITCH(TRUE(), Fact_Waterfall_Bridge[Type] = \"Baseline\", \"#2563EB\", Fact_Waterfall_Bridge[Type] = \"Outturn\", \"#111827\", Fact_Waterfall_Bridge[Step_ID] = 4, \"#7F1D1D\", Fact_Waterfall_Bridge[Step_ID] = 8, \"#B91C1C\", \"#DC2626\")"
                        }
                    ],
                    "measures": [
                        {
                            "name": "Waterfall_Incremental_Cost",
                            "expression": "SUM(Fact_Waterfall_Bridge[Incremental_Cost])",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Waterfall_Cumulative_Cost",
                            "expression": "SUM(Fact_Waterfall_Bridge[Cumulative_Cost])",
                            "formatString": "$#,##0"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Waterfall_Bridge.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Step_ID", Int64.Type}, {"Component_Name", type text}, {"Type", type text}, {"Incremental_Cost", Currency.Type}, {"Cumulative_Cost", Currency.Type}, {"Pct_Share", type number}, {"Description", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Monthly_Burn_Rate",
                    "columns": [
                        {"name": "Period", "dataType": "string", "isKey": True},
                        {"name": "Monthly_PV", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Monthly_EV", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Monthly_AC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Cum_AC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Remaining_BAC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Runway_Status", "dataType": "string"}
                    ],
                    "measures": [
                        {
                            "name": "CFO_Cash_Burn_Rate_Monthly",
                            "expression": "DIVIDE([AC_S_Curve], MAX(Dim_Date[Month_Number]), 0)",
                            "formatString": "$#,##0 / Mo"
                        },
                        {
                            "name": "Avg_Monthly_Cash_Burn_Actual",
                            "expression": "AVERAGEX(FILTER(Fact_Monthly_Burn_Rate, Fact_Monthly_Burn_Rate[Cum_AC] <= 23440000), Fact_Monthly_Burn_Rate[Monthly_AC])",
                            "formatString": "$#,##0 / Mo"
                        },
                        {
                            "name": "Remaining_Baseline_Capital",
                            "expression": "[Total_Budget_at_Completion_BAC] - [AC_S_Curve]",
                            "formatString": "$#,##0"
                        },
                        {
                            "name": "Required_Overrun_Financing",
                            "expression": "[Estimate_at_Completion_EAC] - [Total_Budget_at_Completion_BAC]",
                            "formatString": "$#,##0"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Monthly_Burn_Rate.csv"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Period", type text}, {"Monthly_PV", Currency.Type}, {"Monthly_EV", Currency.Type}, {"Monthly_AC", Currency.Type}, {"Cum_AC", Currency.Type}, {"Remaining_BAC", Currency.Type}, {"Runway_Status", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Financial_Appraisal",
                    "columns": [
                        {"name": "Metric", "dataType": "string", "isKey": True},
                        {"name": "Value", "dataType": "string"},
                        {"name": "Numeric_Value", "dataType": "double"},
                        {"name": "Unit", "dataType": "string"},
                        {"name": "Evaluation", "dataType": "string"}
                    ],
                    "measures": [
                        {"name": "Project_NPV_10Pct_WACC", "expression": "14899563.00", "formatString": "$#,##0"},
                        {"name": "Project_IRR", "expression": "0.1886", "formatString": "0.00%"},
                        {"name": "Project_Simple_Payback_Years", "expression": "4.43", "formatString": "0.00 Years"},
                        {"name": "Project_Total_ROI", "expression": "1.3437", "formatString": "0.00%"},
                        {"name": "Project_Profitability_Index", "expression": "1.42", "formatString": "0.00"},
                        {"name": "Project_Future_Value_Year10", "expression": "130499397.00", "formatString": "$#,##0"}
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Financial_Appraisal.csv"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Metric", type text}, {"Value", type text}, {"Numeric_Value", type number}, {"Unit", type text}, {"Evaluation", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Monte_Carlo",
                    "columns": [
                        {"name": "Percentile", "dataType": "string", "isKey": True},
                        {"name": "Confidence_Level", "dataType": "string"},
                        {"name": "Outturn_Cost_EAC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Cost_Overrun_VAC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Contingency_Reserve", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Duration_Days", "dataType": "double", "formatString": "0.0"},
                        {"name": "Completion_Date", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "Schedule_Delay_Days", "dataType": "double", "formatString": "0.0"}
                    ],
                    "measures": [
                        {"name": "MonteCarlo_P10_EAC", "expression": "32444302.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P50_EAC", "expression": "34060783.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P80_EAC", "expression": "35195026.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P90_EAC", "expression": "35815202.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P95_EAC", "expression": "36272986.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P90_Contingency_Needed", "expression": "401598.00", "formatString": "$#,##0"},
                        {"name": "MonteCarlo_P90_Completion_Date", "expression": "DATE(2027, 3, 14)", "formatString": "yyyy-MM-dd"}
                    ],
                    "partitions": [
                        {
                            "name": "Partition",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = Csv.Document(File.Contents("C:\\\\Users\\\\frank\\\\Desktop\\\\EVM\\\\03_power_bi\\\\Fact_Monte_Carlo.csv"),[Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Percentile", type text}, {"Confidence_Level", type text}, {"Outturn_Cost_EAC", Currency.Type}, {"Cost_Overrun_VAC", Currency.Type}, {"Contingency_Reserve", Currency.Type}, {"Duration_Days", type number}, {"Completion_Date", type date}, {"Schedule_Delay_Days", type number}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "Rel_FactEVM_DimDate",
                    "fromTable": "Fact_EVM_Periodic",
                    "fromColumn": "Date_Key",
                    "toTable": "Dim_Date",
                    "toColumn": "Date_Key"
                },
                {
                    "name": "Rel_FactEVM_DimWBS",
                    "fromTable": "Fact_EVM_Periodic",
                    "fromColumn": "Task_ID",
                    "toTable": "Dim_WBS",
                    "toColumn": "Task_ID"
                },
                {
                    "name": "Rel_FactGantt_DimWBS",
                    "fromTable": "Fact_Gantt_Schedule",
                    "fromColumn": "Task_ID",
                    "toTable": "Dim_WBS",
                    "toColumn": "Task_ID"
                }
            ]
        }
    }

    bim_file = os.path.join(pbi_dir, "Drill_Tower_EVM_Master_Model.bim")
    with open(bim_file, "w", encoding="utf-8") as f:
        json.dump(bim_model, f, indent=2)
    print(f"✅ Generated: 03_power_bi/Drill_Tower_EVM_Master_Model.bim")

    # 2. Generate Power BI Dashboard Specification (JSON)
    pbi_spec = {
        "ReportTitle": "North Sea Oil Platform Drill Tower Construction - Enterprise Power BI Dashboard",
        "Theme": "Edward Tufte Data-Ink Ratio Minimalist Executive Theme",
        "Pages": [
            {
                "PageNumber": 1,
                "PageName": "📈 Executive Runway & Cash Burn",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Avg_Monthly_Cash_Burn_Actual", "Title": "Avg Monthly Cash Burn (M1-M8)", "Target": "$2.93M / Mo"},
                    {"VisualType": "Card", "Metric": "Remaining_Baseline_Capital", "Title": "Remaining Baseline Capital ($BAC - AC)", "Target": "$3.06M Remaining"},
                    {"VisualType": "Card", "Metric": "Budget_Burn_Out_Month", "Title": "Exact Budget Burn Out Month", "Target": "Month 9 (Sep 2026)"},
                    {"VisualType": "Card", "Metric": "Required_Overrun_Financing", "Title": "Required Overrun Financing ($EAC - BAC)", "Target": "+$8,913,604"},
                    {"VisualType": "WaterfallChart", "SourceTable": "Fact_Waterfall_Bridge", "XAxis": "Component_Name", "YAxis": "Incremental_Cost", "Title": "Cost Variance Waterfall Bridge ($BAC → EAC Outturn Breakdown)"},
                    {"VisualType": "DonutChart", "Metric": "PM_Overall_Completion_Pct", "Title": "Physical Progress ($EV / BAC)", "Target": "66.2% Earned ($17.54M)"},
                    {"VisualType": "DonutChart", "SourceTable": "Fact_Waterfall_Bridge", "Title": "Cost Overrun Breakdown (+$8.91M)", "Target": "Delay Overhead 42.8%, Egersund Mast 26.9%"},
                    {"VisualType": "DonutChart", "SourceTable": "Dim_WBS", "Title": "Baseline Budget Allocation (BAC $26.50M)", "Target": "Fab 37.0%, Proc 32.1%, Marine 18.9%, Eng 12.1%"},
                    {"VisualType": "ClusteredColumnChart", "SourceTable": "Fact_Monthly_Burn_Rate", "XAxis": "Period", "YAxis": ["Monthly_PV", "Monthly_EV", "Monthly_AC"], "Title": "Monthly Cash Burn Speed & Budget Depletion (Burn Out) Forecast"},
                    {"VisualType": "ExecutiveBriefingCard", "Title": "1-Page Written Executive Project Status Report (Steering Committee Briefing)"}
                ]
            },
            {
                "PageNumber": 2,
                "PageName": "👔 Project Manager S-Curve & Variances",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Total_Budget_at_Completion_BAC", "Title": "Total Scope BAC", "Target": "$26,500,000"},
                    {"VisualType": "Card", "Metric": "PM_Overall_Completion_Pct", "Title": "Physical Progress", "Target": "66.2%"},
                    {"VisualType": "Card", "Metric": "PM_Schedule_Slippage_Days_Max", "Title": "Critical Path Slippage", "Target": "+31 Days"},
                    {"VisualType": "Card", "Metric": "Cost_Performance_Index_CPI", "Title": "Cost Index (CPI)", "Target": "0.75 (Severe Overrun)"},
                    {"VisualType": "Card", "Metric": "Schedule_Performance_Index_SPI", "Title": "Schedule Index (SPI)", "Target": "0.86 (Delayed)"},
                    {"VisualType": "LineChart", "SourceTable": "Fact_EVM_Periodic", "XAxis": "Date_Key", "YAxis": ["PV_S_Curve", "EV_S_Curve", "AC_S_Curve"], "Title": "Performance Measurement Baseline (S-Curves) & Variance Analysis"},
                    {"VisualType": "Table", "SourceTable": "Fact_EVM_Periodic", "Title": "Executive Variance Explanations & Actionable Audit"},
                    {"VisualType": "Matrix", "SourceTable": "Dim_WBS", "Title": "Executive Project Health & Milestone Summary"}
                ]
            },
            {
                "PageNumber": 3,
                "PageName": "💰 CFO Financials & Outturn Forecast",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Total_Budget_at_Completion_BAC", "Title": "Baseline BAC", "Target": "$26,500,000"},
                    {"VisualType": "Card", "Metric": "AC_S_Curve", "Title": "Actual Cash Spent (AC)", "Target": "$23,440,000"},
                    {"VisualType": "Card", "Metric": "Estimate_at_Completion_EAC", "Title": "Outturn EAC (CPI-Based)", "Target": "$35,413,604"},
                    {"VisualType": "Card", "Metric": "Variance_at_Completion_VAC", "Title": "Variance at Completion", "Target": "-$8,913,604"},
                    {"VisualType": "Card", "Metric": "ETC_Remaining_Liquidity_Needed", "Title": "Liquidity Needed to Finish", "Target": "$11,973,604"},
                    {"VisualType": "Table", "SourceTable": "Dim_WBS", "Columns": ["WBS_Code", "Task_Name", "TBC", "EV", "AC", "CV", "CPI", "EAC", "VAC"], "Title": "CFO Outturn Forecast & Cost Variance Analysis"},
                    {"VisualType": "Table", "SourceTable": "Fact_Financial_Appraisal", "Title": "Commercial Capital Budgeting & Financial Appraisal Ratios"}
                ]
            },
            {
                "PageNumber": 4,
                "PageName": "📊 Project Controller EVM & Earned Schedule",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Cost_Variance_CV", "Title": "Cost Variance (CV)", "Target": "-$5,900,000"},
                    {"VisualType": "Card", "Metric": "Schedule_Variance_SV", "Title": "Schedule Variance (SV)", "Target": "-$2,960,000"},
                    {"VisualType": "Card", "Metric": "Earned_Schedule_Months", "Title": "Earned Schedule (ES)", "Target": "7.40 Months"},
                    {"VisualType": "Card", "Metric": "SPI_Time_Based", "Title": "Time-Based Index SPI(t)", "Target": "0.9250 (-18.2 Days)"},
                    {"VisualType": "Card", "Metric": "TCPI_BAC", "Title": "TCPI (BAC Target)", "Target": "6.07 (Unviable)"},
                    {"VisualType": "Table", "SourceTable": "Dim_WBS", "Title": "Control Account Earned Value & Earned Schedule Deep-Dive"},
                    {"VisualType": "ScatterPlot", "XAxis": "Scatter_X_Schedule_Variance_Pct", "YAxis": "Scatter_Y_Cost_Variance_Pct", "Title": "Concentric Bullseye Risk Scatter Plot Coordinates"}
                ]
            },
            {
                "PageNumber": 5,
                "PageName": "🏗️ Project Planner Gantt & Risk Matrix",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Total_Schedule_Tasks", "Target": "10 Tasks"},
                    {"VisualType": "Card", "Metric": "PM_Critical_Path_Task_Count", "Target": "8 Tasks"},
                    {"VisualType": "Card", "Metric": "Planner_Cascading_Delay_Tasks", "Target": "3 Predecessor Delays"},
                    {"VisualType": "Card", "Metric": "Planner_Avg_Task_Delay_Days", "Target": "+26.5 Days"},
                    {"VisualType": "GanttChart", "SourceTable": "Fact_Gantt_Schedule", "Title": "Offshore EPC Gantt Schedule, Key Milestones (◆) & Predecessor Logic"},
                    {"VisualType": "RiskHeatmapMatrix", "SourceTable": "Fact_Risk_Register", "Title": "EPC Executive Risk Matrix & Quantitative Heatmap (5x5 Grid)"},
                    {"VisualType": "SwimlaneGrid", "SourceTable": "Dim_WBS", "Title": "Vertical Swimlane WBS Breakdown by Category & Discipline"}
                ]
            }
        ]
    }

    spec_file = os.path.join(pbi_dir, "PowerBI_Dashboard_Specification.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(pbi_spec, f, indent=2)
    print(f"✅ Generated: 03_power_bi/PowerBI_Dashboard_Specification.json")

    # 3. Create Power BI Project Definition Structure (.pbip)
    pbi_dataset_dir = os.path.join(pbi_dir, "Drill_Tower_EVM_PowerBI.Dataset")
    os.makedirs(pbi_dataset_dir, exist_ok=True)

    pbism_content = {
        "version": "1.0",
        "settings": {}
    }
    with open(os.path.join(pbi_dataset_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_content, f, indent=2)

    with open(os.path.join(pbi_dataset_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(bim_model, f, indent=2)

    print(f"✅ Generated: 03_power_bi/Drill_Tower_EVM_PowerBI.Dataset/ (definition.pbism & model.bim)")

    pbip_dir = os.path.join(pbi_dir, "Drill_Tower_EVM_PowerBI.Report")
    os.makedirs(pbip_dir, exist_ok=True)
    
    definition_json = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {"path": "../Drill_Tower_EVM_PowerBI.Dataset"}
        }
    }
    with open(os.path.join(pbip_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(definition_json, f, indent=2)

    report_json = {
        "config": json.dumps({
            "version": "5.50",
            "themeCollection": {},
            "activeSectionName": "Section1",
            "defaultDrillFilterOtherVisuals": True
        }),
        "layoutOptimization": 0,
        "resourcePackages": [],
        "sections": [
            {
                "name": "Section1",
                "displayName": "📈 Executive Runway & Cash Burn",
                "filters": "[]",
                "height": 720.0,
                "width": 1280.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 20.0, "z": 0.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_burn", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Monthly_Burn_Rate.Avg_Monthly_Cash_Burn_Actual"}]}}})
                    },
                    {
                        "x": 250.0, "y": 20.0, "z": 1.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_cap", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Monthly_Burn_Rate.Remaining_Baseline_Capital"}]}}})
                    },
                    {
                        "x": 480.0, "y": 20.0, "z": 2.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_burnout", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Monthly_Burn_Rate.Budget_Burn_Out_Month"}]}}})
                    },
                    {
                        "x": 710.0, "y": 20.0, "z": 3.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_overrun", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Monthly_Burn_Rate.Required_Overrun_Financing"}]}}})
                    },
                    {
                        "x": 20.0, "y": 140.0, "z": 4.0, "height": 260.0, "width": 600.0,
                        "config": json.dumps({"name": "waterfall_visual", "singleVisual": {"visualType": "waterfallChart", "projections": {"Category": [{"queryRef": "Fact_Waterfall_Bridge.Component_Name"}], "Y": [{"queryRef": "Fact_Waterfall_Bridge.Incremental_Cost"}]}}})
                    },
                    {
                        "x": 640.0, "y": 140.0, "z": 5.0, "height": 260.0, "width": 600.0,
                        "config": json.dumps({"name": "burn_chart", "singleVisual": {"visualType": "clusteredColumnChart", "projections": {"Category": [{"queryRef": "Fact_Monthly_Burn_Rate.Period"}], "Y": [{"queryRef": "Fact_Monthly_Burn_Rate.Monthly_PV"}, {"queryRef": "Fact_Monthly_Burn_Rate.Monthly_EV"}, {"queryRef": "Fact_Monthly_Burn_Rate.Monthly_AC"}]}}})
                    }
                ]
            },
            {
                "name": "Section2",
                "displayName": "👔 Project Manager S-Curve & Variances",
                "filters": "[]",
                "height": 720.0,
                "width": 1280.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 20.0, "z": 0.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_bac", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Dim_WBS.Total_Budget_at_Completion_BAC"}]}}})
                    },
                    {
                        "x": 250.0, "y": 20.0, "z": 1.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_pct", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.PM_Overall_Completion_Pct"}]}}})
                    },
                    {
                        "x": 480.0, "y": 20.0, "z": 2.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_cpi", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Cost_Performance_Index_CPI"}]}}})
                    },
                    {
                        "x": 710.0, "y": 20.0, "z": 3.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_spi", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Schedule_Performance_Index_SPI"}]}}})
                    },
                    {
                        "x": 20.0, "y": 140.0, "z": 4.0, "height": 320.0, "width": 1220.0,
                        "config": json.dumps({"name": "scurve_line_chart", "singleVisual": {"visualType": "lineChart", "projections": {"Category": [{"queryRef": "Dim_Date.Date_Key"}], "Y": [{"queryRef": "Fact_EVM_Periodic.PV_S_Curve"}, {"queryRef": "Fact_EVM_Periodic.EV_S_Curve"}, {"queryRef": "Fact_EVM_Periodic.AC_S_Curve"}]}}})
                    }
                ]
            },
            {
                "name": "Section3",
                "displayName": "💰 CFO Financials & Outturn Forecast",
                "filters": "[]",
                "height": 720.0,
                "width": 1280.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 20.0, "z": 0.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_eac", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Estimate_at_Completion_EAC"}]}}})
                    },
                    {
                        "x": 300.0, "y": 20.0, "z": 1.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_vac", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Variance_at_Completion_VAC"}]}}})
                    },
                    {
                        "x": 580.0, "y": 20.0, "z": 2.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_etc", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.ETC_Remaining_Liquidity_Needed"}]}}})
                    },
                    {
                        "x": 20.0, "y": 140.0, "z": 3.0, "height": 320.0, "width": 1220.0,
                        "config": json.dumps({"name": "cfo_table", "singleVisual": {"visualType": "table", "projections": {"Values": [{"queryRef": "Dim_WBS.WBS_Code"}, {"queryRef": "Dim_WBS.Task_Name"}, {"queryRef": "Dim_WBS.TBC"}]}}})
                    }
                ]
            },
            {
                "name": "Section4",
                "displayName": "📊 Project Controller EVM & Earned Schedule",
                "filters": "[]",
                "height": 720.0,
                "width": 1280.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 20.0, "z": 0.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_cv", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Cost_Variance_CV"}]}}})
                    },
                    {
                        "x": 250.0, "y": 20.0, "z": 1.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_sv", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Schedule_Variance_SV"}]}}})
                    },
                    {
                        "x": 480.0, "y": 20.0, "z": 2.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_es", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.Earned_Schedule_Months"}]}}})
                    },
                    {
                        "x": 710.0, "y": 20.0, "z": 3.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_spit", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.SPI_Time_Based"}]}}})
                    },
                    {
                        "x": 940.0, "y": 20.0, "z": 4.0, "height": 100.0, "width": 220.0,
                        "config": json.dumps({"name": "card_tcpi", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_EVM_Periodic.TCPI_BAC"}]}}})
                    }
                ]
            },
            {
                "name": "Section5",
                "displayName": "🏗️ Project Planner Gantt & Risk Matrix",
                "filters": "[]",
                "height": 720.0,
                "width": 1280.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 20.0, "z": 0.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_tasks", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Gantt_Schedule.PM_Critical_Path_Task_Count"}]}}})
                    },
                    {
                        "x": 300.0, "y": 20.0, "z": 1.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_delays", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Gantt_Schedule.Planner_Cascading_Delay_Tasks"}]}}})
                    },
                    {
                        "x": 580.0, "y": 20.0, "z": 2.0, "height": 100.0, "width": 260.0,
                        "config": json.dumps({"name": "card_avgdelay", "singleVisual": {"visualType": "card", "projections": {"Values": [{"queryRef": "Fact_Gantt_Schedule.Planner_Avg_Task_Delay_Days"}]}}})
                    },
                    {
                        "x": 20.0, "y": 140.0, "z": 3.0, "height": 320.0, "width": 1220.0,
                        "config": json.dumps({"name": "gantt_table", "singleVisual": {"visualType": "table", "projections": {"Values": [{"queryRef": "Fact_Gantt_Schedule.Task_ID"}, {"queryRef": "Fact_Gantt_Schedule.Task_Name"}, {"queryRef": "Fact_Gantt_Schedule.Baseline_Start"}, {"queryRef": "Fact_Gantt_Schedule.Baseline_End"}, {"queryRef": "Fact_Gantt_Schedule.Actual_Start"}, {"queryRef": "Fact_Gantt_Schedule.Actual_End"}, {"queryRef": "Fact_Gantt_Schedule.Critical_Path_Flag"}]}}})
                    }
                ]
            }
        ]
    }
    with open(os.path.join(pbip_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    pbip_root = os.path.join(pbi_dir, "Drill_Tower_EVM_PowerBI.pbip")
    pbip_content = {
        "version": "1.0",
        "artifacts": [
            {"report": {"path": "Drill_Tower_EVM_PowerBI.Report"}}
        ]
    }
    with open(pbip_root, "w", encoding="utf-8") as f:
        json.dump(pbip_content, f, indent=2)
        
    print(f"✅ Generated: 03_power_bi/Drill_Tower_EVM_PowerBI.pbip (Power BI Project Folder)")

if __name__ == "__main__":
    build_powerbi_solution()
