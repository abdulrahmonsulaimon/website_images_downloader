import requests
import os
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin, urlparse
from halo import Halo
# from pprint import pprint


# url = "https://www.adobe.com/express/learn/blog/graphic-design-portfolio"
url = ""
html = ""

try:
    _, url = sys.argv
    
except ValueError as err:
    sys.exit(f"Requires 2 args: python <file> <url>")
    
os.makedirs("images", exist_ok=True)

images_src = []

with Halo(text="Fetching the webpage...", spinner="dots"):
    res = requests.get(url)
    res.raise_for_status()
    html = res.text

soup = BeautifulSoup(html, 'html.parser')

for image in soup.find_all('img'):
    if image["src"].startswith("."):
        image["src"] = image["src"][1:]
           
    images_src.append(f"{url}{image["src"]}")

if images_src:
    for idx, img in enumerate(images_src):
            spinner = Halo(text=f"Downloading image {idx + 1}/{len(images_src)}...", spinner="dots")
            spinner.start()
            
            try:
                img_data = requests.get(img).content
                
                parsed_url = urlparse(img)
                _, ext = os.path.splitext(parsed_url.path)
                
                ext = ext.lower() if ext.lower() in ['.jpg', '.jpeg', '.png'] else '.jpg'
                
                img_name = os.path.join("images", f"image_{idx + 1}{ext}")
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_data)
                    spinner.succeed(f"Downloaded {img_name}")
                
            except Exception as e:
                spinner.fail(f"Failed to download image {idx + 1}: {e}")

else:
    print("No image found.")

print("Done!")