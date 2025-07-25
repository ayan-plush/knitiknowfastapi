from fastapi import APIRouter
from app.models.schemas import ItemList
from app.models.schemas import MinisterRequest
from app.services.scrape_google_news import scrape_google_news
from app.services.scraper_toi import scraper_toi
from app.services.playwright_scraping_prs import playwright_scraping_prs
from app.services.playwright_scraping_prs import playwright_scraping_prs
from app.services.playwright_scraping_myneta import scrape_myneta_data
from app.services.test_vector import vectorizeArticle
from app.models.schemas import MinisterInput
router = APIRouter()

@router.post("/scrapegn")
def scrapegn(data: ItemList):
    return {"results": scrape_google_news(data.ministers)}

@router.post("/scrape")
def scrapetoi(data: ItemList):
    return {"results": scraper_toi(data.ministers)}

@router.post("/scrape-deb")
def scrapedebates(data: MinisterRequest):
    return {"results": playwright_scraping_prs(data)}

@router.post("/scrape-myneta")
def scrape_myneta(input_data: MinisterInput):
    result = scrape_myneta_data(input_data.minister, input_data.constituency)
    return {"result": result}

@router.post("/vectorTest")
def vectorTest():
    result = vectorizeArticle()
    return {result}
