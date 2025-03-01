import sys
sys.path.insert(-1,"..\..\AgentWork-Agent")

from AgentsHub.Supervisor import *
from AgentsHub.Jurol_tools import *
from langchain_openai import ChatOpenAI
from AgentsHub.Crawl_news_agent import *


def create_jurol(name,llm):
    agent = Agent(name=name,
                  llm=llm,
                  description="",
                  tools=[reach_file],
                  prompts = """You are a person who evaluates work results. 
                  Your recieve input as work requirements and a summary of the work process. 
                  In the summary, there are some output files and their paths, you need to read them and return the mark. You can use the reachfile tool 
                  to check the file to see what is in it. Then give an evaluation 
                  of the results on a scale of 1-10. Only give a single number as the 
                  result, do not give anything.
                  The order of work should be as follows:
                first read the job requirements document
                then read the implementation process document
                Check to see which files are exported in the process summary document, 
                the output of this job, if it is exported, need to read the output 
                files to have a comprehensive assessment.
                The results are mainly based on what has been observed in the output files""")
    return agent.agent


if __name__=="__main__":
    llm = ChatOpenAI(model="gpt-4o-mini")
    jurol1 = create_jurol(name = "Jurol1",llm=llm)
    request = """
        Here is the job requirements:"D:\pypy\AgentWork-Agent\Agent_team_1\Request.txt"
        Here is the progress of working:"D:\pypy\AgentWork-Agent\Agent_team_1\Progress.txt"
        Mark the grade for me
    """
    print(jurol1.invoke({"messages":request}))