# pip install requests beautifulsoup4 PyPDF2 pillow
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import PyPDF2
from PIL import Image
from io import BytesIO
import time
import random


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def download_file(url, directory, session):
    response = session.get(url, stream=True)
    local_filename = os.path.join(directory, url.split('/')[-1])
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def save_text(url, directory, session):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    text_file_path = os.path.join(directory, 'website_text.txt')
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(text)


def save_image(url, directory, session):
    response = session.get(url)
    image = Image.open(BytesIO(response.content))
    local_filename = os.path.join(directory, url.split('/')[-1])
    image.save(local_filename)


def human_delay():
    time.sleep(random.uniform(1, 3))


def crawl_website(url):
    # Create the directory to save files
    directory = "websitepdf"
    create_directory(directory)

    # Create a session to maintain cookies
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    # Get the HTML content
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and download all PDFs
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if is_valid_url(full_url) and full_url.endswith('.pdf'):
            download_file(full_url, directory, session)
            human_delay()

    # Extract and save text
    save_text(url, directory, session)
    human_delay()

    # Find and save all images
    for img in soup.find_all('img', src=True):
        src = img['src']
        full_url = urljoin(url, src)
        if is_valid_url(full_url):
            save_image(full_url, directory, session)
            human_delay()


# Example usage
crawl_website('https://intranet.venture.com.sg/HRWeb/index_Singapore_Policy.htm')

