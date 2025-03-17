import sys
sys.path.insert(0,r"..\..\AgentWork-Agent")

from AgentsHub.Supervisor import *
from AgentsHub.Crawl_news_agent import *
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults


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


def create_software_team(id_thread = "test2"):
    llm = ChatOpenAI(model = "gpt-4o")
    toolsearch  = TavilySearchResults(max_results=5)

    Researcher = Agent(name="Researcher",
                    description="",
                    prompts="""You are a researcher. Your responsibility is find some boosttrap or tailwind
                    for Dev to code web.
                    """,
                    tools = [toolsearch],
                    llm = llm,
                    checkpointer=checkpointer,
                    id_thread=id_thread)

    Design_images = Agent(name="Design_images",
                    description="",
                    prompts="""You are a Designer. Your responsibility is generating  some images
                    for Dev to code web. You have to just return the image url. After that, you save the image
                    in the specific path with extension name is jpg and provide the path for developer by using save_imgs function.
                    You need to provide exactly path to the images for Developer.
                    You need to save in jpg format with .jpg extension.
                    """,
                    tools = [gen_imgs,save_imgs],
                    llm = llm,
                    checkpointer=checkpointer,
                    id_thread=id_thread)

    Dev = Agent(name="Developer",
                    description="",
                    prompts="""You are a developer that can code Front end.
                    You can use some resource from Designer images agents (path of image that need for web).
                    If you need some images, you have to use the paths that provided by Designer in the exactly way.
                    and some boosttrap and tailwind from researcher.
                    You have to use the find_image_path function to find the path to suitable image.
                    You just only return code. Save code(donot ask anything to user).
                    """,
                    tools = [save_code,find_image_path],
                    llm = llm,
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

    agents = [Dev,Researcher,Design_images,project_manager]

    super_graph = Supervise_graph(llm=llm,
                                  members = agents,
                                  member_nodes=[a.agent_node for a in agents],
                                  )

    return super_graph

if __name__=="__main__":
    with open("Request.txt","r") as file:
        request = file.read()
    graph = create_software_team()
    print(graph.make_request("Gen lại cho tôi  ảnh logo khác đi",stream = False,save_progress="Progress.txt"))
    # print(graph.graph.get_state())
