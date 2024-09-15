from openai import OpenAI

client = OpenAI(
    api_key="-", 
    base_url="http://198.145.126.109.nip.io/v1" 
)

# Description process for the openAI model
response = client.chat.completions.create(
    model="tgi",
    messages=[
        # System role: Sets the assistant's behavior
        {"role": "system", "content": "You are a helpful assistant."},

        # User asks a question
        {"role": "user", "content": "Who won the World Series in 2020?"},

        # Assistant responds to the user's question
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},

        # User continues with a follow-up question
        {"role": "user", "content": "Where was it played?"},

        # Assistant provides the answer to the follow-up question
        {"role": "assistant", "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas."}
    ],
    stream=True
)

print(response)
