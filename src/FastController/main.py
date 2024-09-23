from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","controlers","jobTrainer")))
from JobTrainer import JobTrainer
from SummarizeCompany import SummarizeCompany
app = FastAPI()

# List of allowed origins (your frontend URL)
origins = [
    "*",  # Add the correct frontend origin here
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set the allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers (Content-Type, Authorization, etc.)
)

class Message(BaseModel):
    text: str

@app.post("/api/echo")
async def problem_desctiption(message: Message):
    import time
    start_time = time.time()


    # #Process to generate the problem
    train = SummarizeCompany() # ~1 seg
    context = await train.relevantIdeas("You are a text analyst. You have to extract the main ideas from the following text:")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    
    print("Extracted context")
    
    trainer = JobTrainer()
    # prompt = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a problem based on the context of the company. The context is as follows:"
    promtp2 = "You are a trainer in a company who teaches newly hired employees. For their introduction, you ask them to solve a programming problem about other programming code fragment. The programming code fragment is as follows:"

    problem = await trainer.generate_problem(context, promtp2)
    print("generated problem")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    
    guideline_code = await trainer.generate_code(context,promtp2,problem)
    
    print("generated guideline code")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time}")
    
    return {"message": f"Echo: {problem}"}

@app.post("/api/other-endpoint")
async def compare_response(message: Message):
    
    
    #Process to compare the original code and the inputted problem
    
    return {"message": f"Other API response: {message.text}"}

@app.post("/api/third-endpoint")
async def chatResponse(message: Message):
    
    #Process to process user input and generate the chatbot response
    
    
    return {"message": f"Third API response: {message.text}"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
