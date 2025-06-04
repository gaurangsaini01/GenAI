from dotenv import load_dotenv
from openai import OpenAI
from newsapi import NewsApiClient
import json
import os

load_dotenv()
client = OpenAI()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


def get_weather(city):
    return "12 degree celsius"

def get_news(topic,ps):
    top_headlines = newsapi.get_top_headlines(q=topic,
                                          category="technology",
                                          language='en',
                                          country='us',
                                          page=1,page_size=ps)
    # print(top_headlines)
    count = 1
    for a in top_headlines["articles"]:
        print(f"{count}: {a.get('title')}")
        count = count+1


tools = {
    "get_weather":get_weather,
    "get_news":get_news
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

    User: Provide me 3 news about AI ?
    Output: {{"step":"start","content":"So I have to get 3 news related to AI, I will check my available tools if there is any"}}
    Output: {{"step":"plan","content":"I found an available tool "get_news" that can help me get the news"}}
    Output: {{"step":"action","function":"get_news","topic":"AI","ps":"3"}}

    Output: {{"step":"observe","output":"1:Meta and Yandex are de-anonymizing Android users web browsing identifiers - Ars Technica
            2:Nintendo Prepping For All Switch 2 Eventualities With 'Out Of Stock' Signs - Nintendo Life
            3:I ignored Google's passkey prompts for months, but now I feel silly for waiting - Android Authority"}}
    Output: {{"step":"output","content":"1:Meta and Yandex are de-anonymizing Android users web browsing identifiers - Ars Technica
            2:Nintendo Prepping For All Switch 2 Eventualities With 'Out Of Stock' Signs - Nintendo Life
            3:I ignored Google's passkey prompts for months, but now I feel silly for waiting - Android Authority"}}

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
        ans = tools[parsed.get("function")](parsed.get("topic"),int(parsed.get("ps")))
        messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":ans})})

    if step == "output" :
        print(content)
        
        break