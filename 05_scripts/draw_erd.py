import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
import os

def generate_erd():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('#F8F9FA')
    
    ax.axis('off')
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 800)

    ax.text(700, 760, "SQLite Enterprise EVM Data Model Entity-Relationship Diagram (ERD)", 
            fontsize=16, fontweight='bold', ha='center', va='center', color='#1F2937', fontfamily='sans-serif')
    ax.text(700, 735, "Relational Star Schema with Foreign Key Constraints (1 : N Cardinality)", 
            fontsize=11, color='#6B7280', ha='center', va='center', fontfamily='sans-serif')

    def draw_entity(x, y, width, title, fields, header_color='#1F4E79'):
        row_height = 28
        header_height = 36
        total_height = header_height + len(fields) * row_height
        
        rect = patches.FancyBboxPatch((x, y - total_height), width, total_height,
                                      boxstyle="round,pad=0,rounding_size=4",
                                      facecolor='#FFFFFF', edgecolor='#D1D5DB', linewidth=1.2)
        ax.add_patch(rect)
        
        header_rect = patches.FancyBboxPatch((x, y - header_height), width, header_height,
                                             boxstyle="round,pad=0,rounding_size=4",
                                             facecolor=header_color, edgecolor=header_color, linewidth=0)
        ax.add_patch(header_rect)
        
        ax.text(x + width/2, y - header_height/2, title,
                fontsize=12, fontweight='bold', color='#FFFFFF', ha='center', va='center', fontfamily='sans-serif')
        
        curr_y = y - header_height - row_height/2
        for key_type, name, data_type in fields:
            if key_type == 'PK':
                ax.text(x + 15, curr_y, 'PK', fontsize=9, fontweight='bold', color='#D97706', ha='left', va='center')
            elif key_type == 'FK':
                ax.text(x + 15, curr_y, 'FK', fontsize=9, fontweight='bold', color='#2563EB', ha='left', va='center')
            else:
                ax.text(x + 15, curr_y, '  ', fontsize=9, ha='left', va='center')

            ax.text(x + 50, curr_y, name, fontsize=10, fontweight='bold' if key_type else 'normal', color='#1F2937', ha='left', va='center')
            ax.text(x + width - 15, curr_y, data_type, fontsize=9, fontfamily='monospace', color='#6B7280', ha='right', va='center')
            ax.plot([x, x + width], [curr_y - row_height/2, curr_y - row_height/2], color='#F3F4F6', linewidth=0.8)
            curr_y -= row_height
            
        return (x, y, width, total_height)

    dim_date_fields = [
        ('PK', 'Date_Key', 'TEXT'),
        ('', 'Year', 'INTEGER'),
        ('', 'Month_Number', 'INTEGER'),
        ('', 'Month_Name', 'TEXT'),
        ('', 'Year_Month', 'TEXT'),
        ('', 'Quarter', 'TEXT')
    ]
    draw_entity(80, 650, 320, 'Dim_Date', dim_date_fields, header_color='#2563EB')

    fact_fields = [
        ('PK', 'Fact_ID', 'INTEGER AUTO'),
        ('FK', 'Task_ID', 'TEXT'),
        ('FK', 'Date_Key', 'TEXT'),
        ('', 'Total_Budget_Cost', 'REAL'),
        ('', 'PV_Incremental', 'REAL'),
        ('', 'EV_Physical_Percent', 'REAL'),
        ('', 'EV_Incremental_Calculated', 'REAL'),
        ('', 'AC_Incremental', 'REAL')
    ]
    draw_entity(510, 680, 380, 'Fact_EVM_Periodic', fact_fields, header_color='#1F4E79')

    dim_wbs_fields = [
        ('PK', 'Task_ID', 'TEXT'),
        ('', 'WBS_Code', 'TEXT'),
        ('', 'WBS_Level_1', 'TEXT'),
        ('', 'WBS_Level_2', 'TEXT'),
        ('', 'Task_Name', 'TEXT'),
        ('', 'CAM', 'TEXT'),
        ('', 'TBC', 'REAL')
    ]
    draw_entity(1000, 660, 320, 'Dim_WBS', dim_wbs_fields, header_color='#059669')

    ax.annotate('', xy=(510, 580), xytext=(400, 615),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#2563EB", lw=2, connectionstyle="arc3,rad=-0.15"))
    ax.text(410, 630, "1", fontsize=12, fontweight='bold', color="#2563EB")
    ax.text(495, 595, "N", fontsize=12, fontweight='bold', color="#2563EB")
    ax.text(445, 620, "FOREIGN KEY (Date_Key)", fontsize=8, color="#2563EB", rotation=-16)

    ax.annotate('', xy=(890, 610), xytext=(1000, 625),
                arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color="#059669", lw=2, connectionstyle="arc3,rad=0.15"))
    ax.text(990, 635, "1", fontsize=12, fontweight='bold', color="#059669")
    ax.text(905, 620, "N", fontsize=12, fontweight='bold', color="#059669")
    ax.text(935, 635, "FOREIGN KEY (Task_ID)", fontsize=8, color="#059669", rotation=12)

    note_box = patches.FancyBboxPatch((400, 100), 600, 130,
                                      boxstyle="round,pad=0,rounding_size=4",
                                      facecolor='#F3F4F6', edgecolor='#E5E7EB', linewidth=1)
    ax.add_patch(note_box)
    ax.text(700, 205, "SQLite Database Governance & Integrity Rules", fontsize=11, fontweight='bold', color='#1F2937', ha='center')
    ax.text(700, 180, "• Enabled PRAGMA foreign_keys = ON for strict relational integrity.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(700, 158, "• Cascade deletion rules configured on Fact_EVM_Periodic foreign keys.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(700, 136, "• View_EVM_Summary synthesized for direct SQL outturn queries.", fontsize=9.5, color='#4B5563', ha='center')
    ax.text(700, 114, "• Path: C:/Users/frank/Desktop/EVM/02_databases/evm_transactional.db", fontsize=9, fontfamily='monospace', color='#1F4E79', ha='center')

    plt.tight_layout()
    output_png = "C:/Users/frank/Desktop/EVM/06_docs/erd_diagram.png"
    plt.savefig(output_png, bbox_inches='tight', facecolor='#F8F9FA')
    plt.close()
    print("ERD diagram rendered to:", output_png)

    brain_dir = "C:/Users/frank/.gemini/antigravity-cli/brain/672e7105-6253-4293-a010-17f354864302"
    if os.path.exists(brain_dir):
        shutil.copy(output_png, os.path.join(brain_dir, "erd_diagram.png"))
        print("Copied ERD diagram to brain artifacts directory.")

if __name__ == "__main__":
    generate_erd()
