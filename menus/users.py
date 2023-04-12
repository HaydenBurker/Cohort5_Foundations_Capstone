import db_operations as db

from date_operations import input_date
from passwords import input_password
from table_printer import print_table
from manager_menu import edit_profile

def create_user() -> db.User:
    first_name = input("First Name (Enter to cancel): ")
    if not first_name:
        return None
    last_name = input("Last Name: ")
    if not last_name:
        return None
    phone = input("Phone Number: ")
    if not phone:
        return None
    email = input("Email: ")
    if not email:
        return None
    password = input_password("Password: ")
    if not password:
        return None
    user_type = db.UserTypes.user
    try:
        user = db.create_user_with_defaults(first_name, last_name, phone, email, password, user_type)
        db.commit()
        return user
    except Exception as e:
        print(e)
        return None

def view_all_users():
    user_list = db.read_all_users()
    fields = ["User ID", "First Name", "Last Name", "Phone Number", "Email", "Password", "Active", "Creation Date", "Hire Date", "User Type"]
    print()
    print_table(user_list, fields)
    print()

def update_user(manager: db.User):
    user_id = input("User ID: ")
    if not user_id:
        return
    user = db.read_user(user_id)
    if not user:
        print("\nUser not found")
        return
    if user.user_id == manager.user_id:
        edit_profile(manager, back_message="Back to User Options")
        return
    while True:
        print("\nUser Info:")
        print()
        print(user)
        print()
        print(f'''Update Options

[1] Change Name
[2] Change phone number
[3] Change email
[4] Change password
[5] Change Hire date
[6] Change type to {db.UserTypes.user if user.user_type == db.UserTypes.manager else db.UserTypes.manager}
[7] {"Activate" if user.active == 0 else "Deactivate"} {user.user_type}
[Q] Back to User Options''')
        response = input(">>> ")

        change_password = False
        if response == '1':
            first_name = input("First Name: ")
            if not first_name:
                continue
            last_name = input("Last Name: ")
            if not last_name:
                continue
            user.first_name = first_name
            user.last_name = last_name

        elif response == '2':
            phone = input("Phone Number: ")
            if not phone:
                continue
            user.phone = phone

        elif response == '3':
            email = input("Email: ")
            if not email:
                continue
            user.email = email

        elif response == '4':
            password = input_password("Password: ")
            if not password:
                continue
            user.password = password
            change_password = True

        elif response == '5':
            hire_date = input_date("Hire Date: ")
            if not hire_date:
                continue
            user.hire_date = hire_date

        elif response == '6':
            if user.user_type == db.UserTypes.user:
                user.user_type = db.UserTypes.manager
            else:
                user.user_type = db.UserTypes.user

        elif response == '7':
            user.active = 1 if user.active == 0 else 0
        elif response.upper() == 'Q':
            break

        try:
            db.update_user(user, change_password)
            db.commit()
        except Exception as e:
            print(e)
            user = db.read_user(user.user_id)


def user_operations(manager):
    print()
    while True:
        print('''------------- User Options -------------

[1] Create user
[2] View all users
[3] Update user
[Q] Back to Dashboard''')
        response = input(">>> ")
        
        if response == '1':
            user = create_user()
            if user:
                print(f"Created user '{user.first_name} {user.last_name}'")
            else:
                print("Cancelled user")
            print()
        elif response == '2':
            view_all_users()
        elif response == '3':
            update_user(manager)
            print()
        elif response.upper() == 'Q':
            break