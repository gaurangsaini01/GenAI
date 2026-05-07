from fastapi import FastAPI
app =FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import status
import json
from langgraph.types import interrupt, Command
from fastapi import Body
from dotenv import load_dotenv
from graphbuilder import graph
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def home():
    return JSONResponse(content={"message":"Hello from server"},status_code=status.HTTP_200_OK)

@app.post('/generate-email')
def generateEmail(thread_id:str=Body(...),query:str=Body(...)):
    res = graph.invoke({'query':query},config={"configurable":{"thread_id":thread_id}})
    if '__interrupt__' in res:
        interrupt_data = res["__interrupt__"][0].value
        return JSONResponse(content=interrupt_data,status_code=status.HTTP_200_OK)

@app.post('/resume')
def generateEmail(approval_status:bool=Body(...),thread_id:str=Body(...)):
    print(approval_status)
    res = graph.invoke(Command(resume=approval_status),config={"configurable":{"thread_id":thread_id}})
    print(res)
    if '__interrupt__' in res:
        interrupt_data = res["__interrupt__"][0].value
        return JSONResponse(content=interrupt_data,status_code=status.HTTP_200_OK)
    return JSONResponse(content=res['final'],status_code=status.HTTP_200_OK)
    