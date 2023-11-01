from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import csv

app = Flask(__name__)
app.secret_key = 'the_most_secret_key'  # Replace with a secret key for session management
csv_file = 'users.csv'  # Path to your CSV file

# function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    username = session.get('username')
    if username:
        return render_template('home.html', username=username)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username:
        return render_template('dashboard.html', username=username)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the CSV file
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[0] == username and row[1] == hash_password(password):
                    session['username'] = username
                    return redirect(url_for('home'))

        return 'Login failed'

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it in the CSV file
        hashed_password = hash_password(password)

        # Store the user in the CSV file
        with open(csv_file, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([username, hashed_password])

        session['username'] = username

        return redirect(url_for('home'))
    
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()
