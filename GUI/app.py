from flask import Flask, request, render_template, redirect, url_for, flash
import os
import time  # Simulating delay for the progress bar

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/how_to_use')
def how_to_use():
    return render_template('how_to_use.html')

@app.route('/how_works')
def how_works():
    return render_template('how_works.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Simulate a pipeline process
        run_pipeline(filepath)

        return redirect(url_for('results'))
    else:
        flash('Invalid file type. Please upload a CSV or TXT file.')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    return render_template('results.html')

def run_pipeline(filepath):
    """ Simulate a pipeline action by adding a delay """
    print(f"Processing file: {filepath}")
    time.sleep(5)  # Simulate delay for processing
    print(f"Processing complete for: {filepath}")

if __name__ == "__main__":
    app.run(debug=True)
