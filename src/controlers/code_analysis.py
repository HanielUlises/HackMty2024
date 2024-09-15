from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(
    api_key="-",
    base_url="http://198.145.126.109:8080/v1"
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('results/analysis.html')

@app.route('/review-code', methods=['POST'])
def review_code():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    guideline_code = data.get("guideline_code")
    user_code = data.get("user_code")

    if not guideline_code or not user_code:
        return jsonify({"error": "Missing 'guideline_code' or 'user_code'"}), 400

    try:
        # First API Call: Evaluate code outputs
        response_interpret = client.chat.completions.create(
            model="tgi",  # Retained as per your instruction
            messages=[
                {"role": "system", "content": "Compare the following two pieces of code and evaluate their outputs."},
                {"role": "user", "content": f"Guideline Code:\n{guideline_code}"},
                {"role": "user", "content": f"User Code:\n{user_code}"},
                {"role": "user", "content": "First, run both codes and compare their outputs. If the outputs are the same, return 1, if not, return 0."}
            ]
        )
        
        # Log the entire response object to understand its structure
        print("Response from API:", response_interpret)

        # Return the response as JSON
        return jsonify({"response": response_interpret})

    except Exception as e:
        print(f"Error during API request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
