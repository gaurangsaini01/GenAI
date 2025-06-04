from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()
client = OpenAI()

def get_weather(city):
    # Simulating an API call here !
    return "12 degree celsius"

tools = {
    "get_weather":get_weather
}

SYSTEM_PROMPT = f"""
    You are an helpful AI agent , that resolves user query .
    you will be solving user query with some predefined sequence of steps that are :
    START,PLAN,ACTION,OBSERVE,RESULT.

    Based on the given query you have to do step by step execution by using the available tools.
    and upon tool selection you perform an action to call the tool

    Available Tools:
    1. "get_weather": takes a city name as input and return the temperature of that city
    2. "get_dancing" : dances for you

    Rules:
    1. Strictly give output in JSON format
    2. Produce one output at a time and wait for next input


    Example:

    User: What's the weather in Patiala?
    Output: {{"step":"start","content":"So I have to get the weather of patiala , I will check my available tools if there is any"}}
    Output: {{"step":"plan","content":"I found an available tool "get_weather" that can help me get the weather"}}
    Output: {{"step":"action","function":"get_weather","input":"patiala"}}
    Output: {{"step":"observe","output":"12 degree cel"}}
    Output: {{"step":"output","content":"The weather of patiala is 12 degrees ."}}


"""

messages = [{"role":"system","content":SYSTEM_PROMPT}]

query = input("User: ")
messages.append({"role": "user", "content": query})
while True:
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        response_format={"type":"json_object"},
        messages = messages
    )
    messages.append({"role":"assistant","content":response.choices[0].message.content})
    parsed = json.loads(response.choices[0].message.content)
    step = parsed.get("step")
    content = parsed.get("content")

    if step == "action" :
        ans = tools[parsed.get("function")](parsed.get("input"))
        messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":ans})})

    if step == "output" :
        print(content)
        break