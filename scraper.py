
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_page(url):
    response = requests.get(
        url,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    content = []

    for element in soup.find_all(["h1", "h2", "h3", "p", "img"]):

        if element.name in ["h1", "h2", "h3", "p"]:
            text = element.get_text(" ", strip=True)

            if text:
                content.append({
                    "type": "text",
                    "content": text
                })

        elif element.name == "img":
            image_url = element.get("src")

            if image_url:
                content.append({
                    "type": "image",
                    "content": urljoin(url, image_url)
                })

    return content
