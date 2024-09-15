from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    api_key="-",  # Replace with your actual API key
    base_url="http://198.145.126.109:8080/v1"
)

# Create the analysis blueprint
analysis_bp = Blueprint('analysis', __name__, template_folder="../../web/analysis")

# Route to serve the HTML file
@analysis_bp.route('/')
def index():
    return render_template('analysis.html')

# Route to handle POST requests for code review
@analysis_bp.route('/review-code', methods=['POST'])
def review_code():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    guideline_code = data.get("guideline_code")
    user_code = data.get("user_code")

    if not guideline_code or not user_code:
        return jsonify({"error": "Missing 'guideline_code' or 'user_code'"}), 400

    try:
        response_interpret = client.chat.completions.create(
            model="tgi",
            messages=[
                {"role": "system", "content": "Compare the following two pieces of code and evaluate their outputs."},
                {"role": "user", "content": f"Guideline Code:\n{guideline_code}"},
                {"role": "user", "content": f"User Code:\n{user_code}"},
                {"role": "user", "content": "First, run both codes and compare their outputs. If the outputs are the same, return 1, if not, return 0."}
            ]
        )

        completion_text = response_interpret.choices[0].message.content
        return jsonify({"response": completion_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
