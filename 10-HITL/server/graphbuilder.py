from langgraph.graph import StateGraph,END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage , BaseMessage
from typing import List
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.types import interrupt, Command
from dotenv import load_dotenv
load_dotenv()

model = init_chat_model("openai:gpt-5.4-mini")
class ResponseClass(TypedDict):
    query:str
    messages:Annotated[List[BaseMessage],add_messages]
    draft:str
    final:str
    approval_status:bool

# //Nodes
def initiate(state):
    query = state['query']
    messages = [(HumanMessage(content=query))]
    res = model.invoke(messages)
    return {'draft':res.content}

def get_human_approval(state):
    draft = state['draft']
    res = interrupt({"draft":draft})
    return {'approval_status':res}

def check_approval_status(state):
    approval_status = state['approval_status']
    if approval_status == True:
        return 'generate_final_draft'
    else:
        return 'initiate'
def generate_final_draft(state):
    draft = state['draft']
    return {'final':draft}

    
graph_builder = StateGraph(ResponseClass)
graph_builder.add_node('initiate',initiate)
graph_builder.add_node('get_human_approval',get_human_approval)
graph_builder.add_node('check_approval_status',check_approval_status)
graph_builder.add_node('generate_final_draft',generate_final_draft)

# Edges
graph_builder.set_entry_point('initiate')
graph_builder.add_edge('initiate','get_human_approval')
graph_builder.add_conditional_edges('get_human_approval',check_approval_status)
graph_builder.add_edge('generate_final_draft',END)

checkpointer = MemorySaver()
graph = graph_builder.compile(checkpointer)
