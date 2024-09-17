from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    
    #Process to generate the problem
    
    return {"message": f"Echo: {message.text}"}

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
