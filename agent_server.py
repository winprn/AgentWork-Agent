from fastapi import FastAPI
import sys
sys.path.insert(-1,r"D:\pypy\Agents")
from Agent_team_2.main import *
from pydantic import BaseModel

class body(BaseModel):
    id:str
    request:str

app = FastAPI()

graph_team_2 = main()
graph_team_1 = main()

job_list = {"1":graph_team_1,
            "2":graph_team_2}
request = """
    This url links to a block that contains many artiles. I need you crawl and summary the information from latest articles of that site.
    After that, summary and write for me a report that can summary all the information. After that save it.
    This is the url: https://blog.injective.com/
    """

@app.get('/{id}')
async def index(id):
    # breakpoint()
    return {'hello':job_list[id].make_request(request)}


@app.post('/invoke')
async def invoke(req:body):
    return {'hello':job_list[req.id].make_request(req.request)}