from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from playwright.sync_api import sync_playwright, Playwright
import re
import unidecode

class MinisterInput(BaseModel):
    minister: str
    constituency: str

def slugify(text):
    text = unidecode.unidecode(text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def slugifylim(text, max_chars=3):
    text = slugify(text)
    return text[:max_chars]

def slug_starts_match(a, b):
    return slugifylim(a) == slugifylim(b)

def slug_match(str1, str2):
    return slugify(str1) == slugify(str2)

def clean_money(raw):
    cleaned = raw.replace('\xa0', ' ').replace('\n', ' ').strip()
    match = re.match(r'(Rs[\d,]+)\s*~?([\d\s\w\+]+)?', cleaned)
    if match:
        base = match.group(1)
        approx = match.group(2)
        return f"{base} (~{approx.strip()})" if approx else base
    return cleaned

def scrape_myneta_data(minister: str, constituency: str) -> Dict:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.myneta.info/")

        page.locator('input[name="q"]').fill(minister)
        page.locator('body > div:nth-child(1) > form > table > tbody > tr > td:nth-child(2) > input').click()
        page.wait_for_timeout(5000)

        names = page.locator('body > div.w3-container > div.w3-responsive > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > a')
        constituency_locators = page.locator('body > div.w3-container > div.w3-responsive > table > tbody > tr > td:nth-child(3)')

        for i in range(names.count()):
            ele = names.nth(i).inner_text().strip()
            cn = constituency_locators.nth(i).inner_text().strip()

            if slug_starts_match(cn, constituency) and slug_starts_match(ele, minister):
                names.nth(i).click()
                page.wait_for_load_state()

                table = page.locator('table.w3-table.w3-striped.w3-centered')
                rows = table.locator('tr')
                data = []

                for i in range(rows.count()):
                    row = rows.nth(i)
                    cells = row.locator('td, th')
                    row_data = []
                    for j in range(cells.count()):
                        text = cells.nth(j).inner_text().strip()
                        if 'Rs' in text:
                            text = clean_money(text)
                        row_data.append(text)
                    data.append(row_data)

                cases = page.locator('body > div.w3-container > div.w3-small').inner_text().strip()
                browser.close()

                return {
                    "minister": ele,
                    "constituency": cn,
                    "data_table": data,
                    "criminal_cases": cases
                }

        browser.close()
        raise HTTPException(status_code=404, detail="No matching minister found")

