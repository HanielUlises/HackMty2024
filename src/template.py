from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(
    api_key="-",
    base_url="http://198.145.126.109:8080/v1"
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route for code review processing
@app.route('/review-code', methods=['POST'])
def review_code():
    data = request.get_json()
    guideline_code = data.get("guideline_code")
    user_code = data.get("user_code")

    # API call for our code review purposes
    response = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": "You are a coding assistant that reviews code based on guidelines."},
            {"role": "user", "content": f"Guideline code:\n{guideline_code}"},
            {"role": "user", "content": f"User code:\n{user_code}"},
            {"role": "user", "content": "Please review the user's code and provide feedback."}
        ]
    )
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
