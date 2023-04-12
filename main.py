import db_operations as db
from manager_menu import manager_menu
from passwords import input_password
from user_menu import user_menu

def login_if_manager_doesnt_exist() -> db.User:
    managers = db.read_all_managers()
    if managers:
        return None
    print("Welcome to the Competency Tracker!")
    print("Fill out the form below to create your account:\n")
    
    while True:
        first_name = input("First Name: ")
        if first_name:
            break

    while True:
        last_name = input("Last Name: ")
        if last_name:
            break

    while True:
        phone = input("Phone Number: ")
        if phone:
            break

    while True:
        email = input("Email: ")
        if email:
            break

    while True:
        password = input_password("Password: ")
        if password:
            break

    user_type = db.UserTypes.manager
    manager = db.create_user_with_defaults(first_name, last_name, phone, email, password, user_type)
    db.commit()
    return manager

def login():
    email = input('Email: ')
    password = input_password('Password: ')
    user, message = db.user_login(email, password)
    if not user:
        print(message)
    else:
        print(message)
        if user.user_type == db.UserTypes.manager:
            manager_menu(user)
        elif user.user_type == db.UserTypes.user:
            user_menu(user)

def main():
    manager = login_if_manager_doesnt_exist()
    
    if manager:
        manager_menu(manager)
        print()
        manager = None
    
    while True:
        print('''Competency Tracker Login Page

[L] Login
[Q] Quit''')
        response = input('''>>> ''').upper()
        if response == 'L':
            login()
        if response == 'Q':
            break
        print()

if __name__ == "__main__":
    db.connect()
    main()
    db.close()
