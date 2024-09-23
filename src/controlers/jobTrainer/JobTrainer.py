from openai import OpenAI
from SummarizeCompany import Client
from SummarizeCompany import SummarizeCompany
import data_base_handler as dbh
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM


import httpx

class JobTrainer:
    def __init__(self):
        conections = Client()
        self.client = conections.client
        self.index = conections.index
        self.mongo = conections.mongo
        


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

    async def generate_problem(self, context, prompt):
        """Generate a problem for a new employee based on the context using Frida API."""
        try:
            # Combine the context and prompt
            input_text = prompt + context + " Tell me what problem you would give to the new employee. And list each potential guideline that the code must meet."
            
            
            #We send the request to the frida API
            
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    url="http://198.145.126.109:8080/v1/chat/completions",  # Assuming this is your Frida endpoint
                    json={
                            "model": "tgi",  # Specify the model used in Frida, e.g., tgi or another LLM
                            "messages": [
                                {"role": "system", "content": input_text}
                            ],
                            "max_tokens": 200,  # Similar to the `max_length` you used before
                            "temperature": 1,    # You can adjust this depending on the variability of responses
                            "stream": False
                        }
                )
                
            problem = response.json()["choices"][0]["message"]["content"]


            return problem
        
        except httpx.ReadTimeout:
            return "Error: The request to the API timed out."
        except Exception as e:
            return f"Error generating problem {str(e)}"


    
    async def generate_code(self, context, prompt, problem):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
            

                response = await client.post(
                    url="http://198.145.126.109:8080/v1/chat/completions",
                    json= {
                        "model":"tgi",
                        "messages":[
                            {"role": "system", "content": "Check this problem statement and generate code based on it: \n" + problem +
                            "\n\nMake sure to generate a complete and functional code snippet, without cutting off or omitting parts."}
                        ],
                        "max_tokens":200, 
                        "stream":False
                    }
                    
                    
                    
                )
                
                code = response.json()["choices"][0]["message"]["content"]
                return code
        
        except httpx.ReadTimeout:
            return "Error: The request to the API timed out"
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


# if __name__ == '__main__':

    # train = SummarizeCompany()
    
    # context = train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    
    # trainer = JobTrainer()

    # prompt = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a problem based on the context of the company. The context is as follows:"
    # promtp2 = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a programming problem about other programming code fragment. The programming code fragment is as follows:"
    # problem = trainer.generate_problem(context, promtp2)
    # guideline_code = trainer.generate_code(context,promtp2,problem)

    # print (problem)
    # print (guideline_code)

    # user_code = """```javascript
    #     // Function to calculate the area of a rectangle
    #     /**
    #     * Calculates the area of a rectangle.
    #     * 
    #     * @param {number} width The width of the rectangle.
    #     * @param {number} height The height of the rectangle.
    #     * @returns {number} The area of the rectangle.
    #     */
    #     function calculateArea(width, height) {
    #     // Variable to store the calculated area
    #     let area = width * height;
    #     return area;
    #     }

    #     // Variable declaration with let for block"""

    # review = trainer.review_code(guideline_code, user_code)

    # print("Problem:")
    # print(problem)
    # print("\nGenerated Code:")
    # print(guideline_code)
    # print("\nReview Result:")
    # print(review)