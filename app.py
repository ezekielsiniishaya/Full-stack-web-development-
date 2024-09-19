
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'Iamsaved.100%2024',
    'host': 'localhost',
    'database': 'Mydatabase'
}

# Function to get a database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to add data to the database (e.g., a patient)
@app.route('/add_patient', methods=['POST'])
def add_patient():  
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dob = request.form['dob']
    gender = request.form['gender']
    language = request.form['language']

    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'INSERT INTO patients (first_name, last_name, date_of_birth, gender, language) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(query, (first_name, last_name, dob, gender, language))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/patients')

# Route to view patients
@app.route('/patients')
def patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('patients.html', patients=patients)

# Route to delete a patient
@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM patients WHERE patient_id = %s', (patient_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/patients')

if __name__ == "__main__":
    app.run(debug=True)
