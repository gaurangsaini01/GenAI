from typing import Union,Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

class State(TypedDict):
    query:str
    llm_result:Union[str,None]
    is_coding_ques: bool
    accuracy:str

class categorizeResponse(BaseModel):
    is_coding_ques : bool

class accuracyFormat(BaseModel):
    accuracy : str

def categorizequery(state:State):
    #use nano model to categories
    print("⭐️ Categorizing Query")
    query = state['query']
    SYSTEM_PROMPT = """
    You are an expert in classifying whether a query is related to coding or not.
    You must return true if coding query else false.
    """
    res = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        response_format=categorizeResponse,
        messages=[{"role":"user","content":query},{"role":"system","content":SYSTEM_PROMPT}]
    )
    is_coding_ques  = res.choices[0].message.parsed.is_coding_ques
    state['is_coding_ques'] = is_coding_ques
    return state

def route_query(state:State) -> Literal["general_query","coding_query"]:
    print("⭐️ Routing Query")

    is_coding_ques = state["is_coding_ques"]
    if is_coding_ques:
        return "coding_query"
    return "general_query"

def general_query(state:State):
    print("⭐️ General Query")

    query = state['query']
    SYSTEM_PROMPT = """You are an AI agent specialized to solve general Queries of Users . """
    res = res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":query},{"role":"system","content":SYSTEM_PROMPT}]
    )
    llm_result  = res.choices[0].message.content
    state['llm_result'] = llm_result
    return state

def coding_query(state:State):
    print("⭐️ Coding Query")

    query = state['query']
    SYSTEM_PROMPT = """You are an AI agent specialized to solve coding Queries of Users . """
    res = res = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role":"user","content":query},{"role":"system","content":SYSTEM_PROMPT}]
    )
    llm_result  = res.choices[0].message.content
    state['llm_result'] = llm_result
    return state

def check_code(state:State):
    print("⭐️ Checking Code Query")

    query = state['query']
    llm_result = state["llm_result"]
    SYSTEM_PROMPT = f"""You are an AI agent specialized to check whether the given result is correct or not according to this query .
     
    query :{query}
    result: {llm_result}
    
    return an accuracy percentage 

    """
    res = client.beta.chat.completions.parse(
        model="gpt-4o",
        response_format=accuracyFormat,
        messages=[{"role":"system","content":SYSTEM_PROMPT}]
    )
    accuracy  = res.choices[0].message.parsed.accuracy
    state['accuracy'] = accuracy
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("categorizequery",categorizequery)
graph_builder.add_node("route_query",route_query)
graph_builder.add_node("general_query",general_query)
graph_builder.add_node("coding_query",coding_query)
graph_builder.add_node("check_code",check_code)

graph_builder.add_edge(START,"categorizequery")
#route query as a string ni jayega , function hi jayega . 
graph_builder.add_conditional_edges("categorizequery",route_query)

graph_builder.add_edge("general_query",END)
graph_builder.add_edge("coding_query","check_code")
graph_builder.add_edge("check_code",END)


graph = graph_builder.compile()

def main():
    query = input("Enter Query:")
    state = {
        "query":query,
        "llm_result":None,
        "is_coding_ques":False,
        "accuracy":""
    }
    graph_result = graph.invoke(state)
    print(graph_result['llm_result'])

main()