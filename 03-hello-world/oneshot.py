from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="Talk like a mom",
    input=[
        {"role":"user","content":"My name is Piyush"},
        {"role":"assistant","content":"Hi Piyush, How Can I help you today "},
        {"role":"user","content":"Whats my name"}
    ]
)
print(response.output_text)