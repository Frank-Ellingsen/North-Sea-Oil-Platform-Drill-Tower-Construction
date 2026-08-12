import os
import shutil

base_dir = "C:/Users/frank/Desktop/EVM"

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
        "PERT-activity.xlsx"
    ],
    "02_databases": [
        "evm_analytics.duckdb",
        "evm_transactional.db"
    ],
    "03_power_bi": [
        "Fact_EVM_Periodic.csv",
        "Dim_WBS.csv",
        "Dim_Date.csv",
        "EVM_DAX_Measures.dax"
    ],
    "04_dashboard": [
        "index.html"
    ],
    "05_scripts": [
        "create_excel_master.py",
        "etl_pipeline.py",
        "build_sqlite_db.py",
        "draw_erd.py",
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
        "Project_Management_and_Earned_Value_Management_Handbook.pdf"
    ]
}

print("=" * 80)
print("Structuring Workspace Folders and Subfolders...")
print("=" * 80)

# Create folders & move files
for folder, files in folders.items():
    target_dir = os.path.join(base_dir, folder)
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        src = os.path.join(base_dir, f)
        dst = os.path.join(target_dir, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f" Moved {f} -> {folder}/")

print("\nWorkspace folder restructuring complete.")
