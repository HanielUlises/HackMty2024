from flask import Blueprint, request, jsonify
import jobTrainer
import SummarizeCompany
import jobTrainer.JobTrainer
# Create a blueprint
processing_bp = Blueprint('processing', __name__)

# Define the /process route in the blueprint
@processing_bp.route('/process', methods=['POST'])
def process():
    # Instantiate the business logic classes
    train = SummarizeCompany()
    
    # Here you can define the context, it can come from the request or be hardcoded
    context = train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    
    # Generate the problem using JobTrainer
    trainer = jobTrainer.JobTrainer.JobTrainer()
    problem = trainer.generateProblem(context)
    
    # Return the result as a JSON response
    return jsonify({'resultado': problem})
