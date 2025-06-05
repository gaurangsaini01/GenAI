from dotenv import load_dotenv
from openai import OpenAI
from newsapi import NewsApiClient
import json
import os

load_dotenv()
client = OpenAI()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


def get_news(topic,category,ps=2):
    top_headlines = newsapi.get_top_headlines(q=topic,
                                          category=category,
                                          language='en',
                                          country='us',
                                          page=1,page_size=ps)
    news_list = []
    for a in top_headlines["articles"]:
        news_url = a["url"]
        news_title = a["title"]
        news_list.append({"title":news_title,"url":news_url})

    return news_list
        

tools = {
    "get_news":get_news
}

SYSTEM_PROMPT = f"""
    You are an helpful AI agent , that resolves user query .
    you will be solving user query with some predefined sequence of steps that are :
    START,PLAN,ACTION,OBSERVE,RESULT.

    Based on the given query you have to do step by step execution by using the available tools.
    and upon tool selection you perform an action to call the tool

    Available Tools:
    1. "get_news": Fetches the top news for the requested topic .

    Rules:
    1. Strictly give output in JSON format
    2. Produce one output at a time and wait for next input


    Example:

    User: Provide me 2 news about AI ?
    Output: {{"step":"start","content":"So I have to get 2 news related to AI, I will check my available tools if there is any"}}
    Output: {{"step":"plan","content":"I found an available tool "get_news" that can help me get the news"}}

    #in the action step you yourself decide which category the users query belong to , you can only choose from following categories : business, entertainment, general, health, science, sports ,technology .
    #you can only choose one category from the given one's , dont use any other category.

    Output: {{"step":"action","function":"get_news","topic":"AI","ps":"2","category":"technology"}}

    Output: {{"step":"observe","output":"1:Title:"AI is getting scary" \n URL:https://url1.com\n2:Title:"AI gets even better with agents", url: https://url2.com\n"}}
    Output: {{"step":"output","content":"1:Title:"AI is getting scary" \n URL:https://url1.com\n2:Title:"AI gets even better with agents", url: https://url2.com\n"}}

    
    Example:
    User: news on top android updates?
    Output: {{"step":"start","content":"So I have to get news related to top android updates, I will check my available tools if there is any"}}
    Output: {{"step":"plan","content":"I found an available tool "get_news" that can help me get the news"}}

    #in the action step you yourself decide which category the users query belong to , you can only choose from following categories : business, entertainment, general, health, science, sports ,technology .
    #you can only choose one category from the given one's , dont use any other category.

    #in case user provides long topics like "top android updates" you can make it "android" and search news related to it instead of nothing

    Output: {{"step":"action","function":"get_news","topic":"android","ps":"2","category":"technology"}}

    Output: {{"step":"observe","output":"1:Title:"Android phones getting cheaper" \n URL:https://url1.com\n2:Title:"android beats apple, gets even better with ai", url: https://url2.com\n"}}
    Output: {{"step":"output","content":"1:Title:"Android phones getting cheaper" \n URL:https://url1.com\n2:Title:"android beats apple, gets even better with ai", url: https://url2.com\n"}}

    Keep in mind you must not exceed these 5 steps . Only these 5 steps must be there . If no result found , simply say "No News Found"

        
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
        news_list = tools[parsed.get("function")](parsed.get("topic"), parsed.get("category"),int(parsed.get("ps")))
        messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":news_list})})

    if step == "output" :
        print(content)
        
        break