import os
import asyncio
import sys
sys.path.insert(-1,r"..\..\Agents")
from dotenv import load_dotenv
import requests
load_dotenv()
from Utils.helpers import *
from langsmith import utils
utils.tracing_is_enabled()
from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright
from pydantic import BaseModel, Field
from typing import Annotated

from langchain_core.tools import tool
from openai import OpenAI
from langgraph.prebuilt import create_react_agent

@tool
def save_code(
	code:Annotated[str,"Extract the code in the response of AI then save them in the directory "],
	directory: Annotated[str,"the root directory folder that the code is saved,"],
	file_name: Annotated[str,"name of file save code with suitable extension of file_name"]
):
	"""Use this to make new folder and save code into right psoition of that folder."""
	os.makedirs(directory,exist_ok=True)
	try:
		with open(os.path.join(directory,file_name),"w") as file:
			file.write(code)
		return "success"
	except Exception as e:
		return e
@tool
def gen_imgs(
	description: Annotated[str,"The description of the image"]
	):
	"""Use this to call api to Dall E model to generate image. The result is return in URL, you can check it by visit the url"""
	prompt = f"Generate a image that is suitable fo this description {description}"
	client = OpenAI()

	response = client.images.generate(
	model="dall-e-3",
	prompt=prompt,
	n=1,
	size="1024x1024",
    quality="standard",
	)
	image_url = response.data[0].url


	return f"Here is the url of the images: {image_url}"

@tool
def save_imgs(
    url:Annotated[str,"the url of the images that generated from Dall-e"],
    image_name:Annotated[str,"the name that the image should be save"],
    root_folder:Annotated[str,"the root folder of project"]
):
    """
    Use this function to save image that generated from url in the specific path.
    """
    file_name = os.path.join(root_folder,image_name)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Ảnh đã được lưu tại {file_name}")
    else:
        print(f"Không thể tải ảnh. Mã lỗi: {response.status_code}")
    
@tool
def find_image_path(
    path:Annotated[str,"The relative path of root folder that contains the project"]
):
    """
    Use this function to find the path link to the image that need for coding.
    All the images are saved in the workspace with the semantic name.
    """
    paths = []
    image_extensions = ['jpg','png']
    for root,_,files in os.walk(path):
        for file_name in files:
            if file_name[-3:] in image_extensions:
                paths.append(files)
    return paths
@tool
def search_and_extract(
    url: Annotated[str,"The url that need to be read and extract information."]
):
    """This function is used to crawl all the href that link to the articles of this site if this site contains many articles.
    Request and get the content of the page. 
    Extract the all the hrefs """
    
    print("##### Crawling data href #######")
    html_content = request_url(url)
        
    soup = BeautifulSoup(html_content, "html.parser")
    hrefs = [(a.get_text(strip = True), a.get("href")) for a in soup.find_all("a") if a.get("href")]
    clean_texts = [text.strip() +"  link: "+ href.strip() for text,href in hrefs if text.strip()]
    final_text = "\n".join(clean_texts)    
    client = OpenAI()
    print("######## Processing href #######")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "assistant", "content": "You are my assistant that help me extract the right information that I need."},
            {
                "role": "user",
                "content": f"""
                    Here is the data I crawl from web, I filterd it and just get the content of the site.
                    I need you extract for me in the exactly way the information I need.
                    Extract all the name, the href that link to the article, and the date when article posted.
                    I just need you return for 3 latest articles.
                    You should read the name and decide that it is the name of article or not. If not, do not extract.
                    You have to return the information in json type, DO NOT return anything else.
                    The keys of json are: 'href','date_posted'
                    Here is the text I need you extract:
                    {final_text}
                    """
            }
        ],
    )
    json_string = response.choices[0].message.content
    
    return process_json(json_string)


@tool
def extract(
    url:Annotated[str,"The url of article that needed to be extract information"]
    ):
    
    
    """
    This function is used for extract and retrieve the information from raw text from an article
    """
    print("##### Crawling data #######")
    html_content = request_url(url)
        
    soup = BeautifulSoup(html_content, "html.parser")
    texts = soup.find_all(text=True)
    clean_texts = [text.strip() for text in texts if text.strip()]
    final_text = "\n".join(clean_texts)    
    client = OpenAI()
    print("######## Processing #######")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=500,
        messages=[
            {"role": "assistant", "content": "You are my assistant that help me retrieve the main content of articles"},
            {
                "role": "user",
                "content": f"""
                    Here is the data I crawl from web, I filterd it and just get the content of the site.
                    I need you retrieve for me in the main content of the article in a short paragraph.
                    This article is a raw html that I filterd and get text only.
                    Retrieve and summary the main content of this article in a short essay(about 500 words).
                    Here is the text I need you retrieve:
                    {final_text}
                    """
            }
        ],
    )
    res = response.choices[0].message.content
    # print(json_string)
    
    return res

@tool
def save_report(
    text:Annotated[str,"The text that needed to be saved"],
    path:Annotated[str,"The file name in txt format"]):
    
    """
    Use this to save the generated report to txt
    """
    try:
        with open(path,"w") as file:
            file.write(text)
        return "Save succes"
    except:
        return "failed to save"
            
def create_agent(llm,tools):
    research_agent = create_react_agent(
    llm, tools=tools, prompt="You are a researcher. DO NOT do any math.",name="researcher")
    return research_agent

if __name__=="__main__":
    # print(search_and_extract("https://blog.injective.com/"))
    print(extract("https://blog.injective.com/introducing-the-new-injective-ambassador-program/"))
        
        

