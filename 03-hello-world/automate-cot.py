from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()
client = OpenAI()
SYSTEM_PROMPT = """
You are a python expert and you must solve any problem using following steps:
Step 1 : Analyze
Step 2 : Think
Step 3 : Output 
Step 4 : Verify
Step 5 : Result


Output Format:
{"step":"string","content":"string"}

Example : 
USER:"What's the result of 2+2?"
OUTPUT: {"step":"Analyze","content":"analyzing that the user is trying to ask me to solve a arithmetic operation"}
OUTPUT: {"step":"Think","content":"Thinking what could be the answer for 2+2"}
OUTPUT: {"step":"Output","content":"4"}
OUTPUT: {"step":"Verify","content":"Rechecking again whether 2+2 is 4"}
OUTPUT: {"step":"Result","content":"Answer : 4"}


Important:
- You must output only one step per response.
- Each response should strictly follow JSON format: {"step":"string", "content":"string"}
- Do not move to the next step until prompted again.

"""


ques = input("Enter Your Question ?  ")
messages = [{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":ques}]

while(True):
    res = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages,
    )   
    messages.append({"role":"assistant","content":res.choices[0].message.content})
    parsed_res = json.loads(res.choices[0].message.content)
    if parsed_res.get("step") != "Result":
        print("🧠:",parsed_res.get("content"))
    else:
        print("Final Output : ",parsed_res.get("content"))
        break