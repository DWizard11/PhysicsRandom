from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime
import csv

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add(): 
    name = request.form.get('name')
    date = request.form['date']
    desc = request.form.get('description')
    severity = request.form['severity'].lower()

    if severity not in ['low', 'medium', 'high']: 
        return "Invalid severity level"

    try: 
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError: 
        return "Invalid date format"

    new_offence = [name, date, desc, severity]
    
    # file closes after with block 
    with open("offences.csv", "a") as file: 
        writer = csv.writer(file) 
        writer.writerow(new_offence)

    return redirect("/")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
