from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Likhith@7685'
app.config['MYSQL_DB'] = 'college_db'

mysql = MySQL(app)

# Secret key for session management
app.secret_key = 'Likhith@7685'

# Route to display all students
@app.route('/')
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY id")
        students = cur.fetchall()
        cur.close()
        return render_template('index.html', students=students)
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
        return render_template('index.html', students=[])

# Route to add a new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            # Fetch form data
            usn = request.form['usn']
            name = request.form['name']
            department = request.form['department']
            dob = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            sem = request.form['sem']
            cgpa = request.form['cgpa']

            # Insert into database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (usn, name, department, date_of_birth, sem, cgpa) VALUES (%s, %s, %s, %s, %s, %s)",
                        (usn, name, department, dob, sem, cgpa))
            mysql.connection.commit()
            cur.close()

            flash('Student added successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
            return redirect(url_for('add_student'))

    return render_template('add_student.html')

# Route to view all students
@app.route('/view_students')
def view_students():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students ORDER BY id")
        students = cur.fetchall()
        cur.close()
        return render_template('view_students.html', students=students)
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
        return render_template('view_students.html', students=[])

# Route to view a single student's details
@app.route('/view_student/<int:student_id>')
def view_student(student_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
        cur.close()
        if student:
            return render_template('view_student.html', student=student)
        else:
            flash('Student not found', 'danger')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f"An error occurred: {e}", 'danger')
        return redirect(url_for('index'))

@app.route('/search_students', methods=['GET', 'POST'])
def search_students():
    if request.method == 'POST':
        department = request.form['department']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM students WHERE department = %s", (department,))
            students = cur.fetchall()
            cur.close()
            return render_template('search_results.html', students=students)
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
            return render_template('search_students.html')
    return render_template('search_students.html')

if __name__ == '__main__':
    app.run(debug=True)
