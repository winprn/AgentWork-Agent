import sys
sys.path.insert(-1,r"..\..\AgentWork-Agent")

from AgentsHub.Supervisor import *
from AgentsHub.Crawl_news_agent import *
from langchain_openai import ChatOpenAI

def create_report_team():
    llm = ChatOpenAI(model = "gpt-4o-mini")
    crawler = Agent(name="Crawler",
                    description="",
                    prompts="""Your are a researcher,use some tools to search and crawl some useful information.
                    if the result return the href, it is just the href that link to the main article. 
                    Then you need to use 'extract' function to get the whole content of the article.
                    I need the out should contain the main content of the news and the url to that article 
                    """,
                    tools = [search_and_extract,extract],
                    llm = llm)
    
    Content_creator = Agent(name="Content_creator",
                     description="",
                     prompts = "You are a Content creater. According to the content that was extracted," 
                     "write for me an esssay about the main content of all the news. "
                     "Write it as a post to facebook, twitter, .... With each news, I need you provide the link that link to that news."
                     "Then, save that post to my computer",
                     llm = llm,
                     tools=[save_report])
    reader = Agent(name="reader",
               description="",
               tools=[extract],
               prompts="You are a reader, read the content in a specifice url and summary it.",
               llm=llm)
    
    
    agents = [crawler,Content_creator,reader]
    
    super_graph = Supervise_graph(llm=llm,
                                  members = agents,
                                  member_nodes=[a.agent_node for a in agents],
                                  )
    
    return super_graph

if __name__=="__main__":
    with open("Request.txt","r") as file:
        request = file.read()
    # request = "hello."
    graph = create_report_team()
    # print(graph.make_request(request,stream = False,save_progress="Progress.txt"))
    a = graph.make_request(request,stream = True,save_progress="Progress.txt")
    breakpoint()
    