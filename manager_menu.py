import db_operations as db
from menus.profile import edit_profile
from menus.reports import report_options
from menus.users import user_operations
from menus.competencies import competency_operations
from menus.assessments import assessment_operations
from menus.assessment_results import assessment_result_operations
from menus.csv_options import csv_options


def manager_menu(manager: db.User):
    print("Logged in as manager")
    print(f"Welcome {manager.first_name} {manager.last_name}")
    csv_warning = True
    print()
    while True:
        print('''------------- Manager Dashboard -------------

[1] Edit profile
[2] User options
[3] Competency options
[4] Assessment options
[5] Assessment result options
[6] Reports
[7] Import/export csv options
[Q] Logout''')
        response = input(">>> ")
        if response == '1':
            edit_profile(manager, back_message="Back to Dashboard")
        if response == '2':
            user_operations(manager)
        elif response == '3':
            competency_operations()
        elif response == '4':
            assessment_operations()
        elif response == '5':
            assessment_result_operations(manager)
        elif response == '6':
            report_options(manager)
        elif response == '7':
            csv_options(csv_warning)
            csv_warning = False
        elif response.upper() == 'Q':
            break
        print()
    print("Logging out")
