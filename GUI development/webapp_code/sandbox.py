from flask import Flask, jsonify, request

# Create the Flask app
app = Flask(__name__)

# Example route that returns JSON data
@app.route('/api/greet/<name>', methods=['GET'])
def greet(name):
    # Create a JSON response
    return jsonify({
        'message': f'Hello, {name}!',
        'status': 'success'
    })

# Example route that handles POST request and returns JSON data
@app.route('/api/sum', methods=['POST'])
def calculate_sum():
    data = request.get_json()  # Get JSON data from the request body
    num1 = data.get('num1')
    num2 = data.get('num2')

    if num1 is None or num2 is None:
        return jsonify({'error': 'Missing parameters', 'status': 'fail'})

    total = num1 + num2
    return jsonify({'num1': num1, 'num2': num2, 'sum': total, 'status': 'success'})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
