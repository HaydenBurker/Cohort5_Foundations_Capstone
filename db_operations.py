import csv
import os
import sqlite3

from passwords import hash_password, check_password
from date_operations import get_current_date, get_current_datetime
from models.users import User
from models.competencies import Competency
from models.assessments import Assessment
from models.assessment_results import AssessmentResult


def create_db():
    print("Building tables...")
    with open("models/schema.sql") as my_queries:
        queries = my_queries.read()
    cursor.executescript(queries)
    users_file_exists = check_users_import()
    competencies_file_exists = check_competencies_import()
    assessments_file_exists = check_assessments_import()
    assessment_results_file_exists = check_assessment_results_import()
    if True in [users_file_exists, competencies_file_exists, assessments_file_exists, assessment_results_file_exists]:
        import_option = input("Import files found. Do you want to add them to the database? (y/n): ")
        if import_option.upper() != 'Y':
            return

    if users_file_exists:
        print('''users.csv found. Here are the import options

[1] Hashed passwords
[2] Plaintext passwords

If logins fail: close app, delete 'competency_tracker.db' in the database folder, and try again with the other option
''')
        while True:
            user_option = input('>>> ')
            if user_option == '1':
                users_imported = import_users_from_csv(True)
            elif user_option == '2':
                users_imported = import_users_from_csv(False)
            else:
                print("Enter '1' or '2'")
                continue
            break
        if not users_imported:
            print(f'Failed to import {users_csv_import_path}')

    if competencies_file_exists:
        print(f'Importing {competencies_csv_import_path}')
        if not import_competencies_from_csv():
            print(f'Failed to import {competencies_csv_import_path}')

    if assessments_file_exists:
        print(f'Importing {assessments_csv_import_path}')
        if not import_assessments_from_csv():
            print(f'Failed to import {competencies_csv_import_path}')
            
    if assessment_results_file_exists:
        print(f'Importing {assessment_results_csv_import_path}')
        if not import_assessment_results_from_csv():
            print(f'Failed to import {competencies_csv_import_path}')

def file_exists(path):
    return os.path.isfile(path)


connection: sqlite3.Connection = None
cursor: sqlite3.Cursor = None
def connect():
    print("Connecting to database...")
    global connection, cursor
    database_path = "database/competency_tracker.db"
    database_exists = file_exists(database_path)
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    if not database_exists:
        print("Database not found! Creating a new one...")
        create_db()
    print("Done!\n\n")

def close():
    connection.close()

# -------------------  User Operations  -------------------
class UserTypes:
    user = "user"
    manager = "manager"

def user_login(email, password) -> tuple[User, str]:
    query = '''SELECT * FROM Users WHERE email = ?'''
    user_password_message = "Incorrect Username of Password"

    result = cursor.execute(query, (email,)).fetchone()
    if not result:
        return None, user_password_message
    user = User(*result)
    if not check_password(password, user.password):
        return None, user_password_message

    if user.active == 0:
        return None, "Your account is inactive"
    else:
        return user, "Logging in"

def create_user_with_defaults(first_name, last_name, phone, email, password, user_type) -> User:
    active = 1
    date_created = get_current_date()
    hire_date = None
    return create_user(None, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)

def create_user(user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type, password_hashed = False):
    if not password_hashed:
        password = hash_password(password)
    if not user_type in [UserTypes.user, UserTypes.manager]:
        raise ValueError(f"Invalid user type: {user_type}")
    query = '''Insert INTO Users (user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    fields = (user_id, first_name, last_name, phone, email, password, active, date_created, hire_date, user_type)
    id = cursor.execute(query, fields).lastrowid
    return User(id, *fields[1:])

def read_user(user_id) -> User:
    query = '''SELECT * FROM Users WHERE user_id = ?'''
    result = cursor.execute(query, (user_id,)).fetchone()
    if result:
        return User(*result)
    return None

def read_all_users() -> list[tuple]:
    query = '''SELECT * FROM Users'''
    users = cursor.execute(query).fetchall()
    return users

def read_all_managers() -> list[tuple]:
    query = '''SELECT * FROM Users WHERE user_type = ?'''
    managers = cursor.execute(query, (UserTypes.manager,)).fetchall()
    return managers

def update_user(user: User, change_password = False):
    query = '''UPDATE Users
