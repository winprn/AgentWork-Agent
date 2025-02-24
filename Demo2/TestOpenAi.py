from openai import OpenAI
from dotenv import load_dotenv
from typing import List
from bs4 import BeautifulSoup
load_dotenv()

client = OpenAI()

from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: List[str]
    href: List[str]
    date: List[str]

from playwright.sync_api import sync_playwright

url = "https://blog.injective.com/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle",timeout=50000)
    page.wait_for_timeout(10000)  
    html_content = page.content()
    # print(len(html_content))
    browser.close()


soup = BeautifulSoup(html_content, "html.parser")
hrefs = [(a.get_text(strip = True), a.get("href")) for a in soup.find_all("a") if a.get("href")]
# print(hrefs)
# # Lấy nội dung của tất cả các thẻ
# texts = soup.find_all(text=True)

# Lọc bỏ các khoảng trắng dư thừa
clean_texts = [text.strip() +"  link: "+ href.strip() for text,href in hrefs if text.strip()]

# print(len("\n".join(clean_texts)))
# print(len(clean_texts))
final_text = "\n".join(clean_texts)
# print(final_text)

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "assistant", "content": "bạn là 1 trợ lý trihcs xuất thông tin. Việc của bạn là đọc html, rồi trích xuất ra thông tin theo yêu cầu của tôi"},
        {
            "role": "user",
            "content": f"""Hãy đọc và trích xuát ra nhưgnx thông tin(tiêu đề, link href, ngày đăng) của những thông báo, bài viết trong kia:{final_text},
            bạn đọc rồi trích xuát luôn, không code.
                """
        }
    ],
    response_format=CalendarEvent
)

print(completion.choices[0].message)