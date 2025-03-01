import sys
sys.path.insert(-1,r"..\..\AgentWork-Agent")

from JurolAgents.Jurols import create_jurol
from langchain_openai import ChatOpenAI
def vote(jurol_agent,job_request_path, job_progress_path):
    message = f"""Here is the job request path: {job_request_path}
                Here is the job progress path: {job_progress_path}
                Mark the grade for me.
                """
                
    a = jurol_agent.invoke({"messages":message})
    return int(a["messages"][-1].content)
    # breakpoint()
    
    
if __name__=="__main__":
    llm = ChatOpenAI(model="gpt-4o-mini")
    jurol1 = create_jurol(name = "Jurol1",llm=llm)
    
    a = vote(jurol_agent=jurol1,
         job_request_path=r"D:\pypy\AgentWork-Agent\Agent_team_2\Request.txt",
         job_progress_path=r"D:\pypy\AgentWork-Agent\Agent_team_2\Progress.txt")
    print(a)
    