import os
import pandas as pd
import csv
from flask import Flask, render_template, request, redirect, url_for
from random import sample
import psycopg2

# Connect to the PostgreSQL database
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Load the CSV file with image IDs and URLs
images = pd.read_csv('images.csv')

# Shuffle the DataFrame
images = images.sample(frac=1).reset_index(drop=True)

app = Flask(__name__)

@app.route('/image/<int:image_index>')
def image(image_index):
    message = request.args.get('message')
    image_id = images.loc[image_index, 'ID']
    image_url = images.loc[image_index, 'URL']
    return render_template('cowslips.html', image_id=image_id, image_url=image_url, message=message)

@app.route('/submit', methods=['POST'])
def submit():
    image_id = request.form.get('image_id')
    image_url = request.form.get('image_url')
    flower_type = request.form.get('flower_type')

    # Insert the submitted data into the database
    cur.execute("INSERT INTO responses (id, url, response) VALUES (%s, %s, %s)", (image_id, image_url, flower_type))
    conn.commit()

    image_index = images[images['ID'] == int(image_id)].index[0]
    next_image_index = (image_index + 1) % len(images)

    return redirect(url_for('image', image_index=next_image_index, message="Thank you for your submission!"))

@app.route('/')
def index():
    return redirect(url_for('image', image_index=0))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
