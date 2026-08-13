import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import shutil

BASE_DIR = "C:/Users/frank/Desktop/EVM"
DOCS_DIR = os.path.join(BASE_DIR, "06_docs")
BRAIN_DIR = "C:/Users/frank/.gemini/antigravity-cli/brain/90e19606-c7c0-46ec-b802-c9a5b2f59896"

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

def draw_table_card(ax, x, y, width, title, fields, header_color='#1F4E79'):
    row_h = 24
    head_h = 32
    tot_h = head_h + len(fields) * row_h
    
    # Outer Card
    box = patches.FancyBboxPatch((x, y - tot_h), width, tot_h,
                                  boxstyle="round,pad=0,rounding_size=5",
                                  facecolor='#FFFFFF', edgecolor='#D1D5DB', linewidth=1.2)
    ax.add_patch(box)
    
    # Header Bar
    head_box = patches.FancyBboxPatch((x, y - head_h), width, head_h,
                                       boxstyle="round,pad=0,rounding_size=5",
                                       facecolor=header_color, edgecolor=header_color, linewidth=0)
    ax.add_patch(head_box)
    
    # Header Title
    ax.text(x + width/2, y - head_h/2, title, fontsize=10.5, fontweight='bold', color='#FFFFFF', ha='center', va='center')
    
    # Fields
    curr_y = y - head_h - row_h/2
    for item in fields:
        if len(item) == 3:
            key_type, name, data_type = item
        else:
            key_type, name = item[0], item[1]
            data_type = ""

        if key_type == 'PK':
            ax.text(x + 10, curr_y, 'PK', fontsize=8, fontweight='bold', color='#D97706', ha='left', va='center')
        elif key_type == 'FK':
            ax.text(x + 10, curr_y, 'FK', fontsize=8, fontweight='bold', color='#2563EB', ha='left', va='center')
        elif key_type == 'M':
            ax.text(x + 10, curr_y, 'fx', fontsize=8, fontweight='bold', color='#059669', ha='left', va='center')
        else:
            ax.text(x + 10, curr_y, '  ', fontsize=8, ha='left', va='center')
            
        ax.text(x + 36, curr_y, name, fontsize=9, fontweight='bold' if key_type else 'normal', color='#1F2937', ha='left', va='center')
        if data_type:
            ax.text(x + width - 10, curr_y, data_type, fontsize=8, fontfamily='monospace', color='#6B7280', ha='right', va='center')
            
        ax.plot([x, x + width], [curr_y - row_h/2, curr_y - row_h/2], color='#F3F4F6', linewidth=0.8)
        curr_y -= row_h
    return tot_h

