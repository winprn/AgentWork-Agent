from fastapi import FastAPI
import sys
sys.path.insert(-1,r"D:\pypy\Agents")
from Agent_team_2.WriteReport import *
from Agent_team_1.CodeWeb import *

from pydantic import BaseModel

class body(BaseModel):
    id:str
    request:str

app = FastAPI()

graph_team_2 = create_report_team()
graph_team_1 = create_software_team()

job_list = {"1":graph_team_1,
            "2":graph_team_2}


@app.get('/{id}')
async def index(id):
    # breakpoint()
    return {'hello':job_list[id].make_request(request)}


@app.post('/invoke')
async def invoke(req:body):
    return {'output':job_list[req.id].make_request(req.request)}