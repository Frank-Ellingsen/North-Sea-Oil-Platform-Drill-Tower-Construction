import asyncio
import os
import sys

# Ensure UTF-8 output encoding for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright

async def generate_pdf_reports():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(base_dir, "06_docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    html_path = os.path.join(base_dir, "index.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    print("=" * 80)
    print("Generating Professional PDF Reports for North Sea Drill Tower Construction...")
    print("=" * 80)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # -------------------------------------------------------------------------
        # REPORT 1: 1-Page Executive Steering Committee Briefing (PDF)
        # -------------------------------------------------------------------------
        page1 = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page1.goto(file_url, wait_until="networkidle")
        await page1.emulate_media(media="print")
        pdf1_path = os.path.join(docs_dir, "Executive_1Page_Steering_Status_Briefing.pdf")
        await page1.pdf(
            path=pdf1_path,
            format="A4",
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "10mm", "right": "10mm"}
        )
        print(f"✅ Generated: 06_docs/Executive_1Page_Steering_Status_Briefing.pdf")

        # -------------------------------------------------------------------------
        # REPORT 2: Full Web Dashboard Report (PDF)
        # -------------------------------------------------------------------------
        page2 = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page2.goto(file_url, wait_until="networkidle")
        await page2.emulate_media(media="screen")
        pdf2_path = os.path.join(docs_dir, "Drill_Tower_Full_EVM_Dashboard_Report.pdf")
        await page2.pdf(
            path=pdf2_path,
            format="A4",
            landscape=True,
            print_background=True,
            margin={"top": "8mm", "bottom": "8mm", "left": "8mm", "right": "8mm"}
        )
        print(f"✅ Generated: 06_docs/Drill_Tower_Full_EVM_Dashboard_Report.pdf")

        # -------------------------------------------------------------------------
        # REPORT 3: Comprehensive Multi-Tab Project Controller Report (PDF)
        # -------------------------------------------------------------------------
        # Create a dedicated styled single HTML compilation of all markdown reports for a multi-page PDF binder
        markdown_files = [
            ("Executive_1Page_Project_Status_Report.md", "1. Executive Steering Committee Status Briefing"),
            ("EVM_Final_Outcome_Predictions.md", "2. Earned Value & Outturn Predictions"),
            ("Monte_Carlo_P90_Risk_Analysis.md", "3. Monte Carlo Schedule & Cost Risk Analysis (P50 / P90)"),
            ("EVM_Variance_Explanations_and_Action_Plan.md", "4. EVM Variance Explanations & Corrective Action Audit"),
            ("Project_Burn_Rate_and_Runway_Analysis.md", "5. Monthly Cash Burn Speed & Budget Depletion (Burn Out)"),
            ("Project_Cost_Waterfall_Bridge.md", "6. Cost Variance Waterfall Bridge ($BAC to EAC)"),
            ("Project_Risk_Matrix_and_Register.md", "7. EPC Executive Risk Matrix & Mitigation Register"),
            ("Vertical_Swimlane_WBS_Breakdown.md", "8. Vertical Swimlane WBS Control Account Breakdown"),
            ("Project_Financial_Ratios_and_Appraisal.md", "9. Project Financial Metrics & Appraisal")
        ]

        compiled_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>North Sea Drill Tower Construction - Comprehensive EVM Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 11px; line-height: 1.5; color: #1F2937; padding: 20px; }
        h1 { font-size: 20px; font-weight: 700; color: #111827; border-bottom: 2px solid #111827; padding-bottom: 6px; margin-bottom: 16px; }
        h2 { font-size: 14px; font-weight: 700; color: #2563EB; border-bottom: 1px solid #E5E7EB; padding-bottom: 4px; margin-top: 24px; margin-bottom: 10px; page-break-before: always; }
        h2:first-of-type { page-break-before: avoid; }
        h3 { font-size: 12px; font-weight: 600; color: #374151; margin-top: 14px; margin-bottom: 6px; }
        p { margin-bottom: 8px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 14px; font-size: 10.5px; font-variant-numeric: tabular-nums; }
        th { background: #F3F4F6; text-align: left; padding: 6px 8px; font-weight: 600; color: #4B5563; border-bottom: 1.5px solid #111827; }
        td { padding: 6px 8px; border-bottom: 1px solid #E5E7EB; }
        tr:nth-child(even) td { background: #FAFAFA; }
        ul, ol { padding-left: 18px; margin-bottom: 10px; }
        li { margin-bottom: 4px; }
        .header-meta { display: flex; justify-content: space-between; font-size: 10px; color: #6B7280; border-bottom: 1px solid #E5E7EB; padding-bottom: 8px; margin-bottom: 20px; }
        .badge-red { background: #FEE2E2; color: #DC2626; padding: 2px 6px; border-radius: 2px; font-weight: 700; }
        .badge-amber { background: #FEF3C7; color: #D97706; padding: 2px 6px; border-radius: 2px; font-weight: 700; }
        .badge-green { background: #D1FAE5; color: #059669; padding: 2px 6px; border-radius: 2px; font-weight: 700; }
    </style>
</head>
<body>
    <h1>North Sea Oil Platform Drill Tower Construction</h1>
    <div class="header-meta">
        <span>Document ID: <strong>EVM-COMPREHENSIVE-REPORT-2026-M08</strong></span>
        <span>Status Date: <strong>August 31, 2026</strong></span>
        <span>Author: <strong>Frank Ellingsen, Lead Project Controller</strong></span>
    </div>
"""

        for filename, section_title in markdown_files:
            md_path = os.path.join(docs_dir, filename)
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Simple HTML formatting of markdown content
                compiled_html_content += f"<h2>{section_title}</h2>\n"
                
                lines = content.splitlines()
                in_table = False
                table_lines = []
                
                for line in lines:
                    line_str = line.strip()
                    if line_str.startswith("# "):
                        continue
                    elif line_str.startswith("## "):
                        compiled_html_content += f"<h3>{line_str[3:]}</h3>\n"
                    elif line_str.startswith("### "):
                        compiled_html_content += f"<h3>{line_str[4:]}</h3>\n"
                    elif line_str.startswith("|") and line_str.endswith("|"):
                        in_table = True
                        table_lines.append(line_str)
                    else:
                        if in_table:
                            # Render accumulated table
                            compiled_html_content += "<table>\n"
                            headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
                            compiled_html_content += "<thead><tr>" + "".join([f"<th>{h}</th>" for h in headers]) + "</tr></thead>\n<tbody>\n"
                            for row_str in table_lines[2:]:
                                cells = [c.strip() for c in row_str.strip("|").split("|")]
                                compiled_html_content += "<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>\n"
                            compiled_html_content += "</tbody></table>\n"
                            in_table = False
                            table_lines = []
                        
                        if line_str.startswith("- ") or line_str.startswith("* "):
                            compiled_html_content += f"<li>{line_str[2:]}</li>\n"
                        elif line_str:
                            compiled_html_content += f"<p>{line_str}</p>\n"
                
                if in_table and table_lines:
                    compiled_html_content += "<table>\n"
                    headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
                    compiled_html_content += "<thead><tr>" + "".join([f"<th>{h}</th>" for h in headers]) + "</tr></thead>\n<tbody>\n"
                    for row_str in table_lines[2:]:
                        cells = [c.strip() for c in row_str.strip("|").split("|")]
                        compiled_html_content += "<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>\n"
                    compiled_html_content += "</tbody></table>\n"

        compiled_html_content += "</body></html>"
        
        temp_html_path = os.path.join(docs_dir, "temp_comprehensive_report.html")
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(compiled_html_content)
            
        page3 = await browser.new_page()
        temp_url = f"file:///{temp_html_path.replace(os.sep, '/')}"
        await page3.goto(temp_url, wait_until="networkidle")
        pdf3_path = os.path.join(docs_dir, "North_Sea_Drill_Tower_EVM_Comprehensive_Report.pdf")
        await page3.pdf(
            path=pdf3_path,
            format="A4",
            print_background=True,
            margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"}
        )
        print(f"✅ Generated: 06_docs/North_Sea_Drill_Tower_EVM_Comprehensive_Report.pdf")
        
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

        await browser.close()
        print("\nAll PDF reports generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_pdf_reports())
