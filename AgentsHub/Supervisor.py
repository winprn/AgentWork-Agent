from typing import Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
class State(MessagesState):
    next: str

class Agent:
    def __init__(self,name,description,tools,prompts,llm):
        self.name = name
        self.description = description
        self.tools = tools
        self.prompts = prompts
        self.llm = llm
        self.agent = self.create()
    
    def create(self):
        agent = create_react_agent(llm = self.llm,
                                   tools = self.tools,
                                   prompt = self.prompts,
                                   name = self.name)
        return agent
    
    def create_node(self,state: State):
        result = self.agent.invoke(state)
        return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="researcher")
            ]
        },
        goto="supervisor",
    )






class Supervise_graph():

    def __init__(self,llm = ChatOpenAI(model = "gpt-4o"), 
                 members = [""],
                 member_nodes = [], 
                 job_description ="", 
                 prompt = ""):
        self.members = [member.agent for member in members if  isinstance(member,Agent) ]
        self.member_names = [member.name for member in members if  isinstance(member,Agent)]
        self.member_nodes = member_nodes
        self.job_description = job_description
        self.promt = prompt
        self.options = members+["FINISH"]
        self.llm = llm
        self.Router.__annotations__["next"] = Literal[*self.options]

    def get_member_names(self):
        return self.member_names
    
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: str
    def supervisor_node(self,state: State):
        messages = [
            {"role": "system", "content": self.prompt},
        ] + state["messages"]
        response = self.llm.with_structured_output(Supervise_graph.Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})   
    
    def build_graph(self):
        builder = StateGraph(State)
        builder.add_edge(START, "supervisor")
        builder.add_node("supervisor", self.supervisor_node)
        for i in range(self.member_nodes):
            builder.add_node(self.member_names[i],self.member_nodes[i])
        graph = builder.compile()
        return graph

if __name__=="__main__":
    super_graph = Supervise_graph()
    
    
    
    
    
    