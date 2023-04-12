import db_operations as db
from menus.reports import user_report
from menus.profile import edit_profile

def user_menu(user: db.User):
    print("Logged in as user")
    print(f"Welcome {user.first_name} {user.last_name}")
    while True:
        print('''------------- User Dashboard -------------

[1] Edit profile
[2] View assessment results
[Q] Logout''')
        response = input('>>> ')
        if response == '1':
            edit_profile(user, back_message="Back to Dashboard")
        elif response == '2':
            user_report(user)
        elif response.upper() == 'Q':
            break
    print("Logging out")