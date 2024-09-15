from flask import Blueprint, request, jsonify
import jobTrainer
import SummarizeCompany as SummarizeCompany
import jobTrainer.JobTrainer
# Create a blueprint
processing_bp = Blueprint('processing', __name__)

# Define the /process route in the blueprint
@processing_bp.route('/process', methods=['POST'])
def process():
    # Instantiate the business logic classes
    train = SummarizeCompany()
    
    # Here you can define the context, it can come from the request or be hardcoded
    # Promt de reconocimiento de patrones 
    # #You are a pattern detection specialist. You have to find patterns in the following text:"
    context = train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    
    # Generate the problem using JobTrainer
    trainer = jobTrainer.JobTrainer.JobTrainer()
    promt = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a problem based on the context of the company. The context is as follows:"
    promt2 = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a programming problem about other programming code fragment. The programming code fragment is as follows:"
    problem = trainer.generateProblem(context, promt2)
    
    # Return the result as a JSON response
    return jsonify({'resultado': problem})
