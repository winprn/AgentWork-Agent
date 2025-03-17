import sys
sys.path.insert(-1,r"..\..\AgentWork-Agent")

from AgentsHub.Supervisor import *
from AgentsHub.Crawl_news_agent import *
from langchain_openai import ChatOpenAI
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgres://postgres:123456@140.245.117.232:5432/postgres"
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}
pool =  ConnectionPool(
    # Example configuration
    conninfo=DB_URI,
    max_size=40,
    kwargs=connection_kwargs,
)
checkpointer = PostgresSaver(pool)
checkpointer.setup()

def create_report_team(id_thread = "test"):
    llm = ChatOpenAI(model = "gpt-4o-mini")
    crawler = Agent(name="Crawler",
                    description="",
                    prompts="""Your are a researcher,use some tools to search and crawl some useful information.
                    if the result return the href, it is just the href that link to the main article.
                    Then you need to use 'extract' function to get the whole content of the article.
                    I need the out should contain the main content of the news and the url to that article
                    """,
                    tools = [search_and_extract,extract],
                    llm = llm, checkpointer=checkpointer,
                    id_thread=id_thread)

    Content_creator = Agent(name="Content_creator",
                     description="",
                     prompts = "You are a Content creater. According to the content that was extracted,"
                     "write for me an esssay about the main content of all the news. "
                     "Write it as a post to facebook, twitter, .... With each news, I need you provide the link that link to that news."
                     "Then, save that post to my computer",
                     llm = llm,
                     tools=[save_report],
                     checkpointer=checkpointer,
                     id_thread=id_thread)
    reader = Agent(name="reader",
               description="",
               tools=[extract],
               prompts="You are a reader, read the content in a specifice url and summary it.",
               llm=llm,
               checkpointer=checkpointer,
               id_thread=id_thread)

    project_manager = Agent(name="Project_manager",
               description="",
               tools=[],
               prompts="You are a project manager, Your responsible is communicate with custom"
                        "You will get the information of progress of task"
                        "You need to answer the question of custom about the task",
               llm=llm,
               checkpointer=checkpointer,
               id_thread=id_thread)


    agents = [crawler,Content_creator,reader,project_manager]

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
    a = graph.make_request("Tôi vừa nhờ bạn làm gì ấy nhỉ",stream = False,save_progress=None)
    print(a)
    # breakpoint()
