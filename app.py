import os
import pandas as pd
import csv
from flask import Flask, render_template, request, redirect, url_for
from random import sample

# Load the CSV file with image IDs and URLs
images = pd.read_csv('images.csv')

# Shuffle the DataFrame
images = images.sample(frac=1).reset_index(drop=True)

app = Flask(__name__)

# Create a variable for the absolute path to the responses.csv file
responses_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'responses.csv')

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
    
    # Read the responses.csv file
    responses = pd.read_csv(responses_file_path)

    # Create a new DataFrame with the submitted data
    new_response = pd.DataFrame({'ID': [image_id], 'URL': [image_url], 'Response': [flower_type]})
    
    # Append the new response to the responses DataFrame
    responses = pd.concat([responses, new_response], ignore_index=True)

    # Save the updated responses DataFrame to the CSV file
    responses.to_csv(responses_file_path, index=False)

    image_index = images[images['ID'] == int(image_id)].index[0]
    next_image_index = (image_index + 1) % len(images)

    return redirect(url_for('image', image_index=next_image_index, message="Thank you for your submission!"))


@app.route('/')
def index():
    return redirect(url_for('image', image_index=0))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
