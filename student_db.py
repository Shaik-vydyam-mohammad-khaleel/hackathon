import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('student_recognition.db')

# Create a cursor object
cursor = conn.cursor()

# 1. Create Student Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Student ("
    NAME TEXT,
    student_id INTEGER PRIMARY KEY,
    GENDER TEXT,
    YEAR INTEGER,CGPA REAl,SEMESTER WISE CGPA REAL,CORE COURSES-CGPA REAL,NATIONAL HACKATHON INTEGER,LOCAL HACKATHON INTEGER,PPT INTEGER, PROJECT INTEGER, EXTRACURICULAR INTEGER
   
")
''')