SET first_name = ?, last_name = ?, phone = ?, email = ?, password = ?, active = ?, date_created = ?, hire_date = ?, user_type = ?
WHERE user_id = ?'''
    if change_password:
        user.password = hash_password(user.password)
    fields = (user.first_name, user.last_name, user.phone, user.email, user.password, user.active, user.date_created, user.hire_date, user.user_type, user.user_id)
    cursor.execute(query, fields)


# -------------------  Competency Operations  -------------------

def create_competency_with_defaults(name) -> Competency:
    date_created = get_current_date()
    return create_competency(None, name, date_created)

def create_competency(competency_id, name, date_created):
    query = '''INSERT INTO Competencies (competency_id, name, date_created)
VALUES (?, ?, ?)'''
    competency_id = cursor.execute(query, (competency_id, name, date_created)).lastrowid
    return Competency(competency_id, name, date_created)

def read_competency(competency_id) -> Competency:
    query = '''SELECT * FROM Competencies WHERE competency_id = ?'''
    result = cursor.execute(query, (competency_id,)).fetchone()
    if result:
        return Competency(*result)
    return None

def read_all_competencies() -> list[tuple]:
    query = '''SELECT * FROM Competencies'''
    competencies = cursor.execute(query).fetchall()
    return competencies

def update_competency(competency: Competency):
    query = '''UPDATE Competencies SET name = ?, date_created = ? WHERE competency_id = ?'''
    fields = (competency.name, competency.date_created, competency.competency_id)
    cursor.execute(query, fields)


# -------------------  Assessment Operations  -------------------

def create_assessment_with_defaults(competency_id, name) -> Assessment:
    date_created = get_current_date()
    return create_assessment(None, competency_id, name, date_created)

def create_assessment(assessment_id, competency_id, name, date_created):
    query = '''INSERT INTO Assessments (assessment_id, competency_id, name, date_created)
VALUES (?, ?, ?, ?)'''
    assessment_id = cursor.execute(query, (assessment_id, competency_id, name, date_created)).lastrowid
    return Assessment(assessment_id, competency_id, name, date_created)

def read_assessment(assessment_id) -> Assessment:
    query = '''SELECT * FROM Assessments WHERE assessment_id = ?'''
    result = cursor.execute(query, (assessment_id,)).fetchone()
    if result:
        return Assessment(*result)
    return None

def read_assessments_from_user(user_id) -> list[tuple]:
    query = '''SELECT u.first_name, u.last_name, a.assessment_id, a.name, c.name
FROM Assessments AS a
JOIN Competencies AS c ON c.competency_id = a.competency_id
JOIN Assessment_Results AS ar ON ar.assessment_id = a.assessment_id
JOIN Users AS u ON u.user_id = ar.user_id
WHERE u.user_id = ?
GROUP BY a.assessment_id'''
    assessments = cursor.execute(query, (user_id,)).fetchall()
    assessments = [(f'{a[0]} {a[1]}', a[2], a[3], a[4]) for a in assessments]
    return assessments

def read_all_assessments() -> list[tuple]:
    query = '''SELECT * FROM Assessments'''
    assessments = cursor.execute(query).fetchall()
    return assessments

def read_all_assessments_formatted() -> list[tuple]:
    query = '''SELECT a.assessment_id, a.name, c.name, a.date_created FROM Assessments AS a
JOIN Competencies AS c ON a.competency_id = c.competency_id'''
    assessments = cursor.execute(query).fetchall()
    return assessments

def update_assessment(assessment: Assessment):
    query = '''UPDATE Assessments SET competency_id = ?, name = ?, date_created = ? WHERE assessment_id = ?'''
    fields = (assessment.competency_id, assessment.name, assessment.date_created, assessment.assessment_id)
    cursor.execute(query, fields)


# -------------------  Assessment Result Operations  -------------------

def create_assessment_result(result_id, user_id, assessment_id, manager_id, score, date_taken) -> AssessmentResult:
    query = '''INSERT INTO Assessment_Results (result_id, user_id, assessment_id, manager_id, score, date_taken)
VALUES (?, ?, ?, ?, ?, ?)'''
    result_id = cursor.execute(query, (result_id, user_id, assessment_id, manager_id, score, date_taken)).lastrowid
    return AssessmentResult(result_id, user_id, assessment_id, manager_id, score, date_taken)

def read_assessment_result(assessment_id) -> AssessmentResult:
    query = '''SELECT * FROM Assessment_Results WHERE result_id = ?'''
    result = cursor.execute(query, (assessment_id,)).fetchone()
    if result:
        return AssessmentResult(*result)
    return None

def read_all_assessment_results() -> list[AssessmentResult] | list[tuple]:
    query = '''SELECT * FROM Assessment_Results'''
    assessment_results = cursor.execute(query).fetchall()
    return assessment_results

def read_all_assessment_results_formatted() -> list[tuple]:
    query = '''SELECT ar.result_id, u.first_name, u.last_name, a.name, c.name, m.first_name, m.last_name, ar.score, ar.date_taken FROM Assessment_Results AS ar
