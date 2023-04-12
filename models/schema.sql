CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT UNIQUE,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    date_created TEXT NOT NULL,
    hire_date TEXT,
    user_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Competencies (
    competency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    date_created TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competency_id INTEGER,
    name TEXT NOT NULL,
    date_created TEXT NOT NULL,

    UNIQUE (competency_id, name),

    FOREIGN KEY (competency_id)
        REFERENCES Competencies (competency_id)
);

CREATE TABLE IF NOT EXISTS Assessment_Results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    assessment_id INTEGER,
    manager_id INTEGER,
    score INTEGER NOT NULL,
    date_taken TEXT NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES Users (user_id),
    FOREIGN KEY (manager_id)
        REFERENCES Users (user_id),
    FOREIGN KEY (assessment_id)
        REFERENCES Assessments (assessment_id)
);

