"""
Generates the Master Power BI EVM Implementation & Architecture Guide (PDF).
Includes complete data schemas, DAX measures, VOR update procedures, scenario parameters,
Tufte visualization standards, Fabric/Azure architecture, and stakeholder dashboard mockups.
"""

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "06_docs")
PDF_PATH = os.path.join(DOCS_DIR, "PowerBI_EVM_Master_Guide_and_Architecture.pdf")
BRAIN_DIR = "C:/Users/frank/.gemini/antigravity-cli/brain/97cb6b09-997d-43e7-bc58-78e7c079917c"

# Source dashboard images
img_sources = {
    "pm": os.path.join(BRAIN_DIR, "pm_evm_dashboard_1786637751385.jpg"),
    "cfo": os.path.join(BRAIN_DIR, "cfo_financial_dashboard_1786637766271.jpg"),
    "controller": os.path.join(BRAIN_DIR, "controller_evm_dashboard_1786637780547.jpg"),
    "executive": os.path.join(BRAIN_DIR, "executive_steering_dashboard_1786637793839.jpg")
}

# Target docs images
img_targets = {}
for key, src in img_sources.items():
    dst = os.path.join(DOCS_DIR, f"{key}_dashboard_mockup.jpg")
    if os.path.exists(src):
        shutil.copy(src, dst)
    img_targets[key] = dst if os.path.exists(dst) else src

