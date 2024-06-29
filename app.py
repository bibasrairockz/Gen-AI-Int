import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from openai import OpenAI

# Function to get all links on a page
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        link = urljoin(url, link)
        if urlparse(link).netloc == urlparse(url).netloc:
            links.add(link)
    return links

# Function to get text from a page
def get_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = soup.stripped_strings
        return ' '.join(texts)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ''

def crawl_website(base_url):
    visited = set()
    to_visit = set([base_url])
    texts = []

    visited.add(base_url)
    # print(f'Crawling= {base_url}')
    try:
    # texts.append(get_text(url))
        links = get_links(base_url)
        # print(links, len(links))
    except Exception as e:
        print(f'Failed to crawl: {base_url} ({e})')
    
    return links

def llm_call(prompt, text):
    openai = OpenAI(
    api_key= 'openai_key'
    )

    message = [
        {"role":"user", "content": prompt},
        {"role":"user", "content": text}
    ]

    response= openai.chat.completions.create(
        messages= message,
        model= "gpt-3.5-turbo"
    )

    return response.choices[0].message.content


base_url = 'https://lottie.org/'
links = crawl_website(base_url)

full_text = ' '.join(links)
# print(full_text)
# with open('links.txt', 'w', encoding="utf-8") as file:
#     file.write(full_text)

ques= ["What does the startup do?", "Startup Industry?", "Who are their customers? B2B/B2C", 
       "Have they raised funds before? If yes, provide details", "Startup Geography?"]

for i in ques:
    prompt = f"""From the list of links, select the one that is most 
    likely to contain information about {i}. Return only the link."""
    # print(full_text)
    link_result= llm_call(prompt, full_text)
    print("link result= ", link_result)

    link_content= get_text(link_result)
    with open('link_content.txt', 'w', encoding="utf-8") as file:
        file.write(link_content)
    
    prompt = f"""Based on the provided information, answer the following 
    question: {i}. Please return only the answer."""
    content_result= llm_call(prompt, full_text)

    print(f">{i}\n>content result= ", content_result, "\n")
    with open('content_result.txt', 'w', encoding="utf-8") as file:
        file.write(content_result)

