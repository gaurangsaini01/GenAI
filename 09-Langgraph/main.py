from typing import Union
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START,END
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

class State(TypedDict):
    query:str
    llm_result: Union[str,None]
    
    #creating a Node
def get_ans(state:State):
    query = state["query"]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":query}]
    )
    state["llm_result"] = response.choices[0].message.content
    return state


#Creating a graph builder
graph_builder = StateGraph(State)
graph_builder.add_node("get_ans",get_ans)

graph_builder.add_edge(START,"get_ans")
graph_builder.add_edge("get_ans",END)

graph = graph_builder.compile()

def main():
    query = input("Enter Query:")
    state = {
        "query":query,
        "llm_result":None
    }
    graph_result = graph.invoke(state)
    print(graph_result)

main()



