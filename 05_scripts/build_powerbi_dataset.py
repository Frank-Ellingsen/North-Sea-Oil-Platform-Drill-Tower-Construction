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
    print("Building Power BI Solution & Star Schema Model for Drill Tower Construction...")
    print("=" * 80)

    # 1. Generate Power BI Tabular Model (BIM / TOM Schema)
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
                        {"name": "WBS_Code", "dataType": "string", "isKey": True},
                        {"name": "WBS_Element_Name", "dataType": "string"},
                        {"name": "CAM_Owner", "dataType": "string"},
                        {"name": "Level", "dataType": "int64"},
                        {"name": "Parent_WBS", "dataType": "string"},
                        {"name": "TBC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Control_Account", "dataType": "string"}
                    ]
                },
                {
                    "name": "Dim_Date",
                    "columns": [
                        {"name": "Date_Key", "dataType": "dateTime", "formatString": "yyyy-MM-dd", "isKey": True},
                        {"name": "Month_Name", "dataType": "string"},
                        {"name": "Month_Number", "dataType": "int64"},
                        {"name": "Year", "dataType": "int64"}
                    ]
                },
                {
                    "name": "Fact_EVM_Periodic",
                    "columns": [
                        {"name": "Fact_ID", "dataType": "string"},
                        {"name": "Date_Key", "dataType": "dateTime", "formatString": "yyyy-MM-dd"},
                        {"name": "WBS_Code", "dataType": "string"},
                        {"name": "PV_Incremental", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "EV_Incremental_Calculated", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "AC_Incremental", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Physical_Pct_Complete", "dataType": "double", "formatString": "0.0%"},
                        {"name": "PV_Cumulative", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "EV_Cumulative", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "AC_Cumulative", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "CV_Cumulative", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "SV_Cumulative", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "CPI_Cumulative", "dataType": "double", "formatString": "0.000"}
                    ]
                },
                {
                    "name": "Fact_Monthly_Burn_Rate",
                    "columns": [
                        {"name": "Month_Num", "dataType": "int64", "isKey": True},
                        {"name": "Month_Name", "dataType": "string"},
                        {"name": "Monthly_PV", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Monthly_EV", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Monthly_AC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Cum_AC", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Burn_Out_Flag", "dataType": "string"}
                    ]
                },
                {
                    "name": "Fact_Waterfall_Bridge",
                    "columns": [
                        {"name": "Step_Num", "dataType": "int64", "isKey": True},
                        {"name": "WBS_Element", "dataType": "string"},
                        {"name": "Step_Variance_Amount", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Cum_Waterfall_Total", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Category", "dataType": "string"},
                        {"name": "Driver_Explanation", "dataType": "string"}
                    ]
                },
                {
                    "name": "Fact_Gantt_Schedule",
                    "columns": [
                        {"name": "Task_ID", "dataType": "string", "isKey": True},
                        {"name": "WBS_Code", "dataType": "string"},
                        {"name": "Task_Name", "dataType": "string"},
                        {"name": "Predecessor_ID", "dataType": "string"},
                        {"name": "Dependency_Type", "dataType": "string"},
                        {"name": "Total_Float_Days", "dataType": "int64"},
                        {"name": "Pct_Complete", "dataType": "double", "formatString": "0.0%"},
                        {"name": "Baseline_Start", "dataType": "dateTime"},
                        {"name": "Baseline_Finish", "dataType": "dateTime"},
                        {"name": "Actual_Forecast_Start", "dataType": "dateTime"},
                        {"name": "Actual_Forecast_Finish", "dataType": "dateTime"},
                        {"name": "Is_Critical_Path", "dataType": "boolean"}
                    ]
                },
                {
                    "name": "Fact_Risk_Register",
                    "columns": [
                        {"name": "Risk_ID", "dataType": "string", "isKey": True},
                        {"name": "Risk_Description", "dataType": "string"},
                        {"name": "WBS_Code", "dataType": "string"},
                        {"name": "CAM_Owner", "dataType": "string"},
                        {"name": "Probability_Score", "dataType": "int64"},
                        {"name": "Impact_Score", "dataType": "int64"},
                        {"name": "Risk_Score", "dataType": "int64"},
                        {"name": "Financial_Exposure", "dataType": "decimal", "formatString": "$#,##0"},
                        {"name": "Mitigation_Strategy", "dataType": "string"}
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
                    "fromColumn": "WBS_Code",
                    "toTable": "Dim_WBS",
                    "toColumn": "WBS_Code"
                },
                {
                    "name": "Rel_FactGantt_DimWBS",
                    "fromTable": "Fact_Gantt_Schedule",
                    "fromColumn": "WBS_Code",
                    "toTable": "Dim_WBS",
                    "toColumn": "WBS_Code"
                },
                {
                    "name": "Rel_FactRisk_DimWBS",
                    "fromTable": "Fact_Risk_Register",
                    "fromColumn": "WBS_Code",
                    "toTable": "Dim_WBS",
                    "toColumn": "WBS_Code"
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
        "Theme": "Tufte Minimalist Dark-Slate Controller Theme",
        "Pages": [
            {
                "PageNumber": 1,
                "PageName": "📈 Executive Runway & Cash Burn",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Total_Budget_at_Completion_BAC", "Title": "Baseline BAC Target", "Target": "$26.50M"},
                    {"VisualType": "Card", "Metric": "Cumulative_EV", "Title": "Earned Value", "Target": "$17.54M"},
                    {"VisualType": "Card", "Metric": "Cumulative_AC", "Title": "Actual Spend", "Target": "$23.44M"},
                    {"VisualType": "Card", "Metric": "Cost_Variance_CV", "Title": "Cost Overrun", "Target": "-$5.90M"},
                    {"VisualType": "WaterfallChart", "SourceTable": "Fact_Waterfall_Bridge", "XAxis": "WBS_Element", "YAxis": "Step_Variance_Amount", "Title": "Cost Variance Waterfall Bridge ($BAC to EAC)"},
                    {"VisualType": "ClusteredColumnChart", "SourceTable": "Fact_Monthly_Burn_Rate", "XAxis": "Month_Name", "YAxis": ["Monthly_PV", "Monthly_EV", "Monthly_AC"], "Title": "Monthly Cash Burn Speed & Month 9 Burn Out"}
                ]
            },
            {
                "PageNumber": 2,
                "PageName": "👔 Project Manager S-Curve & Variances",
                "Visuals": [
                    {"VisualType": "LineChart", "SourceTable": "Fact_EVM_Periodic", "XAxis": "Date_Key", "YAxis": ["PV_Cumulative", "EV_Cumulative", "AC_Cumulative"], "Title": "Performance Measurement Baseline (PMB S-Curve)"},
                    {"VisualType": "Matrix", "SourceTable": "Dim_WBS", "Columns": ["WBS_Code", "WBS_Element_Name", "CAM_Owner", "TBC"], "Title": "Executive Project Health & Milestone Summary"}
                ]
            },
            {
                "PageNumber": 3,
                "PageName": "💰 CFO Financials & Outturn Forecast",
                "Visuals": [
                    {"VisualType": "Card", "Metric": "Estimate_at_Completion_EAC", "Title": "Outturn EAC Forecast", "Target": "$35.41M"},
                    {"VisualType": "Card", "Metric": "Variance_at_Completion_VAC", "Title": "Outturn Deficit", "Target": "-$8.91M"},
                    {"VisualType": "Table", "SourceTable": "Dim_WBS", "Columns": ["WBS_Code", "Control_Account", "TBC", "EV", "AC", "CV", "CPI", "EAC", "VAC"], "Title": "CFO Control Account Outturn Forecast Table"}
                ]
            },
            {
                "PageNumber": 4,
                "PageName": "📊 Project Controller EVM & Earned Schedule",
                "Visuals": [
                    {"VisualType": "Gauge", "Metric": "Cost_Performance_Index_CPI", "Target": 1.00, "Current": 0.748, "Status": "Critical Red"},
                    {"VisualType": "Gauge", "Metric": "Schedule_Performance_Index_SPI", "Target": 1.00, "Current": 0.856, "Status": "Amber Delayed"},
                    {"VisualType": "Table", "SourceTable": "Fact_EVM_Periodic", "Columns": ["WBS_Code", "PV_Cumulative", "EV_Cumulative", "AC_Cumulative", "CV_Cumulative", "CPI_Cumulative"], "Title": "Earned Schedule & TCPI Efficiency Deep-Dive"}
                ]
            },
            {
                "PageNumber": 5,
                "PageName": "🏗️ Project Planner Gantt & Risk Matrix",
                "Visuals": [
                    {"VisualType": "GanttChart", "SourceTable": "Fact_Gantt_Schedule", "TaskField": "Task_Name", "StartField": "Actual_Forecast_Start", "FinishField": "Actual_Forecast_Finish", "CriticalField": "Is_Critical_Path"},
                    {"VisualType": "MatrixHeatmap", "SourceTable": "Fact_Risk_Register", "Row": "Probability_Score", "Column": "Impact_Score", "Values": "Risk_ID", "Title": "5x5 EPC Executive Risk Probability vs Impact Heatmap"}
                ]
            }
        ]
    }

    spec_file = os.path.join(pbi_dir, "PowerBI_Dashboard_Specification.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(pbi_spec, f, indent=2)
    print(f"✅ Generated: 03_power_bi/PowerBI_Dashboard_Specification.json")

    # 3. Create Power BI Project Definition Structure (.pbip)
    # 3a. Create Dataset Folder (.Dataset) with definition.pbism & model.bim
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

    # 3b. Create Report Folder (.Report) with definition.pbir & report.json
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
        "config": "{}",
        "layoutOptimization": 0
    }
    with open(os.path.join(pbip_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    # 3c. Create Root .pbip File
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
