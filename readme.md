
# Hayden Burker Competency Tracker

### Steps to run

	pipenv install
	pipenv shell
	python main.py

Running the app for the first time will take you to a form to create a manager. The credentials entered there will be the login credentials next time you login.

If at least one manager already exists, running the app will take you to the login page.

### Steps to add test data

* Login as manager
* Copy all csv files in `csv/test_data` to `csv/imports`
* Go to Import/export csv options
* Run all import options (users with plaintext passwords, competencies, assessments, assessment results)
	* If any imports fail, create a new database by closing the app, rename `competency_tracker.db` in the database folder, then run the app. You can now choose to either add the test data and login using one of the managers in `users.csv` or create a new manager first then import data
* Congratulation! You now have test data!