JOIN Assessments AS a ON ar.assessment_id = a.assessment_id
JOIN Competencies AS c ON a.competency_id = c.competency_id
JOIN Users AS u ON ar.user_id = u.user_id
LEFT OUTER JOIN Users AS m ON ar.manager_id = m.user_id'''
    assessment_results = cursor.execute(query).fetchall()
    assessment_results = [(ar[0], f'{ar[1]} {ar[2]}', ar[3], ar[4], f'{ar[5]} {ar[6]}' if ar[5] != None and ar[6] != None else None, ar[7], ar[8]) for ar in assessment_results]
    return assessment_results

def update_assessment_result(assessment_result: AssessmentResult):
    query = '''UPDATE Assessment_Results SET user_id = ?, assessment_id = ?, manager_id = ?, score = ?, date_taken = ? WHERE result_id = ?'''
    fields = (assessment_result.user_id, assessment_result.assessment_id, assessment_result.manager_id, assessment_result.score, assessment_result.date_taken, assessment_result.result_id)
    cursor.execute(query, fields)

def delete_assessment_result(assessment_result: AssessmentResult):
    query = '''DELETE FROM Assessment_Results WHERE result_id = ?'''
    id = assessment_result.result_id
    cursor.execute(query, (id,))

def commit():
    connection.commit()

def rollback():
    connection.rollback()




# -------------------  Reports  -------------------

def user_competency_report(user: User, include_null_results: bool):
    if include_null_results:
        query = '''SELECT u.user_id, u.first_name, u.last_name, c.name, a.name, a.result_id, a.score, AVG(a.score), a.date_taken
FROM Competencies AS c
LEFT OUTER JOIN (
    SELECT a.competency_id, a.name, ar.result_id, ar.score, ar.user_id, ar.date_taken FROM Assessment_Results AS ar
    JOIN Assessments as a ON ar.assessment_id = a.assessment_id
    WHERE ar.user_id = ?
) AS a ON a.competency_id = c.competency_id
LEFT OUTER JOIN Users AS u ON a.user_id = u.user_id
WHERE u.user_id = ? OR u.user_id IS NULL
GROUP BY u.user_id, c.competency_id
HAVING date_taken = MAX(date_taken) OR date_taken IS NULL
ORDER BY LOWER(c.name)'''
        report = cursor.execute(query, (user.user_id, user.user_id)).fetchall()
    else:
        query = '''SELECT u.user_id, u.first_name, u.last_name, c.name, a.name, ar.result_id, ar.score, AVG(ar.score), ar.date_taken
FROM Competencies AS c
JOIN Assessments as a ON a.competency_id = c.competency_id
JOIN Assessment_Results AS ar ON ar.assessment_id = a.assessment_id
JOIN Users AS u ON ar.user_id = u.user_id
WHERE u.user_id = ?
GROUP BY u.user_id, c.competency_id
HAVING date_taken = MAX(date_taken) OR date_taken IS NULL
ORDER BY LOWER(c.name)'''
        report = cursor.execute(query, (user.user_id,)).fetchall()
    report = [(r[0], f'{r[1]} {r[2]}' if r[1] and r[2] else None, r[3], r[4], r[5], r[6], r[7], r[8]) for r in report]
    return report

def competency_result_report(competency_id, include_null_results: bool):
    if include_null_results:
        query = '''SELECT c.competency_id, c.name, u.first_name, u.last_name, ar.score, ar.name, ar.date_taken
FROM Users AS u
LEFT OUTER JOIN (
    SELECT ar.user_id, ar.score, a.name, ar.date_taken, a.competency_id FROM Assessment_Results AS ar
    JOIN Assessments AS a ON a.assessment_id = ar.assessment_id
    WHERE a.competency_id = ?
) AS ar ON ar.user_id = u.user_id
LEFT OUTER JOIN Competencies AS c ON c.competency_id = ar.competency_id
WHERE u.active = 1
GROUP BY u.user_id, c.competency_id
HAVING date_taken = MAX(date_taken) OR date_taken IS NULL
ORDER BY LOWER(u.first_name), LOWER(u.last_name)'''
    else:
        query = '''SELECT c.competency_id, c.name, u.first_name, u.last_name, ar.score, a.name, ar.date_taken
