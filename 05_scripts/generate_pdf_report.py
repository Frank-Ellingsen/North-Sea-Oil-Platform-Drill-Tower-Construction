"""
Generates a PDF Executive Status Report for the Offshore EPC Platform Drill Tower Project.
Uses ReportLab to build a formatted PDF document.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "06_docs")
PDF_PATH = os.path.join(DOCS_DIR, "Drill_Tower_Project_Executive_Report.pdf")

def build_pdf():
    print(f"--- Generating PDF Executive Report: {PDF_PATH} ---")
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
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#111827'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#111827'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=6
    )
    alert_style = ParagraphStyle(
        'AlertCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#991B1B'),
        spaceAfter=8
    )
    
    story = []
    
    # Header Banner
    story.append(Paragraph("OFFSHORE EPC PLATFORM DRILL TOWER PROJECT", title_style))
    story.append(Paragraph("EXECUTIVE STEERING COMMITTEE PROJECT STATUS & APPRAISAL REPORT", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#111827"), spaceAfter=12))
    
    # Project Health Callout
    health_text = "<b>OVERALL PROJECT HEALTH:</b> <font color='#DC2626'>🚨 CRITICAL COST OVERRUN & SCHEDULE SLIPPAGE (RED)</font><br/>" \
                  "Status Date: August 31, 2026 (Month 8 / Week 36) | Prepared By: Frank Ellingsen, Lead Project Controller"
    story.append(Paragraph(health_text, alert_style))
    story.append(Spacer(1, 8))
    
    # Executive Summary Paragraph
    summary_p = "This report presents the Earned Value Management (EVM) status, commercial financial appraisal, " \
                "Monte Carlo risk simulation outturn, cash burn runway analysis, and step-by-step cost variance bridge " \
                "for the Offshore Platform Drill Tower Construction Project. The baseline budget ceiling ($BAC = $26.50M) " \
                "will be 100% depleted in <b>Month 9 (September 2026)</b>, requiring an executive funding line approval of " \
                "<b>+$8.91M</b> to fund remaining operations through commercial COD."
    story.append(Paragraph(summary_p, body_style))
    story.append(Spacer(1, 10))
    
    # SECTION 1: CORE EVM PERFORMANCE METRICS
    story.append(Paragraph("1. Earned Value Performance Metrics Summary", h2_style))
    
    evm_data = [
        ["EVM Metric Symbol", "Description / Standard Definition", "Value", "Status / RAG"],
        ["BAC", "Total Baseline Budget at Completion", "$26,500,000", "Approved Baseline"],
        ["PV", "Planned Value Baseline Progress (77.4%)", "$20,500,000", "Planned Progress"],
        ["EV", "Earned Value Physical Completion (66.2%)", "$17,540,000", "Earned Progress"],
        ["AC", "Cumulative Actual Cost Incurred", "$23,440,000", "Critical Overrun"],
        ["CV", "Cost Variance (EV - AC)", "-$5,900,000", "-33.6% Over Budget"],
        ["SV", "Schedule Variance (EV - PV)", "-$2,960,000", "-14.4% Schedule Lag"],
        ["CPI", "Cost Performance Index (EV / AC)", "0.7483", "Red ($0.75 / $1.00)"],
        ["SPI_t", "Earned Schedule Velocity (ES / Actual)", "0.9250", "Amber (-18.2 Days)"],
        ["EAC_1", "Most Likely Cost Outturn (BAC / CPI)", "$35,413,604", "+$8.91M Overrun"],
        ["EAC_t", "Predicted Completion Date (PD / SPI_t)", "Jan 31, 2027", "+31 Days Delay"]
    ]
    
    t_evm = Table(evm_data, colWidths=[60, 240, 100, 140])
    t_evm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_evm)
    story.append(Spacer(1, 12))
    
    # SECTION 2: COMMERCIAL FINANCIAL APPRAISAL & RATIOS
    story.append(Paragraph("2. Commercial Capital Budgeting & Financial Appraisal Ratios", h2_style))
    
    fin_data = [
        ["Financial Appraisal Metric", "Calculated Value", "Hurdle Rate / Benchmark", "Commercial Evaluation"],
        ["Net Present Value (NPV @ 10% WACC)", "+$14,899,563", "$0.00 Hurdle Target", "Strong Positive Net Capital Value"],
        ["Internal Rate of Return (IRR)", "18.86%", "10.0% Discount Rate", "Outperforms Hurdle by +886 bps"],
        ["Simple Payback Period", "4.43 Years", "< 5.0 Years Target", "53.1 Months (May 2031)"],
        ["Profitability Index (PI)", "1.42", "> 1.0 Benefit/Cost Ratio", "Generates $1.42 PV per $1.00 spent"],
        ["Total Simple ROI", "134.37%", "100.0% Baseline", "High 10-Year Return"],
        ["Annualized ROI (CAGR)", "8.89%/Year", "5.0% Risk-Free Rate", "Compounded Annual Growth Rate"],
        ["Gross Future Value (FV Yr 10)", "$130,499,397", "CAPEX Base", "Total Nominal Operating Inflow"]
    ]
    
    t_fin = Table(fin_data, colWidths=[180, 90, 110, 160])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 12))
    
    # SECTION 3: MONTE CARLO RISK SIMULATION (P90 ANALYSIS)
    story.append(Paragraph("3. Monte Carlo 10,000 Iteration Risk Simulation (P90 Percentiles)", h2_style))
    
    mc_data = [
        ["Percentile Level", "Confidence Level", "Outturn Cost (EAC)", "Overrun vs BAC", "Completion Date", "Schedule Delay"],
        ["P10", "10% Optimistic", "$32,444,302", "-$5,944,302", "Feb 13, 2027", "+43.1 Days"],
        ["P50", "50% Median", "$34,060,783", "-$7,560,783", "Feb 27, 2027", "+57.3 Days"],
        ["P80", "80% Standard Budget", "$35,195,026", "-$8,695,026", "Mar 09, 2027", "+67.3 Days"],
        ["P90 (High Confidence)", "90% High Confidence", "$35,815,202", "-$9,315,202", "Mar 14, 2027", "+72.5 Days"],
        ["P95", "95% Extreme Risk", "$36,272,986", "-$9,772,986", "Mar 18, 2027", "+76.6 Days"]
    ]
    
    t_mc = Table(mc_data, colWidths=[100, 110, 110, 100, 70, 50])
    t_mc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7F1D1D')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (2,0), (3,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#FEF2F2'))
    ]))
    story.append(t_mc)
    story.append(Spacer(1, 8))
    
    p90_text = "<b>P90 High-Confidence Finding:</b> Achieving 90% cost certainty requires a predicted outturn of " \
               "<b>$35,815,202</b> and an additional management contingency reserve of <b>+$401,598</b> above the base EAC."
    story.append(Paragraph(p90_text, body_style))
    story.append(Spacer(1, 12))
    
    # SECTION 4: COST VARIANCE WATERFALL BRIDGE
    story.append(Paragraph("4. Step-by-Step Cost Variance Waterfall Bridge ($BAC to EAC)", h2_style))
    
    wf_data = [
        ["Step", "WBS Code", "Control Account / Variance Driver", "Incremental Cost", "Cumulative Cost", "% Share"],
        ["0", "1.0", "Original Baseline Budget (BAC)", "$26,500,000", "$26,500,000", "0.0%"],
        ["1", "1.1.1", "Detail Structural Engineering Revisions", "+$300,000", "$26,800,000", "3.4%"],
        ["2", "1.2.1", "Procurement Subsea Tubular Steel Inflation", "+$600,000", "$27,400,000", "6.7%"],
        ["3", "1.3.1", "Verdal Sub-Structure Fabrication Yard", "+$200,000", "$27,600,000", "2.2%"],
        ["4", "1.3.2", "Egersund Derrick Mast Yard Rework", "+$2,400,000", "$30,000,000", "26.9%"],
        ["5", "1.4.1", "Heavy Lift Vessel Weather Standby", "+$1,300,000", "$31,300,000", "14.6%"],
        ["6", "1.4.2", "Offshore Topside Lifting & Mating", "+$100,000", "$31,400,000", "1.1%"],
        ["7", "1.5.1", "Hook-up & Commissioning Specialist Crew", "+$200,000", "$31,600,000", "2.2%"],
        ["8", "EAC_t", "Time Delay Overhead Spread (SPI_t = 0.9250)", "+$3,813,604", "$35,413,604", "42.8%"],
        ["END", "1.0", "Final Predicted Outturn Forecast (EAC)", "+$8,913,604", "$35,413,604", "100.0%"]
    ]
    
    t_wf = Table(wf_data, colWidths=[30, 45, 235, 90, 95, 45])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (3,0), (4,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 14))
    
    # SECTION 5: ACTIONABLE STEERING COMMITTEE DECISIONS
    story.append(Paragraph("5. Steering Committee Decision Matrix & Action Plan", h2_style))
    actions_p = "1. <b>Authorize +$8.91M Overrun Credit Line:</b> Executive approval required before September 15, 2026 to prevent yard shutdown in Month 9.<br/>" \
                "2. <b>Enforce Fixed-Fee Cap on Egersund Yard:</b> Transition remaining Derrick Mast welding hours to a fixed-fee labor cap.<br/>" \
                "3. <b>Compress Offshore Hook-up:</b> Recover 15 calendar days along the critical path to preserve the January 31, 2027 COD."
    story.append(Paragraph(actions_p, body_style))
    
    doc.build(story)
    print(f" [PASS] PDF report generated successfully at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
