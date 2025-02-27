import os
import sys
sys.path.insert(-1,r"..\..\AgentWork-Agent")
from dotenv import load_dotenv
import requests
load_dotenv()
from Utils.helpers import *
from langsmith import utils
utils.tracing_is_enabled()


from typing import Annotated

from langchain_core.tools import tool
from openai import OpenAI
from langgraph.prebuilt import create_react_agent


@tool
def reach_file(
    path_file:Annotated[str,"The path of the file need to read and check"]
):
    """
    This function is used for reading some file: txt,html,css,py,etc
    """
    try:
        with open(path_file,"r") as file:
            content = file.read()
    except Exception as e:
        return e
    return content