def build_guide_pdf():
    print(f"================================================================================")
    print(f"Generating Master Power BI EVM Guide PDF: {PDF_PATH}")
    print(f"================================================================================")

    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    doc_title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'MainSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=6
    )

    tbl_cell_left = ParagraphStyle('TCellL', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor('#1E293B'))
    tbl_cell_bold = ParagraphStyle('TCellB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=colors.HexColor('#0F172A'))

    story = []

    # TITLE & HEADER
    story.append(Paragraph("Enterprise Power BI Earned Value Management (EVM) Master Guide", doc_title_style))
    story.append(Paragraph("Complete Architecture, Data Modeling, DAX Library, Change Management (VOR), What-If Scenarios, Stakeholder Visuals & MS Fabric/Azure Integration", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=0, spaceAfter=10))

    meta_table_data = [
        [Paragraph("<b>Author / Role:</b> Frank Ellingsen, Lead Project Controller", tbl_cell_left), Paragraph("<b>Target Sector:</b> EPC Offshore, Maritime & Heavy Engineering", tbl_cell_left)],
        [Paragraph("<b>Data Engines:</b> DuckDB (Analytics) & SQLite (Transactional)", tbl_cell_left), Paragraph("<b>UI Standards:</b> Edward Tufte Data-Ink Ratio (Zero Clutter)", tbl_cell_left)],
        [Paragraph("<b>Status Date:</b> August 31, 2026 (Month 8 / Week 36)", tbl_cell_left), Paragraph("<b>Baseline Budget (BAC):</b> $26,500,000 | Outturn EAC: $35,413,604", tbl_cell_left)]
    ]
    t_meta = Table(meta_table_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # SECTION 1: DATA ARCHITECTURE & REQUIRED DATA TABLES
    story.append(Paragraph("1. Data Architecture & Required Data Tables", h1_style))
    story.append(Paragraph("To deliver enterprise EVM in Power BI, data must be structured in a strict Star Schema star-join model separating dimensional attributes from periodic transactional facts.", body_style))

    wbs_table_data = [
        ["Table Name", "Type", "Primary Key", "Description & Required Attributes"],
        ["Dim_WBS", "Dimension", "Task_ID", "WBS hierarchy (Task_ID, WBS_Code, WBS_L1, WBS_L2, Task_Name, CAM, TBC/BAC)."],
        ["Dim_Date", "Dimension", "Date_Key", "Calendar dimension (Date_Key, Year, Month_Number, Month_Name, Year_Month, Quarter)."],
        ["Fact_EVM_Periodic", "Fact", "Fact_ID", "Periodic snapshots (Task_ID, Date_Key, TBC, PV_Incremental, EV_%, EV_Calculated, AC_Incremental)."],
        ["Fact_Gantt_Schedule", "Fact", "Task_ID", "Schedule status (Task_ID, Baseline_Start/End, Actual_Start/End, Predecessor, Critical_Path_Flag)."],
        ["Fact_Change_Requests_VOR", "Fact", "VOR_ID", "Variation Orders (VOR_ID, Task_ID, Date_Key, Description, Cost_Delta, Approved_Cost, Status)."],
        ["Fact_Risk_Register", "Fact", "Risk_ID", "Active risk matrix (Risk_ID, Title, WBS_Code, Risk_Score, Financial_Exposure, Status)."]
    ]
    t_wbs = Table(wbs_table_data, colWidths=[110, 55, 65, 310])
    t_wbs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_wbs)
    story.append(Spacer(1, 10))

    # SECTION 2: UPDATING DATABASES, VOR & CHANGE REQUESTS
    story.append(Paragraph("2. Updating Databases, Change Requests (VOR) & Re-baselining", h1_style))
    story.append(Paragraph("<b>Variation Order Requests (VOR)</b> and Scope Changes require strict distinction between original baseline, approved variations, and pending claims:", body_style))
    story.append(Paragraph("<b>Formulas:</b> Original Baseline (BAC_Orig) = Sum(Dim_WBS.TBC) | Approved VOR Delta = Sum(Fact_VOR[Approved_Cost_Delta]) | Adjusted Baseline (BAC_Adj) = BAC_Orig + Approved VOR Delta", body_style))

    vor_sql_code = """-- SQL View Pattern: Integrating Approved Change Requests into Adjusted BAC
CREATE VIEW View_Adjusted_WBS_Baseline AS
SELECT 
    w.WBS_Code,
    w.Task_Name,
    w.CAM,
    w.TBC AS BAC_Original,
    COALESCE(SUM(CASE WHEN v.Status = 'Approved' THEN v.Approved_Cost_Delta ELSE 0 END), 0) AS Approved_VOR_Cost,
    COALESCE(SUM(CASE WHEN v.Status = 'Pending' THEN v.Requested_Cost_Delta ELSE 0 END), 0) AS Pending_VOR_Exposure,
    (w.TBC + COALESCE(SUM(CASE WHEN v.Status = 'Approved' THEN v.Approved_Cost_Delta ELSE 0 END), 0)) AS BAC_Adjusted
FROM Dim_WBS w
LEFT JOIN Fact_Change_Requests_VOR v ON w.Task_ID = v.Task_ID
GROUP BY w.WBS_Code, w.Task_Name, w.CAM, w.TBC;"""
    story.append(Paragraph(vor_sql_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 8))

    # SECTION 3: COMPLETE DAX MEASURE LIBRARY
    story.append(Paragraph("3. Complete Production DAX Measure Library", h1_style))
    
    dax_code_block = """// ===============================================================================
// PRODUCTION DAX MEASURE LIBRARY (EARNED VALUE MANAGEMENT & VARIATION ORDERS)
// ===============================================================================

// 1. CORE VALUE METRICS
Total_Budget_at_Completion_BAC = SUM(Dim_WBS[TBC])

PV_S_Curve = CALCULATE(SUM(Fact_EVM_Periodic[PV_Incremental]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key])))

EV_S_Curve = 
VAR CurrentDate = MAX(Dim_Date[Date_Key])
VAR StatusDate = MAX(Fact_EVM_Periodic[Date_Key])
RETURN IF(CurrentDate <= StatusDate, CALCULATE(SUM(Fact_EVM_Periodic[EV_Incremental_Calculated]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key]))), BLANK())

AC_S_Curve = 
VAR CurrentDate = MAX(Dim_Date[Date_Key])
VAR StatusDate = MAX(Fact_EVM_Periodic[Date_Key])
RETURN IF(CurrentDate <= StatusDate, CALCULATE(SUM(Fact_EVM_Periodic[AC_Incremental]), WINDOW(1, ABS, 0, REL, ORDERBY(Dim_Date[Date_Key]))), BLANK())

// 2. VARIANCES & PERFORMANCE INDICES
Cost_Variance_CV = [EV_S_Curve] - [AC_S_Curve]
Schedule_Variance_SV = [EV_S_Curve] - [PV_S_Curve]

Cost_Performance_Index_CPI = DIVIDE([EV_S_Curve], [AC_S_Curve], 1.0)
Schedule_Performance_Index_SPI = DIVIDE([EV_S_Curve], [PV_S_Curve], 1.0)
Critical_Ratio_CR = [Cost_Performance_Index_CPI] * [Schedule_Performance_Index_SPI]

// 3. LIPKE EARNED SCHEDULE METRICS (TIME VELOCITY)
Earned_Schedule_Months = 
VAR CurrentEV = [EV_S_Curve]
VAR DateTableWithPV = FILTER(ALL(Dim_Date), [PV_S_Curve] <= CurrentEV)
VAR C_MonthDate = MAXX(DateTableWithPV, Dim_Date[Date_Key])
VAR C_MonthNumber = MAXX(DateTableWithPV, Dim_Date[Month_Number])
VAR PV_At_C = CALCULATE([PV_S_Curve], Dim_Date[Date_Key] = C_MonthDate)
VAR PV_At_C_Plus_1 = CALCULATE([PV_S_Curve], DATEADD(Dim_Date[Date_Key], 1, MONTH))
VAR Interpolation = DIVIDE(CurrentEV - PV_At_C, PV_At_C_Plus_1 - PV_At_C, 0)
RETURN IF(CurrentEV >= [Total_Budget_at_Completion_BAC], MAX(Dim_Date[Month_Number]), C_MonthNumber + Interpolation)

SPI_Time_Based = DIVIDE([Earned_Schedule_Months], MAX(Dim_Date[Month_Number]), 1.0)
Time_Variance_Days = ROUND(([Earned_Schedule_Months] - MAX(Dim_Date[Month_Number])) * 30.4375, 0)

// 4. FORECASTING & TO-COMPLETE METRICS
Estimate_at_Completion_EAC = DIVIDE([Total_Budget_at_Completion_BAC], [Cost_Performance_Index_CPI], [Total_Budget_at_Completion_BAC])
Variance_at_Completion_VAC = [Total_Budget_at_Completion_BAC] - [Estimate_at_Completion_EAC]

TCPI_BAC = DIVIDE([Total_Budget_at_Completion_BAC] - [EV_S_Curve], [Total_Budget_at_Completion_BAC] - [AC_S_Curve], 1.0)
TCPI_EAC = DIVIDE([Total_Budget_at_Completion_BAC] - [EV_S_Curve], [Estimate_at_Completion_EAC] - [AC_S_Curve], 1.0)

// 5. CHANGE REQUEST & VOR METRICS
Approved_VOR_Delta = CALCULATE(SUM(Fact_Change_Requests_VOR[Approved_Cost_Delta]), Fact_Change_Requests_VOR[Status] = "Approved")
Pending_VOR_Exposure = CALCULATE(SUM(Fact_Change_Requests_VOR[Requested_Cost_Delta]), Fact_Change_Requests_VOR[Status] = "Pending")
BAC_Adjusted = [Total_Budget_at_Completion_BAC] + [Approved_VOR_Delta]

// 6. TUFTE CONDITIONAL FORMATTING RAG MEASURES
CPI_RAG_Color = VAR CPI = [Cost_Performance_Index_CPI] RETURN SWITCH(TRUE(), CPI < 0.90, "#DC2626", CPI < 1.00, "#D97706", "#059669")
CR_RAG_Color = VAR CR = [Critical_Ratio_CR] RETURN SWITCH(TRUE(), ISBLANK(CR), "#737373", CR < 0.90, "#DC2626", CR < 1.00, "#D97706", "#059669")"""
    story.append(Paragraph(dax_code_block.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # SECTION 4: WHAT-IF PARAMETERS & SCENARIO ANALYSIS
    story.append(Paragraph("4. Parameters & What-If Scenario Modeling in Power BI", h1_style))
    story.append(Paragraph("What-If parameters allow controllers to dynamically model recovery scenarios, labor productivity changes, and VOR approval rates directly in Power BI visuals.", body_style))

    scenario_dax = """// WHAT-IF SCENARIO DAX MEASURES
// Parameter 1: CPI Recovery Factor (Slicer Range: 0.70 to 1.15, Step 0.05)
EAC_Dynamic_Scenario = 
VAR RecoveryFactor = SELECTEDVALUE('CPI_Recovery_Parameter'[CPI_Recovery_Parameter], 1.00)
VAR ModeledCPI = [Cost_Performance_Index_CPI] * RecoveryFactor
RETURN DIVIDE([Total_Budget_at_Completion_BAC], ModeledCPI, [Total_Budget_at_Completion_BAC])

// Parameter 2: VOR Approval Realization Rate % (Slicer Range: 0% to 100%)
BAC_Scenario_With_Pending_VOR = 
VAR ApprovalRate = SELECTEDVALUE('VOR_Approval_Rate_Parameter'[VOR_Approval_Rate_Parameter], 0.50)
RETURN [BAC_Adjusted] + ([Pending_VOR_Exposure] * ApprovalRate)"""
    story.append(Paragraph(scenario_dax.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 10))

    # SECTION 5: STAKEHOLDER VISUAL CONSTRUCTION & MOCKUPS
    story.append(Paragraph("5. Stakeholder Visual Construction & Dashboard Mockups", h1_style))
    story.append(Paragraph("Following Edward Tufte's Data-Ink Ratio rules: zero background drop shadows, muted colors, direct line labels on S-Curves, left-aligned text columns, and right-aligned numbers.", body_style))

    # Stakeholder 1: PM
    story.append(Paragraph("Stakeholder View 1: Project Manager (PM) EVM Dashboard", h2_style))
    story.append(Paragraph("<b>Focus:</b> Physical completion %, Gantt schedule slippage, baseline S-Curve trends, and active change requests log.", body_style))
    if os.path.exists(img_targets["pm"]):
        story.append(RLImage(img_targets["pm"], width=520, height=292))
    story.append(Spacer(1, 10))

    # Stakeholder 2: CFO
    story.append(Paragraph("Stakeholder View 2: CFO Financial Control & Liquidity Dashboard", h2_style))
    story.append(Paragraph("<b>Focus:</b> Outturn EAC forecast, Variance at Completion (VAC), Cost Variance Waterfall Bridge, and Monthly Cash Burn Rate.", body_style))
    if os.path.exists(img_targets["cfo"]):
        story.append(RLImage(img_targets["cfo"], width=520, height=292))
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # Stakeholder 3: Controller
    story.append(Paragraph("Stakeholder View 3: Project Controller Deep-Dive & Scenario Matrix", h2_style))
    story.append(Paragraph("<b>Focus:</b> Earned Schedule (ES), Time Variance (SVt), TCPI feasibility (6.07 vs 1.00), Scatter Plot Matrix (CV% vs SV%), and What-If Parameter slicers.", body_style))
    if os.path.exists(img_targets["controller"]):
        story.append(RLImage(img_targets["controller"], width=520, height=292))
    story.append(Spacer(1, 10))

    # Stakeholder 4: Executive Committee
    story.append(Paragraph("Stakeholder View 4: Executive Steering Committee Briefing", h2_style))
    story.append(Paragraph("<b>Focus:</b> Overall Project RAG Red alert, Monte Carlo P90 Risk Cost Distribution Curve ($35.82M), approved VOR impact, and Steering Action Decision Matrix.", body_style))
    if os.path.exists(img_targets["executive"]):
        story.append(RLImage(img_targets["executive"], width=520, height=292))
    story.append(Spacer(1, 10))

    # SECTION 6: MS FABRIC & AZURE INTEGRATION
    story.append(Paragraph("6. Enterprise Microsoft Fabric & Azure Integration Architecture", h1_style))
    story.append(Paragraph("For heavy industrial EPC environments, Power BI connects to Microsoft Fabric and Azure Data Services using Medallion Architecture (Bronze / Silver / Gold):", body_style))

    fabric_arch_data = [
        ["Layer", "Technology", "Storage Format", "Role & ETL Processing"],
        ["Ingestion", "Azure Data Factory / Fabric Pipelines", "REST / SQL Connector", "Ingest raw Primavera P6 schedule XML & SAP GL transaction logs."],
        ["Bronze (Raw)", "Azure Data Lake Storage Gen2 (ADLS)", "Parquet / Delta Lake", "Immutable historical land of raw transactional snapshots."],
        ["Silver (Clean)", "Fabric Synapse PySpark Notebooks", "Delta Lake Tables", "Cleanse schema, enforce foreign key integrity, compute incremental EVM."],
        ["Gold (Analytics)", "Fabric OneLake Data Warehouse", "Delta Lake (Gold)", "Star Schema (Dim_WBS, Dim_Date, Fact_EVM_Periodic, Fact_VOR)."],
        ["Serving (BI)", "Power BI Direct Lake Mode", "OneLake Direct Lake", "Zero-copy Direct Lake query engine providing sub-second load times."]
    ]
    t_fabric = Table(fabric_arch_data, colWidths=[70, 115, 95, 260])
    t_fabric.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(t_fabric)
    story.append(Spacer(1, 12))

    doc.build(story)
    print(f" [PASS] Master Guide PDF successfully generated at: {PDF_PATH}")

if __name__ == "__main__":
    build_guide_pdf()
