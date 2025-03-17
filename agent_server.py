from fastapi import FastAPI
import sys
sys.path.insert(-1,r"..\..\*")
from Agent_team_2.WriteReport import *
from Agent_team_1.CodeWeb import *

from pydantic import BaseModel

class body(BaseModel):
    id:str
    request:str
    id_thread:str

app = FastAPI()

# graph_team_2 = create_report_team()
# graph_team_1 = create_software_team()

# job_list = {"1":graph_team_1,
#             "2":graph_team_2}


@app.get('/{id}')
async def index(id):
    # breakpoint()
    return {'hello':"test"}


@app.post('/invoke')
async def invoke(req:body):
    if req.id == 1:
        team = create_software_team(req.id_thread)
    else:
        team = create_report_team(req.id_thread)
    return {'output':team.make_request(req.request)}