import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

def render_diagrams():
    base_dir = "C:/Users/frank/Desktop/EVM"
    docs_dir = os.path.join(base_dir, "06_docs")
    brain_dir = "C:/Users/frank/.gemini/antigravity-cli/brain/672e7105-6253-4293-a010-17f354864302"

    # =========================================================================
    # 1. RENDER SQLITE TRANSACTIONAL ERD DIAGRAM
    # =========================================================================
    fig1, ax1 = plt.subplots(figsize=(15, 9), dpi=300)
    ax1.set_facecolor('#F8F9FA')
    fig1.patch.set_facecolor('#F8F9FA')
    ax1.axis('off')
    ax1.set_xlim(0, 1500)
    ax1.set_ylim(0, 900)

    ax1.text(750, 860, "SQLite Enterprise EVM & Gantt Transactional ERD", 
             fontsize=16, fontweight='bold', ha='center', va='center', color='#1F2937')
    ax1.text(750, 830, "North Sea Oil Platform Drill Tower Project (PRAGMA foreign_keys = ON)", 
             fontsize=11, color='#6B7280', ha='center', va='center')

    def draw_table(ax, x, y, width, title, fields, header_color='#1F4E79'):
        row_h = 26
        head_h = 34
        tot_h = head_h + len(fields) * row_h
        
        box = patches.FancyBboxPatch((x, y - tot_h), width, tot_h, boxstyle="round,pad=0,rounding_size=4", facecolor='#FFFFFF', edgecolor='#D1D5DB', linewidth=1.2)
        ax.add_patch(box)
        head_box = patches.FancyBboxPatch((x, y - head_h), width, head_h, boxstyle="round,pad=0,rounding_size=4", facecolor=header_color, edgecolor=header_color, linewidth=0)
        ax.add_patch(head_box)
        ax.text(x + width/2, y - head_h/2, title, fontsize=11, fontweight='bold', color='#FFFFFF', ha='center', va='center')
        
        curr_y = y - head_h - row_h/2
        for key_type, name, data_type in fields:
            if key_type == 'PK':
                ax.text(x + 12, curr_y, 'PK', fontsize=8.5, fontweight='bold', color='#D97706', ha='left', va='center')
            elif key_type == 'FK':
                ax.text(x + 12, curr_y, 'FK', fontsize=8.5, fontweight='bold', color='#2563EB', ha='left', va='center')
            else:
                ax.text(x + 12, curr_y, '  ', fontsize=8.5, ha='left', va='center')
            ax.text(x + 45, curr_y, name, fontsize=9.5, fontweight='bold' if key_type else 'normal', color='#1F2937', ha='left', va='center')
            ax.text(x + width - 12, curr_y, data_type, fontsize=8.5, fontfamily='monospace', color='#6B7280', ha='right', va='center')
            ax.plot([x, x + width], [curr_y - row_h/2, curr_y - row_h/2], color='#F3F4F6', linewidth=0.8)
            curr_y -= row_h

    # Entities for SQLite ERD
    draw_table(ax1, 60, 780, 310, 'Dim_Date', [
        ('PK', 'Date_Key', 'TEXT'), ('', 'Year', 'INTEGER'), ('', 'Month_Number', 'INTEGER'),
        ('', 'Month_Name', 'TEXT'), ('', 'Year_Month', 'TEXT'), ('', 'Quarter', 'TEXT')
    ], '#2563EB')

    draw_table(ax1, 440, 800, 380, 'Fact_EVM_Periodic', [
        ('PK', 'Fact_ID', 'INTEGER AUTO'), ('FK', 'Task_ID', 'TEXT'), ('FK', 'Date_Key', 'TEXT'),
        ('', 'Total_Budget_Cost', 'REAL'), ('', 'PV_Incremental', 'REAL'), ('', 'EV_Physical_Percent', 'REAL'),
        ('', 'EV_Incremental_Calculated', 'REAL'), ('', 'AC_Incremental', 'REAL')
    ], '#1F4E79')

    draw_table(ax1, 890, 800, 420, 'Fact_Gantt_Schedule', [
        ('PK', 'Task_ID', 'TEXT'), ('', 'Task_Name', 'TEXT'), ('', 'WBS_Code', 'TEXT'),
        ('', 'CAM', 'TEXT'), ('', 'Baseline_Start', 'TEXT'), ('', 'Baseline_End', 'TEXT'),
        ('', 'Actual_Start', 'TEXT'), ('', 'Actual_End', 'TEXT'), ('FK', 'Predecessor_Task_ID', 'TEXT'),
        ('', 'Dependency_Type', 'TEXT'), ('', 'Critical_Path_Flag', 'TEXT')
    ], '#7C3AED')

    draw_table(ax1, 60, 380, 310, 'Dim_WBS', [
        ('PK', 'Task_ID', 'TEXT'), ('', 'WBS_Code', 'TEXT'), ('', 'WBS_Level_1', 'TEXT'),
        ('', 'WBS_Level_2', 'TEXT'), ('', 'Task_Name', 'TEXT'), ('', 'CAM', 'TEXT'), ('', 'TBC', 'REAL')
    ], '#059669')

    # SQLite Relations Arrows
    # Dim_Date -> Fact_EVM_Periodic
    ax1.annotate('', xy=(440, 720), xytext=(370, 720), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#2563EB", lw=2))
    ax1.text(380, 730, "1", fontsize=11, fontweight='bold', color="#2563EB")
    ax1.text(425, 730, "N", fontsize=11, fontweight='bold', color="#2563EB")

    # Dim_WBS -> Fact_EVM_Periodic
    ax1.annotate('', xy=(550, 560), xytext=(370, 320), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#059669", lw=2, connectionstyle="arc3,rad=-0.2"))
    ax1.text(380, 335, "1", fontsize=11, fontweight='bold', color="#059669")
    ax1.text(535, 545, "N", fontsize=11, fontweight='bold', color="#059669")

    # Dim_WBS -> Fact_Gantt_Schedule
    ax1.annotate('', xy=(890, 580), xytext=(370, 260), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#059669", lw=2, connectionstyle="arc3,rad=-0.3"))
    ax1.text(380, 275, "1", fontsize=11, fontweight='bold', color="#059669")
    ax1.text(870, 565, "1", fontsize=11, fontweight='bold', color="#059669")

    # Self reference Fact_Gantt_Schedule Predecessor
    ax1.annotate('', xy=(1310, 550), xytext=(1310, 680), arrowprops=dict(arrowstyle="->,head_width=0.4", color="#7C3AED", lw=2, connectionstyle="arc3,rad=-0.6"))
    ax1.text(1385, 610, "Self FK (Predecessor)", fontsize=8.5, color="#7C3AED", rotation=-90, fontweight='bold')

    plt.tight_layout()
    sqlite_png = os.path.join(docs_dir, "sqlite_erd_diagram.png")
    fig1.savefig(sqlite_png, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close(fig1)

    # =========================================================================
    # 2. RENDER POWER BI STAR SCHEMA DATA MODEL DIAGRAM
    # =========================================================================
    fig2, ax2 = plt.subplots(figsize=(15, 9), dpi=300)
    ax2.set_facecolor('#F8F9FA')
    fig2.patch.set_facecolor('#F8F9FA')
    ax2.axis('off')
    ax2.set_xlim(0, 1500)
    ax2.set_ylim(0, 900)

    ax2.text(750, 860, "Power BI Desktop Relational Star Schema Data Model View", 
             fontsize=16, fontweight='bold', ha='center', va='center', color='#1F2937')
    ax2.text(750, 830, "Optimized VertiPaq Star Schema | Single Unidirectional Filtering (* : 1)", 
             fontsize=11, color='#6B7280', ha='center', va='center')

    # Dim_Date (Top Left)
    draw_table(ax2, 100, 800, 320, 'Dim_Date (1)', [
        ('PK', 'Date_Key', 'Date'), ('', 'Year', 'Int'), ('', 'Month_Number', 'Int'),
        ('', 'Month_Name', 'Text'), ('', 'Year_Month', 'Text'), ('', 'Quarter', 'Text')
    ], '#2563EB')

    # Dim_WBS (Top Right)
    draw_table(ax2, 1080, 800, 320, 'Dim_WBS (1)', [
        ('PK', 'Task_ID', 'Text'), ('', 'WBS_Code', 'Text'), ('', 'WBS_Level_1', 'Text'),
        ('', 'WBS_Level_2', 'Text'), ('', 'Task_Name', 'Text'), ('', 'CAM', 'Text'), ('', 'TBC', 'Currency')
    ], '#059669')

    # Fact_EVM_Periodic (Center Left)
    draw_table(ax2, 200, 480, 380, 'Fact_EVM_Periodic (*)', [
        ('FK', 'Task_ID_FK (Hidden)', 'Text'), ('FK', 'Date_Key_FK (Hidden)', 'Date'),
        ('', 'Total_Budget_Cost', 'Currency'), ('', 'PV_Incremental', 'Currency'),
        ('', 'EV_Physical_Percent', 'Double'), ('', 'EV_Incremental_Calculated', 'Currency'),
        ('', 'AC_Incremental', 'Currency')
    ], '#1F4E79')

    # Fact_Gantt_Schedule (Center Right)
    draw_table(ax2, 850, 480, 400, 'Fact_Gantt_Schedule (*)', [
        ('FK', 'Task_ID_FK (Hidden)', 'Text'), ('', 'Task_Name', 'Text'), ('', 'WBS_Code', 'Text'),
        ('', 'Baseline_Start', 'Date'), ('', 'Baseline_End', 'Date'), ('', 'Actual_Start', 'Date'),
        ('', 'Actual_End', 'Date'), ('FK', 'Predecessor_Task_ID', 'Text'), ('', 'Critical_Path_Flag', 'Text')
    ], '#7C3AED')

    # DAX Measures Group Table (Bottom Center)
    draw_table(ax2, 530, 220, 440, 'EVM_DAX_Measures (Measure Table)', [
        ('', 'Total_Budget_at_Completion_BAC', 'DAX Measure'),
        ('', 'PV_S_Curve_WINDOW / EV_S_Curve / AC_S_Curve', 'DAX Measure'),
        ('', 'CFO_Cost_Variance_CV / CPI / EAC / VAC', 'DAX Measure'),
        ('', 'Controller_Earned_Schedule_Months / SPI(t)', 'DAX Measure'),
        ('', 'RAG_CPI_Color / RAG_SPI_Color / RAG_VAC_Color', 'DAX Measure')
    ], '#D97706')

    # Relationship Arrows (* : 1 Unidirectional)
    # Dim_Date -> Fact_EVM_Periodic (* : 1)
    ax2.annotate('', xy=(260, 480), xytext=(260, 600), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#2563EB", lw=2.5))
    ax2.text(270, 580, "1 (One Side)", fontsize=10, fontweight='bold', color="#2563EB")
    ax2.text(270, 500, "* (Many Side)", fontsize=10, fontweight='bold', color="#2563EB")
    ax2.text(160, 540, "Single Direction Filter", fontsize=8.5, color="#2563EB", rotation=90)

    # Dim_WBS -> Fact_EVM_Periodic (* : 1)
    ax2.annotate('', xy=(580, 360), xytext=(1080, 600), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#059669", lw=2.5, connectionstyle="arc3,rad=-0.1"))
    ax2.text(1050, 590, "1", fontsize=10, fontweight='bold', color="#059669")
    ax2.text(595, 375, "*", fontsize=10, fontweight='bold', color="#059669")

    # Dim_WBS -> Fact_Gantt_Schedule (* : 1)
    ax2.annotate('', xy=(950, 480), xytext=(1180, 600), arrowprops=dict(arrowstyle="<-,head_width=0.4", color="#059669", lw=2.5))
    ax2.text(1190, 580, "1", fontsize=10, fontweight='bold', color="#059669")
    ax2.text(960, 500, "*", fontsize=10, fontweight='bold', color="#059669")

    plt.tight_layout()
    pbi_png = os.path.join(docs_dir, "powerbi_starschema_diagram.png")
    fig2.savefig(pbi_png, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close(fig2)

    # Copy to brain artifact directory
    if os.path.exists(brain_dir):
        shutil.copy(sqlite_png, os.path.join(brain_dir, "sqlite_erd_diagram.png"))
        shutil.copy(pbi_png, os.path.join(brain_dir, "powerbi_starschema_diagram.png"))
        print("Copied diagrams to brain artifacts directory.")

    print("[SUCCESS] Data model diagrams rendered:")
    print("  - sqlite_erd_diagram.png")
    print("  - powerbi_starschema_diagram.png")

if __name__ == "__main__":
    render_diagrams()
