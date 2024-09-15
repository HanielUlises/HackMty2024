from flask import Flask, render_template
import os
from codeAnalysis.code_analysis import analysis_bp
from jobTrainer.jobTrainerRoutes import processing_bp

# Initialize the Flask app and specify the folder for HTML templates
app = Flask(__name__, template_folder="../web",static_folder="../static")

# Register blueprints for the 'analysis' and 'processing' sections of the app
app.register_blueprint(analysis_bp, url_prefix='/analysis')
app.register_blueprint(processing_bp, url_prefix='/processing')

# Root route for the app
@app.route('/')
def index():
    return render_template("evaluation.html")

# Start the Flask app with debugging enabled
if __name__ == '__main__':
    app.run(debug=True)
