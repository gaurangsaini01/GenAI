from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()
client = OpenAI()
SYSTEM_PROMPT = """
you are a python expert and you must solve any problem using following steps:
Step 1 : Analyze
Step 2 : Think
Step 3 : Output 
Step 4: Verify
Step 5 : Result
Rules:
complete 1 step then wait for next input
Example : 
USER:"What's the result of 2+2?"
OUTPUT:{"step":"Analyze","content":"analyzing that the user is trying to ask me to solve a arithmetic operation"}
OUTPUT:{"step":"Think","content":"Thinking what could be the answer for 2+2"}
OUTPUT:{"step":"Output","content":"4"}
OUTPUT:{"step":"Verify","content":"Rechecking again whether 2+2 is 4 , if not repeat all steps again from start"}
OUTPUT:{"step":"Result","content":"Answer : 4"}
"""

response = client.responses.create(
    model="gpt-4o-mini",
    instructions=SYSTEM_PROMPT,
    input=[
        {"role":"user","content":"3+4 "},
        {"role":"assistant","content":json.dumps({"step":"Analyze","content":"analyzing that the user is asking to solve a simple arithmetic operation, specifically the addition of 3 and 4."})},
        {"role":"assistant","content":json.dumps({"step": "Think", "content": "Considering the operation 3 + 4, the expected sum is being calculated."})}
    ]
)

print(response.output_text)