FROM Users AS u
JOIN Assessment_Results AS ar ON ar.user_id = u.user_id
JOIN Assessments AS a ON a.assessment_id = ar.assessment_id
JOIN Competencies AS c ON c.competency_id = a.competency_id
WHERE c.competency_id = ? AND u.active = 1
GROUP BY u.user_id, c.competency_id
HAVING date_taken = MAX(date_taken) OR date_taken IS NULL
ORDER BY LOWER(u.first_name), LOWER(u.last_name)'''

    report = cursor.execute(query, (competency_id,)).fetchall()
    total_score = sum([int(r[4]) if r[4] else 0 for r in report])
    report_len = len(report) - sum([0 if r[0] else 1 for r in report])
    avg_score = total_score / report_len if report_len > 0 else 0.0
    report = [(r[0], r[1], f'{r[2]} {r[3]}', r[4], avg_score, r[5], r[6]) for r in report]
    return report


# -------------------  CSV Operations  -------------------

csv_table_export_path = "csv/exports/"
csv_table_import_path = "csv/imports/"
reports_export_path = "reports/"

users_csv_import_path = f"{csv_table_import_path}{User.table_name.lower()}.csv"
competencies_csv_import_path = f"{csv_table_import_path}{Competency.table_name.lower()}.csv"
assessments_csv_import_path = f"{csv_table_import_path}{Assessment.table_name.lower()}.csv"
assessment_results_csv_import_path = f"{csv_table_import_path}{AssessmentResult.table_name.lower()}.csv"

def export_to_csv(file_name, rows, fields):
    with open(file_name, 'w+') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fields)
        for row in rows:
            csv_writer.writerow(row)

def read_and_export_to_csv(file_name, fields, read_table):
    records = read_table()
    export_to_csv(file_name, records, fields)

def export_users_to_csv():
    file_name = f"{csv_table_export_path}{User.table_name.lower()} - {get_current_datetime()}.csv"
    fields = User.fields
    read_and_export_to_csv(file_name, fields, lambda: read_all_users())
    return file_name

def export_competencies_to_csv():
    file_name = f"{csv_table_export_path}{Competency.table_name.lower()} - {get_current_datetime()}.csv"
    fields = Competency.fields
    read_and_export_to_csv(file_name, fields, lambda: read_all_competencies())
    return file_name

def export_assessments_to_csv():
    file_name = f"{csv_table_export_path}{Assessment.table_name.lower()} - {get_current_datetime()}.csv"
    fields = Assessment.fields
    read_and_export_to_csv(file_name, fields, lambda: read_all_assessments())
    return file_name

def export_assessment_results_to_csv():
    file_name = f"{csv_table_export_path}{AssessmentResult.table_name.lower()} - {get_current_datetime()}.csv"
    fields = AssessmentResult.fields
    read_and_export_to_csv(file_name, fields, lambda: read_all_assessment_results())
    return file_name

def get_user_report_name(user_id):
    return f"User Competency Summary - {user_id} - {get_current_datetime()}"

def get_competency_report_name(competency_id):
    return f"Competency Results Summary - {competency_id} - {get_current_datetime()}"

def user_competency_summary_to_csv(user_id, rows, fields):
    file_name = f"{reports_export_path}{get_user_report_name(user_id)}.csv"
    export_to_csv(file_name, rows, fields)
    return file_name

def competency_results_summary_to_csv(competency_id, rows, fields):
    file_name = f"{reports_export_path}{get_competency_report_name(competency_id)}.csv"
    export_to_csv(file_name, rows, fields)
    return file_name

def import_from_csv(file_name):
    rows = []
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            row = [None if not value else value for value in row]
            rows.append(row)
    return rows

def import_and_write_from_csv(file_name, create_record):
    try:
        data = import_from_csv(file_name)
        for record in data:
            create_record(record)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False

def check_users_import():
    return file_exists(users_csv_import_path)

def check_competencies_import():
    return file_exists(competencies_csv_import_path)

def check_assessments_import():
    return file_exists(assessments_csv_import_path)

def check_assessment_results_import():
    return file_exists(assessment_results_csv_import_path)

def import_users_from_csv(password_hashed):
    file_name = users_csv_import_path
    return import_and_write_from_csv(file_name, lambda r: create_user(*r, password_hashed))

def import_competencies_from_csv():
    file_name = competencies_csv_import_path
    return import_and_write_from_csv(file_name, lambda r: create_competency(*r))

def import_assessments_from_csv():
    file_name = assessments_csv_import_path
    return import_and_write_from_csv(file_name, lambda r: create_assessment(*r))

def import_assessment_results_from_csv():
    file_name = assessment_results_csv_import_path
    return import_and_write_from_csv(file_name, lambda r: create_assessment_result(*r))
