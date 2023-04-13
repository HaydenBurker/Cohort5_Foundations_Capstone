import db_operations as db
from fpdf import FPDF
from table_printer import get_column_sizes, format_rows

def print_table_to_pdf(pdf: FPDF, ln, rows, fields = None):
    width = 0
    height = 5
    if fields == None and len(rows) > 0:
        fields = [f'Field {i+1}' for i in range(len(rows[0]))]
    rows = format_rows(rows)
    column_sizes = get_column_sizes(rows, fields)

    text = "  "
    for i, field in enumerate(fields):
        column_size = column_sizes[i]
        text += f"{field:<{column_size}}  "
    pdf.cell(width, height, txt = text, ln = ln, align = 'C')
    ln += 1
    text = "  "
    
    for row in rows:
        row = list(row)
        for i, column_size in enumerate(column_sizes):
            text += f"{row[i]:<{column_size}}  "
        pdf.cell(width, height, txt = text, ln = ln, align = 'C')
        ln += 1
        text = "  "
    return ln


def user_competency_summary_to_pdf(user_id, user_summary, fields):
    pdf_name = f"{db.reports_export_path}{db.get_user_report_name(user_id)}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Cascadia Code", fname="fonts/CascadiaCode.ttf", uni=True)
    pdf.set_font("Cascadia Code", size = 15)
    pdf.cell(0, 15, txt = "User Competency Summary", ln = 1, align='C')
    pdf.set_font_size(6)
    ln = print_table_to_pdf(pdf, 2, user_summary, fields)
    pdf.output(pdf_name)
    return pdf_name

def competency_results_summary_to_pdf(competency_id, competency_summary, fields):
    pdf_name = f"{db.reports_export_path}{db.get_competency_report_name(competency_id)}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Cascadia Code", fname="fonts/CascadiaCode.ttf", uni=True)
    pdf.set_font("Cascadia Code", size = 15)
    pdf.cell(0, 15, txt = "Competency Results Summary", ln = 1, align='C')
    pdf.set_font_size(6)
    ln = print_table_to_pdf(pdf, 2, competency_summary, fields)
    pdf.output(pdf_name)
    return pdf_name