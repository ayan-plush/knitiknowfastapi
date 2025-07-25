from playwright.sync_api import sync_playwright, TimeoutError
from fastapi import HTTPException
from pydantic import BaseModel

class MinisterRequest(BaseModel):
    minister: str

def playwright_scraping_prs(req: MinisterRequest):
    target_slug = req.minister.strip()
    browser = None

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            print("[INFO] Going to prsindia.org...")
            page.goto("https://prsindia.org/", timeout=30000)

            try:
                page.locator('a.nav-link.dropdown-toggle >> i.fas.fa-search').click()
                page.locator('input[name="search_block_form"]').fill(target_slug)
                page.locator('form.searchformg button[type="submit"]').click()
                print("[INFO] Clicking search icon...")
                page.wait_for_load_state('networkidle', timeout=30000)
            except TimeoutError:
                raise HTTPException(status_code=504, detail="⏱️ Timeout during initial navigation/search")

            # Parse search results
            breadcrumb_divs = page.locator('a.gs-title')
            count = breadcrumb_divs.count()
            print("[INFO] Search results found:", count)

            if count == 0:
                raise HTTPException(status_code=404, detail="❌ No results found.")

            for i in range(count):
                try:
                    b_tags = breadcrumb_divs.nth(i).locator('b')
                    b_count = b_tags.count()
                    b_texts = [b_tags.nth(j).inner_text().strip() for j in range(b_count)]

                    if any(target_slug.lower() in text.lower() for text in b_texts):
                        print(f"✅ Match found: {b_texts}")

                        with page.expect_popup() as popup_info:
                            breadcrumb_divs.nth(i).click()

                        new_page = popup_info.value
                        new_page.wait_for_load_state(timeout=15000)

                        print("🆕 New page URL:", new_page.url)

                        new_page.wait_for_selector(
                            '#block-views-mps-debate-related-views-block > div > div > table > tbody > tr',
                            timeout=10000
                        )

                        rows = new_page.locator(
                            '#block-views-mps-debate-related-views-block > div > div > table > tbody > tr'
                        )
                        row_count = rows.count()
                        print(f"📄 Found {row_count} rows")

                        debates = []
                        for j in range(row_count):
                            try:
                                row = rows.nth(j)
                                date = row.locator('td').nth(0).inner_text().strip()
                                title_link = row.locator('td').nth(1).locator('a')
                                title = title_link.inner_text().strip()
                                link = title_link.evaluate("el => el.href")
                                debate_type = row.locator('td').nth(2).inner_text().strip()

                                if link and link.startswith('/'):
                                    link = f"https://prsindia.org{link}"

                                debates.append({
                                    "date": date,
                                    "title": title,
                                    "link": link,
                                    "debate_type": debate_type
                                })
                            except Exception as row_err:
                                print("⚠️ Skipping broken row:", row_err)
                                continue

                        return debates
                except Exception as item_err:
                    print("⚠️ Skipping broken search result item:", item_err)
                    continue

            raise HTTPException(status_code=404, detail="❌ No matching minister found in search results.")
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"⚠️ Scraping error: {e}")
    finally:
        if browser:
            browser.close()