def generate_full_erd():
    fig, ax = plt.subplots(figsize=(20, 12), dpi=300)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#F8F9FA')
    ax.axis('off')
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1200)

    # Title Banner
    ax.text(1000, 1160, "Offshore EPC Drill Tower Construction — Full Relational Database ERD", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#1F2937')
    ax.text(1000, 1130, "Comprehensive Entity-Relationship Model (10 Data Tables with Primary/Foreign Keys & Governance)", 
            fontsize=11, color='#6B7280', ha='center', va='center')

    # 1. Dim_Date
    draw_table_card(ax, 50, 1100, 320, 'Dim_Date (Calendar Dim)', [
        ('PK', 'Date_Key', 'TEXT'),
        ('', 'Year', 'INTEGER'),
        ('', 'Month_Number', 'INTEGER'),
        ('', 'Month_Name', 'TEXT'),
        ('', 'Year_Month', 'TEXT'),
        ('', 'Quarter', 'TEXT')
    ], '#2563EB')

    # 2. Fact_EVM_Periodic
    draw_table_card(ax, 450, 1100, 380, 'Fact_EVM_Periodic (Core EVM Fact)', [
        ('PK', 'Fact_ID', 'INTEGER AUTO'),
        ('FK', 'Task_ID', 'TEXT'),
        ('FK', 'Date_Key', 'TEXT'),
        ('', 'Total_Budget_Cost', 'REAL'),
        ('', 'PV_Incremental', 'REAL'),
        ('', 'EV_Physical_Percent', 'REAL'),
        ('', 'EV_Incremental_Calculated', 'REAL'),
        ('', 'AC_Incremental', 'REAL')
    ], '#1F4E79')

    # 3. Dim_WBS
    draw_table_card(ax, 910, 1100, 330, 'Dim_WBS (WBS Structure Dim)', [
        ('PK', 'Task_ID', 'TEXT'),
        ('', 'WBS_Code', 'TEXT'),
        ('', 'WBS_Level_1', 'TEXT'),
        ('', 'WBS_Level_2', 'TEXT'),
        ('', 'Task_Name', 'TEXT'),
        ('', 'CAM', 'TEXT'),
        ('', 'TBC', 'REAL')
    ], '#059669')

    # 4. Fact_Gantt_Schedule
    draw_table_card(ax, 1320, 1100, 420, 'Fact_Gantt_Schedule (Gantt Schedule)', [
        ('PK', 'Task_ID', 'TEXT'),
        ('', 'Task_Name', 'TEXT'),
        ('', 'WBS_Code', 'TEXT'),
        ('', 'CAM', 'TEXT'),
        ('', 'Baseline_Start', 'TEXT'),
        ('', 'Baseline_End', 'TEXT'),
        ('', 'Actual_Start', 'TEXT'),
        ('', 'Actual_End', 'TEXT'),
        ('FK', 'Predecessor_Task_ID', 'TEXT'),
        ('', 'Dependency_Type', 'TEXT'),
        ('', 'Lag_Days', 'INTEGER'),
        ('', 'Percent_Complete', 'REAL'),
        ('', 'Critical_Path_Flag', 'TEXT')
    ], '#7C3AED')

    # 5. Fact_Milestones
    draw_table_card(ax, 50, 750, 340, 'Fact_Milestones (Key Gates)', [
        ('PK', 'Milestone_ID', 'TEXT'),
        ('', 'Milestone_Name', 'TEXT'),
        ('', 'Target_Date', 'TEXT'),
        ('', 'Baseline_Date', 'TEXT'),
        ('', 'Status', 'TEXT'),
        ('', 'RAG', 'TEXT'),
        ('FK', 'WBS_Code', 'TEXT')
    ], '#D97706')

    # 6. Fact_Risk_Register
    draw_table_card(ax, 430, 750, 420, 'Fact_Risk_Register (5x5 Heatmap)', [
        ('PK', 'Risk_ID', 'TEXT'),
        ('', 'Risk_Title', 'TEXT'),
        ('', 'Category', 'TEXT'),
        ('', 'Probability', 'INTEGER'),
        ('', 'Impact', 'INTEGER'),
        ('', 'Risk_Score', 'INTEGER'),
        ('', 'RAG_Level', 'TEXT'),
        ('', 'Financial_Exposure', 'REAL'),
        ('', 'Expected_Monetary_Value', 'REAL'),
        ('', 'Mitigation_Strategy', 'TEXT'),
        ('', 'CAM_Owner', 'TEXT')
    ], '#DC2626')

    # 7. Fact_Waterfall_Bridge
    draw_table_card(ax, 890, 750, 370, 'Fact_Waterfall_Bridge ($BAC → EAC)', [
        ('PK', 'Step_ID', 'INTEGER'),
        ('', 'Component_Name', 'TEXT'),
        ('', 'Type', 'TEXT'),
        ('', 'Incremental_Cost', 'REAL'),
        ('', 'Cumulative_Cost', 'REAL'),
        ('', 'Pct_Share', 'REAL'),
        ('', 'Description', 'TEXT')
    ], '#4B5563')

    # 8. Fact_Monthly_Burn_Rate
    draw_table_card(ax, 1300, 600, 380, 'Fact_Monthly_Burn_Rate (Cash Burn)', [
        ('PK', 'Period', 'TEXT'),
        ('', 'Monthly_PV', 'REAL'),
        ('', 'Monthly_EV', 'REAL'),
        ('', 'Monthly_AC', 'REAL'),
        ('', 'Cum_AC', 'REAL'),
        ('', 'Remaining_BAC', 'REAL'),
        ('', 'Runway_Status', 'TEXT')
    ], '#7F1D1D')

    # 9. Fact_Financial_Appraisal
    draw_table_card(ax, 50, 380, 360, 'Fact_Financial_Appraisal (ROI/NPV)', [
        ('PK', 'Metric', 'TEXT'),
        ('', 'Value', 'TEXT'),
        ('', 'Numeric_Value', 'REAL'),
        ('', 'Unit', 'TEXT'),
        ('', 'Evaluation', 'TEXT')
    ], '#059669')

    # 10. Fact_Monte_Carlo
    draw_table_card(ax, 450, 380, 400, 'Fact_Monte_Carlo (P90 Risk Runs)', [
        ('PK', 'Percentile', 'TEXT'),
        ('', 'Confidence_Level', 'TEXT'),
        ('', 'Outturn_Cost_EAC', 'REAL'),
        ('', 'Cost_Overrun_VAC', 'REAL'),
        ('', 'Contingency_Reserve', 'REAL'),
        ('', 'Duration_Days', 'REAL'),
        ('', 'Completion_Date', 'TEXT'),
        ('', 'Schedule_Delay_Days', 'REAL')
    ], '#2563EB')

    # Relationships Lines
    # Dim_Date -> Fact_EVM_Periodic
    ax.annotate('', xy=(450, 1000), xytext=(370, 1000), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#2563EB", lw=2.2))
    ax.text(380, 1010, "1", fontsize=11, fontweight='bold', color="#2563EB")
    ax.text(435, 1010, "N", fontsize=11, fontweight='bold', color="#2563EB")

    # Dim_WBS -> Fact_EVM_Periodic
    ax.annotate('', xy=(830, 1000), xytext=(910, 1000), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#059669", lw=2.2))
    ax.text(900, 1010, "1", fontsize=11, fontweight='bold', color="#059669")
    ax.text(845, 1010, "N", fontsize=11, fontweight='bold', color="#059669")

    # Dim_WBS -> Fact_Gantt_Schedule
    ax.annotate('', xy=(1320, 1000), xytext=(1240, 1000), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#059669", lw=2.2))
    ax.text(1250, 1010, "1", fontsize=11, fontweight='bold', color="#059669")
    ax.text(1305, 1010, "1", fontsize=11, fontweight='bold', color="#059669")

    # Legend & Governance Box
    note_box = patches.FancyBboxPatch((890, 100), 790, 240,
                                      boxstyle="round,pad=0,rounding_size=6",
                                      facecolor='#FFFFFF', edgecolor='#D1D5DB', linewidth=1.2)
    ax.add_patch(note_box)
    ax.text(1285, 315, "Database Architecture & Governance Specification", fontsize=12, fontweight='bold', color='#1F2937', ha='center')
    ax.text(1285, 285, "• Transactional Engine: SQLite 3 (PRAGMA foreign_keys = ON) for single-write ACID operations.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(1285, 260, "• Analytical Engine: DuckDB Star Schema with OLAP columnar indexing for instantaneous aggregation.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(1285, 235, "• Business Intelligence: Power BI Desktop VertiPaq tabular model with 62 DAX measures & calculated columns.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(1285, 210, "• EVM Baseline: Total Budget at Completion (BAC = $26.50M) mathematically checked across all fact tables.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(1285, 185, "• Outturn Risk: Monte Carlo 10,000-run simulation outturn (P50 = $34.06M / P90 = $35.82M + $401.6k Reserve).", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(1285, 155, "Files: 02_databases/evm_analytics.duckdb | 02_databases/evm_transactional.db | 03_power_bi/", fontsize=9, fontfamily='monospace', color='#2563EB', ha='center')

    plt.tight_layout()
    erd_path = os.path.join(DOCS_DIR, "full_erd_diagram.png")
    fig.savefig(erd_path, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close(fig)
    print("[PASS] Rendered:", erd_path)
    shutil.copy(erd_path, os.path.join(BRAIN_DIR, "full_erd_diagram.png"))

def generate_powerbi_star_schema():
    fig, ax = plt.subplots(figsize=(20, 12), dpi=300)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#F8F9FA')
    ax.axis('off')
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1200)

    ax.text(1000, 1160, "Power BI Desktop Relational Star Schema Data Model Diagram", 
            fontsize=18, fontweight='bold', ha='center', va='center', color='#1F2937')
    ax.text(1000, 1130, "Optimized VertiPaq In-Memory Data Model (Single Unidirectional 1 : * Filtering)", 
            fontsize=11, color='#6B7280', ha='center', va='center')

    # Dim_Date (Top Left)
    draw_table_card(ax, 100, 1100, 360, 'Dim_Date (Calendar Dimension - 1)', [
        ('PK', 'Date_Key', 'Date'),
        ('', 'Year', 'Int64'),
        ('', 'Month_Number', 'Int64'),
        ('', 'Month_Name', 'Text'),
        ('', 'Year_Month', 'Text'),
        ('', 'Quarter', 'Text')
    ], '#2563EB')

    # Dim_WBS (Top Right)
    draw_table_card(ax, 1540, 1100, 360, 'Dim_WBS (Structure Dimension - 1)', [
        ('PK', 'Task_ID', 'Text'),
        ('', 'WBS_Code', 'Text'),
        ('', 'WBS_Level_1', 'Text'),
        ('', 'WBS_Level_2', 'Text'),
        ('', 'Task_Name', 'Text'),
        ('', 'CAM', 'Text'),
        ('', 'TBC', 'Currency'),
        ('', 'WBS_Category', 'Calculated Column')
    ], '#059669')

    # Fact_EVM_Periodic (Center Hub Left)
    draw_table_card(ax, 200, 750, 420, 'Fact_EVM_Periodic (Core Fact Table - *)', [
        ('FK', 'Task_ID (Relationship Key)', 'Text'),
        ('FK', 'Date_Key (Relationship Key)', 'Date'),
        ('', 'Total_Budget_Cost', 'Currency'),
        ('', 'PV_Incremental', 'Currency'),
        ('', 'EV_Physical_Percent', 'Double'),
        ('', 'EV_Incremental_Calculated', 'Currency'),
        ('', 'AC_Incremental', 'Currency')
    ], '#1F4E79')

    # Fact_Gantt_Schedule (Center Hub Right)
    draw_table_card(ax, 1380, 750, 420, 'Fact_Gantt_Schedule (Schedule Fact - *)', [
        ('FK', 'Task_ID (Relationship Key)', 'Text'),
        ('', 'Task_Name', 'Text'),
        ('', 'WBS_Code', 'Text'),
        ('', 'Baseline_Start', 'Date'),
        ('', 'Baseline_End', 'Date'),
        ('', 'Actual_Start', 'Date'),
        ('', 'Actual_End', 'Date'),
        ('FK', 'Predecessor_Task_ID', 'Text'),
        ('', 'Critical_Path_Flag', 'Text'),
        ('', 'Baseline_Duration_Days', 'Calculated Column'),
        ('', 'Actual_Duration_Days', 'Calculated Column'),
        ('', 'Schedule_Variance_Days', 'Calculated Column')
    ], '#7C3AED')

    # Fact_Waterfall_Bridge
    draw_table_card(ax, 50, 360, 360, 'Fact_Waterfall_Bridge (*)', [
        ('PK', 'Step_ID', 'Int64'),
        ('', 'Component_Name', 'Text'),
        ('', 'Type', 'Text'),
        ('', 'Incremental_Cost', 'Currency'),
        ('', 'Cumulative_Cost', 'Currency'),
        ('', 'Waterfall_Bar_Color', 'Calculated Column')
    ], '#4B5563')

    # Fact_Risk_Register
    draw_table_card(ax, 440, 360, 380, 'Fact_Risk_Register (*)', [
        ('PK', 'Risk_ID', 'Text'),
        ('', 'Risk_Title', 'Text'),
        ('', 'Probability', 'Int64'),
        ('', 'Impact', 'Int64'),
        ('', 'Risk_Score', 'Int64'),
        ('', 'Financial_Exposure', 'Currency'),
        ('', 'Heatmap_Coordinate', 'Calculated Column')
    ], '#DC2626')

    # Fact_Monthly_Burn_Rate
    draw_table_card(ax, 850, 360, 360, 'Fact_Monthly_Burn_Rate (*)', [
        ('PK', 'Period', 'Text'),
        ('', 'Monthly_PV', 'Currency'),
        ('', 'Monthly_EV', 'Currency'),
        ('', 'Monthly_AC', 'Currency'),
        ('', 'Cum_AC', 'Currency'),
        ('', 'Remaining_BAC', 'Currency')
    ], '#7F1D1D')

    # DAX Master Measures Block (Center Bottom)
    draw_table_card(ax, 1240, 360, 660, 'DAX Master Measure Group (Calculated Metrics Library)', [
        ('M', 'Status_Date / Total_Budget_at_Completion_BAC', 'DAX Measures'),
        ('M', 'PV_S_Curve / EV_S_Curve / AC_S_Curve', 'DAX Time-Intelligence'),
        ('M', 'Cost_Variance_CV / Schedule_Variance_SV / CPI / SPI', 'DAX Variances'),
        ('M', 'Estimate_at_Completion_EAC / Variance_at_Completion_VAC', 'DAX Forecasting'),
        ('M', 'TCPI_BAC / TCPI_EAC / ETC_Remaining_Liquidity_Needed', 'DAX Efficiency'),
        ('M', 'Earned_Schedule_Months / SPI_Time_Based / Time_Variance_Days', 'Earned Schedule'),
        ('M', 'CPI_RAG_Color / SPI_RAG_Color / VAC_RAG_Color / TCPI_RAG_Color', 'Tufte RAG Colors'),
        ('M', 'Project_NPV_10Pct_WACC / Project_IRR / Payback / ROI', 'Financial Appraisal'),
        ('M', 'MonteCarlo_P10_EAC / P50 / P80 / P90 / P95 / P90_Reserve', 'Monte Carlo Runs')
    ], '#D97706')

    # Relationship Arrows
    # Dim_Date -> Fact_EVM_Periodic (* : 1)
    ax.annotate('', xy=(280, 750), xytext=(280, 930), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#2563EB", lw=2.5))
    ax.text(290, 910, "1 (One Side)", fontsize=10, fontweight='bold', color="#2563EB")
    ax.text(290, 770, "* (Many Side)", fontsize=10, fontweight='bold', color="#2563EB")

    # Dim_WBS -> Fact_EVM_Periodic (* : 1)
    ax.annotate('', xy=(620, 600), xytext=(1540, 930), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#059669", lw=2.5, connectionstyle="arc3,rad=-0.15"))
    ax.text(1510, 910, "1", fontsize=10, fontweight='bold', color="#059669")
    ax.text(635, 615, "*", fontsize=10, fontweight='bold', color="#059669")

    # Dim_WBS -> Fact_Gantt_Schedule (* : 1)
    ax.annotate('', xy=(1500, 750), xytext=(1640, 930), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#059669", lw=2.5))
    ax.text(1650, 910, "1", fontsize=10, fontweight='bold', color="#059669")
    ax.text(1510, 770, "*", fontsize=10, fontweight='bold', color="#059669")

    plt.tight_layout()
    star_path = os.path.join(DOCS_DIR, "powerbi_star_schema_diagram.png")
    fig.savefig(star_path, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close(fig)
    print("[PASS] Rendered:", star_path)
    shutil.copy(star_path, os.path.join(BRAIN_DIR, "powerbi_star_schema_diagram.png"))

if __name__ == "__main__":
    generate_full_erd()
    generate_powerbi_star_schema()
