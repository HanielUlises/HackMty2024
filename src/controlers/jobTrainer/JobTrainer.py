from openai import OpenAI
from SummarizeCompany import Client
from SummarizeCompany import SummarizeCompany
import data_base_handler as dbh
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("ibm/PowerLM-3b")
model = AutoModelForCausalLM.from_pretrained("ibm/PowerLM-3b")

class JobTrainer:
    def __init__(self):
        conections = Client()
        self.client = conections.client
        self.index = conections.index
        self.mongo = conections.mongo
        self.model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

        self.tokenizer = AutoTokenizer.from_pretrained("ibm/PowerLM-3b")
        self.lm_model = AutoModelForCausalLM.from_pretrained("ibm/PowerLM-3b")

    def review_code(self, guideline_code, user_code):
        """Review the provided user code against guideline code and provide analysis."""
        try:
            response_interpret = self.client.chat.completions.create(
                model="tgi",
                messages=[
                    {"role": "system", "content": "Compare the following two pieces of code and evaluate their outputs. "
                                                  "Markup the differences between each."},
                    {"role": "user", "content": f"Guideline Code:\n{guideline_code}"},
                    {"role": "user", "content": f"User Code:\n{user_code}"},
                    {"role": "user", "content": "First, run both codes and compare their outputs. Consider the guidelines "
                                                "and coding standards that you might identify from the guideline code and point out "
                                                "what the user code got right in terms of standards and best practices, "
                                                "what they got wrong, and finally, what they could improve."}
                ]
            )

            completion_text = response_interpret.choices[0].message.content
            return completion_text

        except Exception as e:
            return f"Error during code review: {str(e)}"

    def generate_problem(self, context, prompt):
        """Generate a problem for a new employee based on the context using PowerLM-3b."""
        try:
            # Combine the context and prompt
            input_text = prompt + context + " Tell me what problem you would give to the new employee. And list each potential guideline that the code must meet."
            
            # Tokenize the input text
            inputs = self.tokenizer(input_text, return_tensors="pt")

            # Generate the response from the model
            outputs = self.lm_model.generate(**inputs, max_length=500, do_sample=True, temperature=0.7)

            # Decode the generated tokens back into a string
            problem = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            return problem

        except Exception as e:
            return f"Error generating problem: {str(e)}"

    
    def generate_code(self, context, prompt, problem):
        try:
            response = self.client.chat.completions.create(
                model="tgi",
                messages=[
                    {"role": "system", "content": "Check this problem statement and generate code based on it: \n" + problem +
                    "\n\nMake sure to generate a complete and functional code snippet, without cutting off or omitting parts."}
                ],
                max_tokens=1000, 
                stream=False
            )
            
            code = response.choices[0].message.content

            # Writing the code to a file to avoid truncation
            with open("generated_code_output.txt", "w") as file:
                file.write(code)

            return code

        except Exception as e:
            return f"Error generating code: {str(e)}"



    def answering_question(self, query):
        """Answer a question based on retrieved document context."""
        try:
            context = dbh.retrieve_document(query=query, index=self.index, mongo=self.mongo, model=self.model)
            context = ' '.join(context)

            prompt = f"""
            Context: {context}
            Question: {query}

            Now respond appropriately based on the analysis.
            """

            response = self.client.chat.completions.create(
                model="tgi",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            answer = response.choices[0].message.content
            return answer

        except Exception as e:
            return f"Error answering question: {str(e)}"


if __name__ == '__main__':

    train = SummarizeCompany()
    
    context = train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    
    trainer = JobTrainer()

    prompt = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a problem based on the context of the company. The context is as follows:"
    promtp2 = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a programming problem about other programming code fragment. The programming code fragment is as follows:"
    problem = trainer.generate_problem(context, promtp2)
    guideline_code = trainer.generate_code(context,promtp2,problem)

    print (problem)
    print (guideline_code)

    user_code = """```javascript
        // Function to calculate the area of a rectangle
        /**
        * Calculates the area of a rectangle.
        * 
        * @param {number} width The width of the rectangle.
        * @param {number} height The height of the rectangle.
        * @returns {number} The area of the rectangle.
        */
        function calculateArea(width, height) {
        // Variable to store the calculated area
        let area = width * height;
        return area;
        }

        // Variable declaration with let for block"""

    review = trainer.review_code(guideline_code, user_code)

    print("Problem:")
    print(problem)
    print("\nGenerated Code:")
    print(guideline_code)
    print("\nReview Result:")
    print(review)