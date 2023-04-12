import db_operations as db

def csv_options(warning: bool):
    if warning:
        print('''Please be careful with your data!
Keep your export files safe.
Be careful importing files, the operation can't be undone once the data is imported.
Press Enter to continue''')
        input('>>> ')
    print()
    while True:
        print('''Import/export csv options

[1] Export users
[2] Export competencies
[3] Export assessments
[4] Export assessment results
[5] Import users
[6] Import competencies
[7] Import assessments
[8] Import assessment results
[Q] Return to dashboard''')
        response = input('>>> ')

        if response == '1':
            file_name = db.export_users_to_csv()
            print(f"Exported to '{file_name}'")
        elif response == '2':
            file_name = db.export_competencies_to_csv()
            print(f"Exported to '{file_name}'")
        elif response == '3':
            file_name = db.export_assessments_to_csv()
            print(f"Exported to '{file_name}'")
        elif response == '4':
            file_name = db.export_assessment_results_to_csv()
            print(f"Exported to '{file_name}'")
        elif response == '5':
            if db.check_users_import():
                print('''User import options (Enter to cancel)

[1] Hashed passwords
[2] Plaintext passwords

Be very careful here! Choosing the wrong option may require a password reset for all users!
''')
                user_option = input('>>> ')
                if user_option == '1':
                    users_imported = db.import_users_from_csv(True)
                elif user_option == '2':
                    users_imported = db.import_users_from_csv(False)
                else:
                    users_imported = False
                    print("Import cancelled")
                if users_imported:
                    print(f'Imported {db.users_csv_import_path}')
            else:
                print(f'{db.users_csv_import_path} not found')
        elif response == '6':
            if db.check_competencies_import():
                if db.import_competencies_from_csv():
                    print(f'Imported {db.competencies_csv_import_path}')
                else:
                    print(f'Failed to import {db.competencies_csv_import_path}')
            else:
                print(f'{db.competencies_csv_import_path} not found')
        elif response == '7':
            if db.check_assessments_import():
                if db.import_assessments_from_csv():
                    print(f'Imported {db.assessments_csv_import_path}')
                else:
                    print(f'Failed to import {db.assessments_csv_import_path}')
            else:
                print(f'{db.assessments_csv_import_path} not found')
        elif response == '8':
            if db.check_assessment_results_import():
                if db.import_assessment_results_from_csv():
                    print(f'Imported {db.assessment_results_csv_import_path}')
                else:
                    print(f'Failed to import {db.assessment_results_csv_import_path}')
            else:
                print(f'{db.assessment_results_csv_import_path} not found')
        elif response.upper() == 'Q':
            break
        print()
    