 from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

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
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Run the pipeline
            result = run_pipeline(filepath)

            return jsonify({'message': 'File successfully uploaded', 'result': result}), 200

        return jsonify({'error': 'File not allowed'}), 400

    except Exception as e:
        # Return JSON error message on exception
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Route to display the result
@app.route('/result')
def result():
    output = request.args.get('output', 'No result available')
    return render_template('result.html', output=output)

# Example pipeline function that processes the uploaded file
def run_pipeline(filepath):
    try:
        # Example: Read the uploaded CSV and return the sum of a numeric column
        df = pd.read_csv(filepath)
        result = df.sum(numeric_only=True).to_string()
        return result
    except Exception as e:
        # Return the error message to be shown in the frontend
        return f"Error processing file: {str(e)}"


if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=3000, debug=True)
