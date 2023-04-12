import db_operations as db
from passwords import input_password

def edit_profile(user: db.User):
    print()
    while True:
        print("Profile:\n")
        print(user)
        print()
        print('''Editing options

[1] Change name
[2] Change phone
[3] Change email
[4] Change password
[Q] Back to Dashboard''')
        response = input('>>> ')
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
        elif response.upper() == 'Q':
            break
        try:
            db.update_user(user, change_password)
            db.commit()
        except Exception as e:
            print(e)
        print()