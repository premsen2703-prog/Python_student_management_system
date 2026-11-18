from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

print(os.path.abspath('database.db'))
app = Flask(__name__)

app.secret_key = "secretkey"

# DATABASE INITIALIZATION

def init_db():

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS students(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,
            age INTEGER,
            course TEXT,
            marks INTEGER,
            attendance INTEGER

        )

    ''')

    conn.commit()
    conn.close()

init_db()

# LOGIN PAGE

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":

            session['user'] = username

            return redirect('/')

    return render_template('login.html')

# DASHBOARD

@app.route('/')

def index():

    search = request.args.get('search')

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    if search:

        cursor.execute(
            "SELECT * FROM students WHERE name LIKE ?",
            ('%' + search + '%',)
        )

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        students=students
    )

# ADD STUDENT

@app.route('/add', methods=['GET', 'POST'])

def add_student():

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        marks = request.form['marks']
        attendance = request.form['attendance']

        conn = sqlite3.connect('database.db')

        cursor = conn.cursor()

        cursor.execute('''

            INSERT INTO students(
            name,
            age,
            course,
            marks,
            attendance
            )

            VALUES(?,?,?,?,?)

        ''',
        (name, age, course,
        marks, attendance))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_student.html')

# EDIT STUDENT

@app.route('/edit/<int:id>',
methods=['GET', 'POST'])

def edit_student(id):

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        course = request.form['course']
        marks = request.form['marks']
        attendance = request.form['attendance']

        cursor.execute('''

            UPDATE students

            SET
            name=?,
            age=?,
            course=?,
            marks=?,
            attendance=?

            WHERE id=?

        ''',
        (name, age, course,
        marks, attendance, id))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )

# DELETE STUDENT

@app.route('/delete/<int:id>')

def delete_student(id):

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# RUN APP

if __name__ == '__main__':

    app.run(debug=True)