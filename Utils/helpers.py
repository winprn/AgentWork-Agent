import json
from playwright.sync_api import sync_playwright

def request_url(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("networkidle",timeout=50000)
            page.wait_for_timeout(10000)  
            html_content = page.content()
            browser.close()
        return html_content
    except Exception as e:
        print(e)
        return
    
def process_json(json_string:str):
    json_string = json_string.replace("```json\n", "").replace("\n```", "")
    json_data = json.loads(json_string)
    return json_data 