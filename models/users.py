from date_operations import to_date

class User:
    table_name = "Users"
    user_id = "user_id"
    first_name = "first_name"
    last_name = "last_name"
    phone = "phone"
    email = "email"
    password = "password"
    active = "active"
    date_created = "date_created"
    hire_date = "hire_date"
    user_type = "user_type"
    fields = (user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)

    def __init__(self, user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password
        self.active = active
        if type(date_created) == str:
            self.date_created = to_date(date_created)
        else:
            self.date_created = date_created
        if type(hire_date) == str:
            self.hire_date = to_date(hire_date)
        else:
            self.hire_date = hire_date
        self.user_type = user_type

    def __str__(self):
        return f'''User ID:      {self.user_id}
First Name:   {self.first_name}
Last Name:    {self.last_name}
Phone:        {self.phone}
Email:        {self.email}
Password:     {self.password}
Active:       {self.active}
Date Created: {self.date_created}
Hire Date:    {self.hire_date if self.hire_date else "NULL"}
User Type:    {self.user_type}'''
