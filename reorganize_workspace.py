import os
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))

folders = {
    "01_raw_data": [
        "01_PV_Baseline.csv",
        "02_EV_Progress.csv",
        "03_AC_Actuals.csv",
        "04_Dim_WBS.csv",
        "EVM_Master_Data.xlsx",
        "Activity-Template.xlsx",
        "BCR-Activity-template.xlsx",
        "DCF-Activity-template.xlsx",
        "EVM-Assessing-Performance-Worksheet-with-Answers.xlsx",
        "Earned-Value-Management-EVM-and-cost-management_Worksheet.xlsx",
        "FV-Activity-exemplar.xlsx",
        "Forecasting-formulas_Worksheet-with-answers.xlsx",
        "NPV-Activity-exemplar.xlsx",
        "PERT-activity.xlsx",
        "Drill_Tower_EVM_Master_Report.xlsx"
    ],
    "02_databases": [
        "evm_analytics.duckdb",
        "evm_transactional.db"
    ],
    "03_power_bi": [
        "Fact_EVM_Periodic.csv",
        "Dim_WBS.csv",
        "Dim_Date.csv",
        "Fact_Monthly_Burn_Rate.csv",
        "Fact_Waterfall_Bridge.csv",
        "Fact_Gantt_Schedule.csv",
        "Fact_Risk_Register.csv",
        "Fact_Financial_Appraisal.csv",
        "Fact_Monte_Carlo.csv",
        "EVM_DAX_Measures.dax",
        "PowerBI_DAX_Master.dax",
        "PowerQuery_Import_Script.m",
        "Drill_Tower_EVM_Master_Model.bim",
        "PowerBI_Dashboard_Specification.json",
        "Drill_Tower_EVM_PowerBI.pbip"
    ],
    "04_dashboard": [
        "drill_tower_web_report.html"
    ],
    "05_scripts": [
        "build_powerbi_dataset.py",
        "build_sqlite_db.py",
        "calculate_financial_ratios.py",
        "create_drill_tower_excel.py",
        "create_excel_master.py",
        "draw_datamodel_diagrams.py",
        "draw_erd.py",
        "etl_pipeline.py",
        "generate_drill_tower_data.py",
        "generate_excel_reports.py",
        "generate_pdf_report.py",
        "generate_pdf_reports.py",
        "generate_pm_handbook_pdf.py",
        "generate_powerpoint_presentation.py",
        "generate_pptx_reports.py",
        "monte_carlo_simulation.py",
        "test_and_revise_powerbi.py",
        "update_excel_and_powerbi_full.py",
        "verify_model.py"
    ],
    "06_docs": [
        "antigravity.md",
        "erd_diagram.png",
        "EVM.md",
        "contingencies.md",
        "fomulas.md",
        "forcasting_evm.md",
        "pmp.md",
        "s-curve.md",
        "s-curve.png",
        "scenacio1.md",
        "schedule.md",
        "study.md",
        "study_assement.md",
        "Earned_Value_Management_Cheat_Sheet.pdf",
        "Financial-Analysis-Report-outline.docx",
        "Project_Management_and_Earned_Value_Management_Handbook.pdf",
        "Executive_1Page_Steering_Status_Briefing.pdf",
        "Drill_Tower_Full_EVM_Dashboard_Report.pdf",
        "North_Sea_Drill_Tower_EVM_Comprehensive_Report.pdf",
        "Drill_Tower_Executive_Steering_Presentation.pptx",
        "Drill_Tower_EVM_Master_Report.xlsx"
    ]
}

print("=" * 80)
print("Verifying & Structuring Workspace Folders...")
print("=" * 80)

for folder, files in folders.items():
    target_dir = os.path.join(base_dir, folder)
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(target_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f" Moved {f} -> {folder}/")

print("\nWorkspace folder structure verified and organized successfully.")
