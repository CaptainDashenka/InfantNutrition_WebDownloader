import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
import re

def save_markdown(content, url, depth):
    # Sanitize the URL to create a valid filename
    filename = re.sub(r'[^a-zA-Z0-9]', '_', url)
    directory = f"data/depth_{depth}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, f"{filename}.md")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def crawl(url, depth, max_depth, visited):
    if depth > max_depth or url in visited:
        return
    visited.add(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    markdown_content = md(str(soup))
    save_markdown(markdown_content, url, depth)
    print(f"Saved contents of URL: {url}")

    if depth < max_depth:
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            if not next_url.startswith('http'):
                next_url = requests.compat.urljoin(url, next_url)
            #include only links to the same domain and exclude same page references
            if next_url.lower().startswith(url.lower()[:35]) and '#' not in next_url:
                crawl(next_url, depth + 1, max_depth, visited)

def main(urls):
    max_depth = 2
    visited = set()
    for url in urls:
        crawl(url, 0, max_depth, visited)

if __name__ == "__main__":
    urls_to_crawl = [
        "https://www.myplate.gov/life-stages/infants",
        "https://www.cdc.gov/nutrition/infantandtoddlernutrition/index.html",
        "https://www.nhs.uk/conditions/baby/weaning-and-feeding/",
        "https://www.mayoclinic.org/healthy-lifestyle/infant-and-toddler-health/in-depth/breastfeeding-nutrition/art-20046912"
    ]
    main(urls_to_crawl)
