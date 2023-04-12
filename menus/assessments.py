import db_operations as db

from date_operations import input_date
from table_printer import print_table
from menus.competencies import view_all_competencies
from menus.users import view_all_users

def create_assessment() -> db.Assessment:
    view_all_competencies()
    competency_id = input("Competency ID (Enter to cancel): ")
    if not competency_id:
        return None
    competency = db.read_competency(competency_id)
    if competency == None:
        print("Competency not found")
        return None

    name = input("Assessment Name: ")
    if not name:
        return None
    try:
        assessment = db.create_assessment_with_defaults(competency_id, name)
        db.commit()
        return assessment
    except Exception as e:
        print(e)
        return None

def view_all_assessments():
    assessment_list = db.read_all_assessments_formatted()
    fields = ["Assessment ID", "Assessment Name", "Competency Name", "Creation Date"]
    print()
    print_table(assessment_list, fields)
    print()

def view_assessments_from_user():
    view_all_users()
    user_id = input("User ID: ")
    print()
    user = db.read_user(user_id)
    if not user:
        print("User not found")
        return
    assessments = db.read_assessments_from_user(user_id)
    fields = ["User Name", "Assessment ID", "Assessment Name", "Competency Name"]
    print_table(assessments, fields)
    print()

def update_assessment():
    assessment_id = input("Assessment ID: ")
    if not assessment_id:
        return
    assessment = db.read_assessment(assessment_id)
    if not assessment:
        print("\nAssessment not found")
        return
    while True:
        print("\nAssessment Info:")
        print()
        print(assessment)
        print()
        print(f'''Update Options

[1] Change name
[2] Change date created
[Q] Back to Assessment Options''')
        response = input(">>> ")
        if response == '1':
            name = input("Name: ")
            if not name:
                continue
            assessment.name = name
        if response == '2':
            new_date = input_date("Date Created: ")
            if not new_date:
                continue
            assessment.date_created = new_date
        elif response.upper() == 'Q':
            break
        try:
            db.update_assessment(assessment)
            db.commit()
        except Exception as e:
            print(e)
            assessment = db.read_assessment(assessment.assessment_id)

def assessment_operations():
    print()
    while True:
        print('''------------- Assessment Options -------------

[1] Create assessment
[2] View all assessments
[3] View assessments for a user
[4] Update assessment
[Q] Back to Dashboard''')
        response = input(">>> ")
        
        if response == '1':
            assessment = create_assessment()
            if assessment:
                print(f"Created assessment '{assessment.name}'")
            else:
                print("Cancelled assessment")
            print()
        elif response == '2':
            view_all_assessments()
        elif response == '3':
            view_assessments_from_user()
        elif response == '4':
            update_assessment()
            print()
        elif response.upper() == 'Q':
            break