from playwright.sync_api import sync_playwright, Playwright
from rich import print
import re
import unidecode

def slugify(text):
    text = unidecode.unidecode(text)          # Convert accented chars to ASCII
    text = text.lower()                        # Lowercase
    text = re.sub(r'[^\w\s-]', '', text)       # Remove punctuation
    text = re.sub(r'[\s_-]+', '-', text)       # Replace space/_ with dash
    return text.strip('-')
def slugifylim(text, max_chars=3):
    text = unidecode.unidecode(text)          # Convert accented chars to ASCII
    text = text.lower()                        # Lowercase
    text = re.sub(r'[^\w\s-]', '', text)       # Remove punctuation
    text = re.sub(r'[\s_-]+', '-', text)       # Replace space/_ with dash
    text = text.strip('-')
    return text[:max_chars]  # ✅ Return first 5 chars
def slug_starts_match(a, b):
    return slugifylim(a) == slugifylim(b)

def slug_match(str1, str2):
    return slugify(str1) == slugify(str2)

def clean_money(raw):
    # Replace non-breaking space and newline
    cleaned = raw.replace('\xa0', ' ').replace('\n', ' ').strip()
    
    # Optional: format it nicely with parentheses
    match = re.match(r'(Rs[\d,]+)\s*~?([\d\s\w\+]+)?', cleaned)
    if match:
        base = match.group(1)
        approx = match.group(2)
        if approx:
            return f"{base} (~{approx.strip()})"
        else:
            return base
    return cleaned

def run(playwright: Playwright):
    targets = [
    {"minister": "Yogender Chandolia", "constituency": "North West Delhi"},
    ]
    start_url = "https://www.myneta.info/"
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)
    for target in targets: 
        # dropdown_button = page.locator('a.nav-link.dropdown-toggle >> i.fas.fa-search')
        # dropdown_button.click()
        page.locator('input[name="q"]').fill(target['minister'])
        page.locator('body > div:nth-child(1) > form > table > tbody > tr > td:nth-child(2) > input').click()
        page.wait_for_timeout(5000)
        names =  page.locator('body > div.w3-container > div.w3-responsive > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > a')
        constituency = page.locator('body > div.w3-container > div.w3-responsive > table > tbody > tr > td:nth-child(3)')
        for i in range(names.count()):
            ele = names.nth(i).inner_text().strip()
            cn = constituency.nth(i).inner_text().strip()
            print(ele)
            print(cn)
            print(slug_starts_match(cn,target['constituency']) and slug_starts_match(ele,target['minister']))
            if slug_starts_match(cn, target['constituency']) and slug_starts_match(ele, target['minister']):
                print(f"✅ Match found: {ele} - {cn}")

                page.locator('body > div.w3-container > div.w3-responsive > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > a').nth(i).click()
                page.wait_for_load_state()

                print("🔗 Visited:", page.url)
                table = page.locator('table.w3-table.w3-striped.w3-centered')
                rows = table.locator('tr')
                data = []
                for i in range(rows.count()):
                    row = rows.nth(i)
                    # Get all <td> or <th> in the row
                    cells = row.locator('td, th')
                    row_data = []

                    for j in range(cells.count()):
                        # Get all visible text, including <b> and <span>
                        cell_html = cells.nth(j).inner_html()
                        # Strip tags manually if needed, or just use plain text:
                        cell_text = cells.nth(j).inner_text().strip()
                        if 'Rs' in cell_text:
                            cell_text = clean_money(cell_text)
                        row_data.append(cell_text)

                    data.append(row_data)

                for row in data:
                    print(row)
                cases = page.locator('body > div.w3-container > div.w3-small').inner_text().strip()  
                print(cases)          
                page.go_back()
                page.wait_for_load_state()

                match_found = True
                break
        # print(slug_starts_match(ele,'Yogender Chandolia'))
    
    # page.wait_for_load_state('networkidle')
    # breadcrumb_divs = page.locator('a.gs-title')
    # count = breadcrumb_divs.count()
    # target_slug = "Yogender Chandolia"
    # found = False
    # for i in range(count):
    #     b_tags = breadcrumb_divs.nth(i).locator('b')
    #     b_count = b_tags.count()
    #     b_texts = [b_tags.nth(j).inner_text().strip() for j in range(b_count)]
    #     print(b_texts)
    #     if any(target_slug in text for text in b_texts):
    #         print(f"✅ Match found in result {i}: {b_texts}")
    #         found = True
    #         # breadcrumb_divs.nth(i).click()
    #         # page.wait_for_timeout(5000)
    #         with page.expect_popup() as popup_info:
    #             breadcrumb_divs.nth(i).click()

    #         new_page = popup_info.value
    #         new_page.wait_for_load_state()
    #         print(new_page.url)
    #         break
    # if not found:
    #     print("❌ No matching slug found.")

        
    
with sync_playwright() as playwright:
    run(playwright)    