import os

import numpy as np
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse, urljoin
import cv2

def is_absolute(url):
    """Check if the URL is an absolute URL."""
    return bool(urlparse(url).netloc)

def download_images(query, limit, save_directory):
    query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={query}&tbm=isch&hl=en&chips=q:{query},g_1:high+quality&biw=1366&bih=657"

    # Perform Google Image search
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    # Download and resize images
    count = 0
    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url:
            if not is_absolute(img_url):
                img_url = urljoin(search_url, img_url)  # Convert relative URL to absolute URL

            try:
                img_data = requests.get(img_url).content
                img_array = cv2.imdecode(np.frombuffer(img_data, np.uint8), -1)
                resized_img = cv2.resize(img_array, (300, 300), interpolation=cv2.INTER_AREA)
                cv2.imwrite(os.path.join(save_directory, f"{count}.jpg"), resized_img)
                count += 1
            except Exception as e:
                print(f"Error downloading image: {e}")

            if count >= limit:
                break

if __name__ == "__main__":
    query = input("Enter the name of the person you want to download images of: ")
    limit = 200  # Number of images to download
    save_directory = r'C:\Users\Administrator\Desktop\Project Proposal\Trials\uhuru'

    download_images(query, limit, save_directory)
