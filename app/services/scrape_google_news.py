from curl_cffi import requests
from rich import print
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings


def scrape_google_news(ministers: list[str]):
    for minister in ministers:
        query = minister
        base_url = "https://news.google.com"
        rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '%20')}&hl=en-IN&gl=IN&ceid=IN:en"

        resp = requests.get(rss_url)
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(resp.content, "html.parser")
        print(len(soup.select("article")))
        for article in soup.select("article"):
            a_tag = article.find("a")
            if a_tag and "href" in a_tag.attrs:
                relative_url = a_tag["href"]
                if relative_url.startswith("./articles"):
                    full_url = base_url + relative_url[1:]
                    try:
                        final_url = requests.get(full_url, allow_redirects=True).url
                        print("✅ Actual Article:", final_url)
                    except:
                        print("❌ Failed to follow:", full_url)
            else:
                print("no a found")            

        # for item in soup.find_all("item"):
            # title = item.title.text
            # description_html = item.description.text

            # # Parse HTML inside description
            # desc_soup = BeautifulSoup(description_html, "html.parser")
            # anchor = desc_soup.find("a")
            # real_url = anchor['href'] if anchor else None
            # anchor_text = anchor.text if anchor else None

            # print("📰", title)
            # print("📍 Site Shown:", anchor_text)
            # print("🔗 URL from <a>:", real_url)