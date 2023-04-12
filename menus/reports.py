import db_operations as db
from table_printer import print_table

from date_operations import get_current_datetime
from menus.competencies import view_all_competencies
from menus.users import view_all_users
from generate_pdf import user_competency_summary_to_pdf, competency_results_summary_to_pdf

def user_report(user: db.User):
    if user.user_type == db.UserTypes.manager:
        view_all_users()
        user_id = input("User ID: ") 
        user_to_report = db.read_user(user_id)
        if not user_to_report:
            print("User not found")
            return
    else:
        user_to_report = user
    user_summary = db.user_competency_report(user_to_report, include_null_results=True)
    fields = ["User ID", "User Name", "Competency Name", "Assessment Name", "Result ID", "Score", "Avg. Score", "Date Taken"]
    print()
    print_table(user_summary, fields)
    print()
    if user.user_type == db.UserTypes.user:
        return
    response = input("Do you want to save this report? (Y/N) ")
    print()
    if response.upper() == 'Y':
        export_report_options(\
            lambda: db.user_competency_summary_to_csv(user_to_report.user_id, user_summary, fields),\
            lambda: user_competency_summary_to_pdf(user_to_report.user_id, user_summary, fields))

def competency_report():
    view_all_competencies()
    competency_id = input("Competency ID: ")
    if not competency_id:
        return
    competency = db.read_competency(competency_id)
    if not competency:
        print("Competency not found")
        return
    competency_summary = db.competency_result_report(competency_id, include_null_results=True)
    fields = ["Competency ID", "Competency Name", "User Name", "Score", "Avg. Score", "Assessment Name", "Date Taken"]
    print_table(competency_summary, fields)
    response = input("\nDo you want to save this report? (Y/N) ")
    print()
    if response.upper() == 'Y':
        export_report_options(\
            lambda: db.competency_results_summary_to_csv(competency_id, competency_summary, fields),\
            lambda: competency_results_summary_to_pdf(competency_id, competency_summary, fields))

def export_report_options(export_to_csv, export_to_pdf):
    while True:
        print('''Save Report options

[1] Export to csv
[2] Save to PDF
[Q] Back to Reports''')
        report_option = input('>>> ')
        if report_option == '1':
            file_name = export_to_csv()
            print(f"Exported to '{file_name}'")
        elif report_option == '2':
            file_name = export_to_pdf()
            print(f"Saved to '{file_name}'")
        elif report_option.upper() == 'Q':
            break
        print()

def report_options(user: db.User):
    while True:
        print('''Reports

[1] User Competency summary
[2] Competency Results Summary
[Q] Back to Dashboard''')
        report_option = input('>>> ')

        if report_option == '1':
            user_report(user)
        elif report_option == '2':
            competency_report()
        elif report_option.upper() == 'Q':
            break
        print()