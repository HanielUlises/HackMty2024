import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
import requests 

# The Flask app URL
url = 'http://127.0.0.1:5000/review-code'

# JSON data for the test
data = {
    "guideline_code": "def add(a, b): return a + b",
    "user_code": "def add(a, b): return a + b"
}

# Send the POST request to the Flask app
response = requests.post(url, json=data)

# Print the response from the Flask app
print(response.json())
