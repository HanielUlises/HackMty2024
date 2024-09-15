from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(
    api_key="-",
    base_url="http://198.145.126.109:8080/v1"
)

assistant = client.beta.assistants.create(
    purpose="Evaluate and compare code",
    instructions="You are a code interpreter that can evaluate two sets of code (guideline and user code)," 
    + "compare their outputs, and log if they give the same results or not.",
    tools=[{"type": "code_interpreter"}]
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('results/analysis.html')

# Route for code review processing      
@app.route('/review-code', methods=['POST'])
def review_code():
    # Step 1:
    # Retrieval data from a given json
    # Both company's guideline (coding standards, best practices)
    # and the input from the coding evaluation

    # Chevy -> X1 
    # Daniel -> X1 (submit) 
    # Loading 
    # This data is retrieved from the CHEVY and the coding evaluation

    data = request.get_json()
    guideline_code = data.get("guideline_code")
    user_code = data.get("user_code")

    # Step 2: Send the code to the assistant for evaluation
    response_interpret = assistant.completions.create(
        input=f"""
        Compare the following two pieces of code and evaluate their outputs.

        Guideline Code:
        {guideline_code}

        User Code:
        {user_code}

        First, run both codes and compare their outputs. 
        If the outputs are the same, log 1, if not, 0
        """
    )
    
    result_interpret = response_interpret["choices"][0]["message"]["content"]
    if(result_interpret == 1):
        # Processing of input
        response_compare = client.chat.completions.create(
            model="tgi",
            messages=[
                {"role": "system", "content": "First, run both codes and compare their outputs" +
                "Then, highlight any differences in functionality and mark up where the user code deviates from" + 
                "the guideline code. You should identify from the guideline_code a best practices" + 
                "list: i) What the programmer (user_code) got right based on these guidelines (guideline_code)"+
                "ii) What the the programmer (user_code) got wrong based on these guidelines" + 
                "iii) Improvements (suggestions)"},
                {"role": "user", "content": f"Guideline code:\n{guideline_code}"},
                {"role": "user", "content": f"User code:\n{user_code}"},
                {"role": "user", "content": "Compare the following two pieces of code and evalute their outputs."}
            ]
        )
        result_compare = response_compare["choices"][0]["message"]["content"]
        return jsonify({
        "assistant_feedback": result_compare
    })
    elif(result_interpret == 0):
        # May change later to show within the results (analysis)
        result_wrong = client.chat.completions.create(
            model="tgi",
            messages=[{"role": "system", "content": "Mark up what these codes differ, how the user_code is different from the guideline_code"+
                       "because they logged different results, mark up what the user got wrong"},
                {"role": "user", "content": f"Guideline code:\n{guideline_code}"},
                {"role": "user", "content": f"User code:\n{user_code}"},
                {"role": "user", "content": "Compare the following two pieces of code and evalute their outputs."}
            ]
        )
        print("The user input function is not correct, check output")
        return jsonify({
        "assistant_feedback": result_wrong
    })
    else:
        # Code does not compile
        print("Wrong run")


    # Evaluation result
    

if __name__ == '__main__':
    app.run(debug=True)

"""
Exclusivamente, este Json con el se va a trabajar
estará poblado por los datos obtenidos del <<submit>> del 
programador a evaluar y los datos obtenidos de los lineamientos de la empresa



guideline_code{
--------
}
user_input{
-------
}
"""