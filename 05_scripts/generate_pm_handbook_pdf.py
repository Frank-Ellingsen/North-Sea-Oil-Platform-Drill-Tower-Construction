"""
Generates a comprehensive PDF Handbook for Project Managers.
Synthesizes EVM theory, Earned Schedule, Monte Carlo risk simulation,
Commercial financial appraisal, Cash burn runway, Cost waterfall bridges,
and Risk Governance, using the Offshore EPC Platform Drill Tower Project as the primary case study.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "06_docs")
PDF_PATH = os.path.join(DOCS_DIR, "Project_Managers_EVM_and_Controlling_Handbook.pdf")

def build_handbook():
    print(f"--- Generating PDF Project Manager's Handbook: {PDF_PATH} ---")
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
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#111827'),
        alignment=1, # Center
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        alignment=1, # Center
        spaceAfter=15
    )
    ch_header_style = ParagraphStyle(
        'ChapterHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#111827'),
        spaceBefore=14,
        spaceAfter=8
    )
    h3_style = ParagraphStyle(
        'Heading3Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1F2937'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )
    formula_style = ParagraphStyle(
        'FormulaCustom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E40AF'),
        backColor=colors.HexColor('#EFF6FF'),
        borderColor=colors.HexColor('#BFDBFE'),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )
    case_study_style = ParagraphStyle(
        'CaseStudyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#111827'),
        backColor=colors.HexColor('#FEF2F2'),
        borderColor=colors.HexColor('#FCA5A5'),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )

    story = []
    
    # COVER / TITLE BLOCK
    story.append(Spacer(1, 15))
    story.append(Paragraph("PROJECT MANAGER'S HANDBOOK", title_style))
    story.append(Paragraph("Applied Earned Value Management, Commercial Capital Appraisal & Risk Governance", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#111827"), spaceAfter=15))
    
    meta_text = "<b>Author:</b> Frank Ellingsen, Financial Controller & Project Control Specialist<br/>" \
                "<b>Case Study Base:</b> Offshore EPC Platform Drill Tower Construction Project ($BAC = $26.50M)<br/>" \
                "<b>Target Audience:</b> Project Managers, Project Controllers, CFOs, Steering Committee Members"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 15))
    
    # TABLE OF CONTENTS / OVERVIEW
    story.append(Paragraph("Handbook Chapter Sitemap", ch_header_style))
    toc_data = [
        ["Chapter", "Core Focus & Methodological Scope", "Drill Tower Project Practical Case Study"],
        ["Chapter 1", "Principles of Earned Value Management (EVM)", "Month 8 EVM Status (CPI = 0.7483, SPI = 0.8556)"],
        ["Chapter 2", "Advanced Earned Schedule (ES) & Time-Based SPI(t)", "Lipke ES Calculation (ES = 7.40 Mo, SPI_t = 0.9250)"],
        ["Chapter 3", "Quantitative Risk Analysis (Monte Carlo QCRA/QSRA)", "10,000 Iterations (P90 EAC = $35.82M, +$401.5K Reserve)"],
        ["Chapter 4", "Commercial Capital Budgeting & Appraisal Ratios", "Commercial Appraisal (NPV = +$14.90M, IRR = 18.86%)"],
        ["Chapter 5", "Cash Burn Speed & Budget Depletion Runway", "Month 9 (September 2026) Budget Depletion Point"],
        ["Chapter 6", "Variance Reconciliation & Cost Waterfall Bridges", "Step-by-Step Bridge (BAC $26.50M -> EAC $35.41M)"],
        ["Chapter 7", "Risk Heatmaps & Executive Governance", "5x5 Risk Matrix & Active Register (R01-R05)"]
    ]
    t_toc = Table(toc_data, colWidths=[65, 235, 240])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_toc)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # CHAPTER 1: PRINCIPLES OF EVM
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 1: Principles of Earned Value Management (EVM)", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch1 = "Earned Value Management (EVM) is a systematic project management technique for measuring project " \
            "performance and progress by integrating Project Scope, Time Schedule, and Actual Cost metrics into a single " \
            "objective baseline. EVM establishes three foundational metrics at any given status date:"
    story.append(Paragraph(p_ch1, body_style))
    
    story.append(Paragraph("1. Core EVM Triad Definitions:", h3_style))
    story.append(Paragraph("• <b>Planned Value (PV):</b> The authorized budget assigned to scheduled work to be accomplished.", body_style))
    story.append(Paragraph("• <b>Earned Value (EV):</b> The measure of work performed expressed in terms of the budget authorized for that work.", body_style))
    story.append(Paragraph("• <b>Actual Cost (AC):</b> The realized cost incurred for work performed on an activity during a given time period.", body_style))
    
    story.append(Paragraph("2. Performance Formulas:", h3_style))
    form_ch1 = "Cost Variance (CV)         = EV - AC\n" \
               "Schedule Variance (SV)     = EV - PV\n" \
               "Cost Performance Index     = CPI = EV / AC\n" \
               "Schedule Performance Index = SPI = EV / PV\n" \
               "Estimate at Completion     = EAC = BAC / CPI\n" \
               "Variance at Completion     = VAC = BAC - EAC"
    story.append(Paragraph(form_ch1, formula_style))
    
    story.append(Paragraph("3. Drill Tower Case Study Application (Status Month 8):", h3_style))
    cs_ch1 = "<b>DRILL TOWER METRICS AT MONTH 8 (WEEK 36):</b><br/>" \
             "• Baseline Budget (BAC) = $26,500,000 | Planned Value (PV) = $20,500,000 (77.4% Planned)<br/>" \
             "• Earned Value (EV) = $17,540,000 (66.2% Complete) | Actual Cost (AC) = $23,440,000<br/>" \
             "• Cost Variance (CV) = $17.54M - $23.44M = -$5,900,000 (-33.6% Over budget)<br/>" \
             "• CPI Efficiency = $17.54M / $23.44M = <b>0.7483</b> (The project earns $0.75 of value for every $1.00 spent)<br/>" \
             "• Outturn Cost EAC = $26.50M / 0.7483 = <b>$35,413,604</b> (Predicted cost overrun: -$8,913,604)."
    story.append(Paragraph(cs_ch1, case_study_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 2: ADVANCED EARNED SCHEDULE (ES)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 2: Advanced Earned Schedule (ES) & Time-Based Performance", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch2 = "A classic limitation of traditional EVM is that Schedule Variance (SV = EV - PV) is measured in currency, " \
            "and as a project nears 100% completion, EV naturally converges to BAC, forcing SV -> 0 and SPI -> 1.0, " \
            "even if the project is months late! Earned Schedule (ES), developed by Walt Lipke, resolves this by translating " \
            "Earned Value into time units by identifying the exact calendar point where the current EV equaled planned baseline PV."
    story.append(Paragraph(p_ch2, body_style))
    
    story.append(Paragraph("1. Earned Schedule Formulas:", h3_style))
    form_ch2 = "Earned Schedule (ES)       = C + (EV - PV_C) / (PV_C+1 - PV_C)\n" \
               "Time Schedule Variance     = SV_t = ES - Actual Months (AT)\n" \
               "Time Performance Index     = SPI_t = ES / AT\n" \
               "Time Forecast Completion   = EAC_t = Planned Duration (PD) / SPI_t"
    story.append(Paragraph(form_ch2, formula_style))
    
    cs_ch2 = "<b>DRILL TOWER CASE STUDY APPLICATION:</b><br/>" \
             "• At Month 8 (AT = 8.0), Earned Value EV = $17.54M.<br/>" \
             "• Interpolating against baseline PV yields <b>Earned Schedule ES = 7.40 Months</b>.<br/>" \
             "• Time Schedule Variance SV_t = 7.40 - 8.00 = -0.60 Months = <b>-18.2 Days</b> delay.<br/>" \
             "• Time Velocity Index SPI_t = 7.40 / 8.00 = <b>0.9250</b>.<br/>" \
             "• Predicted Completion Date EAC_t = 12.0 / 0.9250 = <b>13.0 Months</b> (<b>January 31, 2027</b> / +31 days late)."
    story.append(Paragraph(cs_ch2, case_study_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 3: MONTE CARLO RISK SIMULATION (P90)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 3: Quantitative Schedule & Cost Risk Analysis (Monte Carlo QCRA/QSRA)", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch3 = "Deterministic single-point estimates ($EAC_1$) fail to account for risk uncertainty and task correlation. " \
            "Monte Carlo risk simulation executes 10,000 statistical iterations, sampling triangular risk distributions " \
            "(Optimistic, Most Likely, Pessimistic) across all WBS control accounts to generate cumulative probability distribution curves (S-Curves)."
    story.append(Paragraph(p_ch3, body_style))
    
    story.append(Paragraph("1. Drill Tower Monte Carlo Percentile Results (10,000 Iterations):", h3_style))
    
    mc_data = [
        ["Percentile", "Confidence Level", "Outturn Cost (EAC)", "Cost Overrun vs BAC", "Completion Date", "Contingency Reserve Needed"],
        ["P10", "10% Optimistic", "$32,444,302", "-$5,944,302", "Feb 13, 2027", "$0.00"],
        ["P50", "50% Median Outturn", "$34,060,783", "-$7,560,783", "Feb 27, 2027", "$0.00"],
        ["P80", "80% Standard Budget", "$35,195,026", "-$8,695,026", "Mar 09, 2027", "$0.00"],
        ["P90", "90% High Confidence", "$35,815,202", "-$9,315,202", "Mar 14, 2027", "+$401,598 Reserve"],
        ["P95", "95% Extreme Risk", "$36,272,986", "-$9,772,986", "Mar 18, 2027", "+$859,382 Reserve"]
    ]
    t_mc = Table(mc_data, colWidths=[60, 100, 105, 105, 80, 90])
    t_mc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7F1D1D')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')]),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#FEF2F2'))
    ]))
    story.append(t_mc)
    story.append(Spacer(1, 10))
    
    cs_ch3 = "<b>P90 CONTINGENCY RESERVE RULE:</b><br/>" \
             "To achieve 90% confidence of completing within approved capital limits, project controllers must provision " \
             "a total outturn budget of <b>$35,815,202</b>, requiring a management risk contingency reserve of <b>+$401,598</b> above the base EAC."
    story.append(Paragraph(cs_ch3, case_study_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 4: COMMERCIAL CAPITAL BUDGETING
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 4: Commercial Capital Budgeting & Investment Appraisal", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch4 = "Project Controllers must evaluate project cost overruns against commercial hurdle rates. " \
            "Using Discounted Cash Flow (DCF) techniques under a 10.0% WACC discount rate, we evaluate commercial viability."
    story.append(Paragraph(p_ch4, body_style))
    
    form_ch4 = "Net Present Value (NPV) = Sum [ CashFlow_t / (1 + r)^t ] - Outturn_CAPEX\n" \
               "Internal Rate of Return = IRR where NPV = 0\n" \
               "Profitability Index     = PI = PV of Inflows / Outturn_CAPEX"
    story.append(Paragraph(form_ch4, formula_style))
    
    cs_ch4 = "<b>DRILL TOWER COMMERCIAL APPRAISAL RESULTS:</b><br/>" \
             "• Outturn CAPEX ($EAC) = $35,413,604 | Operating Cash Flow = $8.00M/year for 10 years<br/>" \
             "• <b>Net Present Value (NPV @ 10% WACC)</b> = <b>+$14,899,563</b> (Generates +$14.90M net wealth above hurdle)<br/>" \
             "• <b>Internal Rate of Return (IRR)</b> = <b>18.86%</b> (Exceeds 10.0% hurdle rate by +886 bps)<br/>" \
             "• <b>Simple Payback Period</b> = <b>4.43 Years</b> (53.1 Months / May 2031)<br/>" \
             "• <b>Profitability Index (PI)</b> = <b>1.42</b> (Generates $1.42 PV per $1.00 spent)."
    story.append(Paragraph(cs_ch4, case_study_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 5: CASH BURN SPEED & RUNWAY
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 5: Cash Burn Speed & Budget Depletion Runway Analysis", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    cs_ch5 = "<b>BUDGET DEPLETION RUNWAY FINDINGS:</b><br/>" \
             "• Average Monthly Burn Speed = <b>$2,930,000 / month</b> (vs planned $2.56M/month).<br/>" \
             "• Remaining Baseline Capital at Month 8 = <b>$3,060,000</b>.<br/>" \
             "• <b>100% BUDGET BURN OUT POINT:</b> The baseline budget ($BAC = $26.50M) will be completely exhausted in <b>Month 9 (September 2026)</b> ($AC_{\\text{cum}} = \\$26.64\\text{M}$).<br/>" \
             "• <b>Executive Directive:</b> Secure C-suite approval for a <b>+$8.91M overrun credit line</b> before September 15, 2026."
    story.append(Paragraph(cs_ch5, case_study_style))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CHAPTER 6: VARIANCE RECONCILIATION & WATERFALL BRIDGES
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 6: Variance Reconciliation & Cost Waterfall Bridges", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch6 = "A Cost Variance Waterfall Bridge reconciles the step-by-step progression from the original $BAC$ budget " \
            "to the final outturn $EAC$ forecast, isolating scope overruns and time delay overhead extensions."
    story.append(Paragraph(p_ch6, body_style))
    
    wf_data = [
        ["Step", "WBS Code", "Control Account / Driver", "Incremental Cost", "Cumulative Cost", "% Share"],
        ["0", "1.0", "Baseline Budget (BAC)", "$26,500,000", "$26,500,000", "0.0%"],
        ["1", "1.1.1", "Detail Structural Engineering Revisions", "+$300,000", "$26,800,000", "3.4%"],
        ["2", "1.2.1", "Procurement Steel Inflation", "+$600,000", "$27,400,000", "6.7%"],
        ["3", "1.3.1", "Verdal Sub-Structure Fabrication", "+$200,000", "$27,600,000", "2.2%"],
        ["4", "1.3.2", "Egersund Derrick Mast Yard Rework", "+$2,400,000", "$30,000,000", "26.9%"],
        ["5", "1.4.1", "Heavy Lift Vessel Weather Standby", "+$1,300,000", "$31,300,000", "14.6%"],
        ["6", "1.4.2", "Offshore Topside Lifting & Mating", "+$100,000", "$31,400,000", "1.1%"],
        ["7", "1.5.1", "Hook-up & Commissioning Crew", "+$200,000", "$31,600,000", "2.2%"],
        ["8", "EAC_t", "Time Delay Overhead Spread (SPI_t)", "+$3,813,604", "$35,413,604", "42.8%"],
        ["END", "1.0", "Final Outturn Forecast (EAC)", "+$8,913,604", "$35,413,604", "100.0%"]
    ]
    t_wf = Table(wf_data, colWidths=[30, 45, 235, 90, 95, 45])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CHAPTER 7: RISK MATRIX & EXECUTIVE GOVERNANCE
    # -------------------------------------------------------------------------
    story.append(Paragraph("Chapter 7: Risk Heatmaps & Executive Governance Matrix", ch_header_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2563EB"), spaceAfter=8))
    
    p_ch7 = "Risk heatmaps combine Probability (1-5) and Impact (1-5) to prioritize active risk exposure. " \
            "Expected Monetary Value ($EMV = \\text{Probability} \\times \\text{Financial Exposure}$) quantifies unmitigated risk reserves."
    story.append(Paragraph(p_ch7, body_style))
    
    risk_data = [
        ["Risk ID", "Risk Title", "Category", "Score", "Exposure", "EMV Value", "Accountable CAM"],
        ["R01", "Egersund Derrick Mast Yard Rework", "Fabrication", "5x5 Critical", "$2,400,000", "$2,400,000", "Lars Hansen"],
        ["R02", "North Sea Weather Standby Delay", "Marine", "4x4 High", "$1,800,000", "$720,000", "Erik Solberg"],
        ["R03", "Tubular Steel Price Inflation", "Procurement", "3x3 Medium", "$600,000", "$180,000", "Ingrid Berg"],
        ["R04", "DNV Structural Redesign Review", "Engineering", "2x3 Medium", "$300,000", "$60,000", "Geir Nilsen"],
        ["R05", "Offshore Hook-up Crew Bottleneck", "Commissioning", "2x2 Low", "$200,000", "$40,000", "Bjørn Lie"]
    ]
    t_risk = Table(risk_data, colWidths=[45, 185, 75, 65, 80, 75, 80])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F2937')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F9FAFB')])
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 14))
    
    # SIGN-OFF BLOCK
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#111827"), spaceAfter=8))
    sign_text = "<b>HANDBOOK SIGN-OFF & METHODOLOGICAL AUTHORSHIP:</b><br/>" \
                "Prepared by Frank Ellingsen, Financial Controller & Project Control Specialist.<br/>" \
                "Validated against EVM standards, Lipke Earned Schedule algorithms, and commercial WACC investment principles."
    story.append(Paragraph(sign_text, body_style))
    
    doc.build(story)
    print(f" [PASS] PDF Handbook generated successfully at: {PDF_PATH}")

if __name__ == "__main__":
    build_handbook()
