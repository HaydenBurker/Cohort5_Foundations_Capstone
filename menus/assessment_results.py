import db_operations as db

from date_operations import get_current_datetime, input_datetime
from table_printer import print_table

from menus.users import view_all_users
from menus.assessments import view_all_assessments

def check_score(score: str):
    if not score.isnumeric():
        return False
    score = int(score)
    if score < 0 or score > 4:
        return False
    return True

def manager_id_options(manager: db.User):
    while True:
        print('''Manager ID Options (Enter to cancel)

[1] Select from list of users
[2] Select yourself
[3] Select no one''')
        manager_id_option = input('>>> ')
        if not manager_id_option:
            return ''
        elif manager_id_option == '1':
            view_all_users()
            return input("Manager ID: ")
        elif manager_id_option == '2':
            return manager.user_id
        elif manager_id_option == '3':
            return None

def create_assessment_result(manager: db.User) -> db.AssessmentResult:
    view_all_users()
    user_id = input("User ID (Enter to cancel): ")
    if not user_id:
        return None
    user = db.read_user(user_id)
    if not user:
        print("User not found")
        return None
    view_all_assessments()
    assessment_id = input("Assessment ID: ")
    if not assessment_id:
        return None
    assessment = db.read_assessment(assessment_id)
    if not assessment:
        print("Assessment not found")
        return None
    manager_id = manager_id_options(manager)
    if manager_id == "":
        return None
    manager = db.read_user(manager_id)
    if not manager and manager_id != None:
        print("Manager not found")
        return None
    while True:
        score = input("Score: ")
        if not score:
            return None
        if not check_score(score):
            print("Enter a whole number between 0 and 4")
        else:
            break
    date_taken = get_current_datetime()
    
    try:
        assessment_result = db.create_assessment_result(None, user_id, assessment_id, manager_id, score, date_taken)
        db.commit()
        return assessment_result
    except Exception as e:
        print(e)
        return None

def view_all_assessment_results():
    assessment_result_list = db.read_all_assessment_results_formatted()
    fields = ["Result ID", "User Name", "Assessment Name", "Competency Name", "Manager Name", "Score", "Date Taken"]
    print()
    print_table(assessment_result_list, fields)
    print()

def update_assessment_result():
    result_id = input("Result ID: ")
    if not result_id:
        return
    print()
    assessment_result = db.read_assessment_result(result_id)
    if not assessment_result:
        print("Assessment result not found")
        return
    while True:
        print("\nAssessment Result Info:")
        print()
        print(assessment_result)
        print()
        print(f'''Update Options

[1] Change score
[2] Change date taken
[3] Delete result
[Q] Back To Assessment Result Options''')
        response = input(">>> ")
        if response == '1':
            while True:
                score = input("Score: ")
                if not score:
                    break
                if not check_score(score):
                    print("Enter a whole number between 0 and 4")
                    continue
                assessment_result.score = score
                break
        elif response == '2':
            new_date = input_datetime("Date Taken: ")
            if not new_date:
                continue
            assessment_result.date_taken = new_date
        elif response == '3':
            db.delete_assessment_result(assessment_result)
            print("Assessment result has been removed! Returning to dashboard.")
            break
        elif response.upper() == 'Q':
            break


        try:
            db.update_assessment_result(assessment_result)
            db.commit()
        except Exception as e:
            print(e)
            assessment_result = db.read_assessment_result(assessment_result.result_id)


def assessment_result_operations(manager):
    print()
    while True:
        print('''-------------Assessment Result Options-------------

[1] Create assessment result
[2] View all assessment results
[3] Update assessment result
[Q] Back to Dashboard''')
        response = input(">>> ")
        
        if response == '1':
            assessment_result = create_assessment_result(manager)
            if assessment_result:
                print("Created assessment result")
            else:
                print("Cancelled assessment result")
        elif response == '2':
            view_all_assessment_results()
        elif response == '3':
            update_assessment_result()
        elif response.upper() == 'Q':
            break
        print()