import db_operations as db

from date_operations import input_date
from table_printer import print_table

def create_competency() -> db.Competency:
    name = input("Competency Name (Enter to cancel): ")
    if not name:
        return None
    try:
        competency = db.create_competency_with_defaults(name)
        db.commit()
        return competency
    except Exception as e:
        print(e)

def view_all_competencies():
    competency_list = db.read_all_competencies()
    fields = ["Competency ID", "Name", "Creation Date"]
    print()
    print_table(competency_list, fields)
    print()

def update_competency():
    competency_id = input("Competency ID: ")
    if not competency_id:
        return
    print()
    competency = db.read_competency(competency_id)
    if not competency:
        print("Competency not found")
        return
    while True:
        print("\nCompetency Info:")
        print()
        print(competency)
        print()
        print(f'''Update Options

[1] Change Name
[2] Change creation date
[Q] Back to Competency Options''')
        response = input(">>> ")
        if response == '1':
            name = input("Name: ")
            if not name:
                continue
            competency.name = name
        elif response == '2':
            new_date = input_date("Date Created: ")
            if not new_date:
                continue
            competency.date_created = new_date
        elif response.upper() == 'Q':
            break
        try:
            db.update_competency(competency)
            db.commit()
        except Exception as e:
            print(e)
            competency = db.read_competency(competency.competency_id)

def competency_operations():
    print()
    while True:
        print('''-------------Competency Options-------------

[1] Create competency
[2] View all competencies
[3] Update competency
[Q] Back to Dashboard''')
        response = input(">>> ")
        
        if response == '1':
            competency = create_competency()
            if competency:
                print(f"Created competency '{competency.name}'")
            else:
                print("Cancelled competency")
        elif response == '2':
            view_all_competencies()
        elif response == '3':
            update_competency()
        elif response.upper() == 'Q':
            break
        print()