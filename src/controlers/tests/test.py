from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple GET route
@app.route('/get-data', methods=['GET'])
def get_data():
    
    
    
    
    return jsonify({"message": "Hello from Flask!"})

# POST route that accepts JSON data
@app.route('/submit-code', methods=['POST'])
def submit_code():
    

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    
    user_code = data.get('user_code')
    guideline_code = data.get('guideline_code')
    
    if user_code == guideline_code:
        return jsonify({"result": "Codes match!"})
    else:
        return jsonify({"result": "Codes do not match!"})

if __name__ == '__main__':
    app.run(debug=True)
