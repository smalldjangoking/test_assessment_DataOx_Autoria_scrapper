from playwright.sync_api import sync_playwright
import time

LAUNCH_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled"
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_links() -> set:
    """Hardcoded first page link aggregator"""
    links = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=LAUNCH_ARGS)
        context = browser.new_context(user_agent=USER_AGENT, viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        page.goto("https://auto.ria.com/uk/car/used/")

        page.wait_for_selector(".standart-view.m-view.result-explore", timeout=20000)
        element = page.query_selector(".standart-view.m-view.result-explore")

        if element:
            elements = element.query_selector_all(".ticket-item")

            for e in elements:
                image = e.query_selector(".ticket-photo")
                if image:
                    link_el = image.query_selector('a')
                    if link_el:
                        href = link_el.get_attribute("href")
                        if href and not "newauto" in href:
                            links.add(href)
        browser.close()
    return links



def get_vehicle_data(links: set) -> dict:
    """Get data by scraping link set"""
    data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print('Starting scrapping')
        
        for link in links:
            print(link)
            page.goto(link)
            page.wait_for_selector("#mainTagTemplate", timeout=20000)
            main_element = page.query_selector("#mainTagTemplate")
            banned = main_element.query_selector("#bannerStatus") if main_element else None
            
            if main_element and not banned:
                title = main_element.query_selector("#basicInfo #basicInfoTitle h1")
                price_usd = main_element.query_selector("#basicInfo #basicInfoPriceRow #basicInfoPriceWrapText #basicInfoPrice strong.titleL")
                odometer = main_element.query_selector("#basicInfo #basicInfoTableMainInfo #basicInfoTableMainInfoInfo #basicInfoTableMainInfo0 span.common-text")
                username = main_element.query_selector("#sellerInfo #sellerInfoUserName span")
                image_url = main_element.query_selector(".carousel__slide--active img")
                images_count = len(main_element.query_selector_all("#photoSlider li.carousel__slide"))
                number = main_element.query_selector(".car-number span")
                car_vin = main_element.query_selector("#badgesVinGrid div .common-text")
                
                title = title.inner_text().strip() if title else None
                price_usd = price_usd.inner_text().strip() if price_usd else None
                odometer = odometer.inner_text().strip() if odometer else None
                username = username.inner_text().strip() if username else None
                image_url = image_url.get_attribute("src") if image_url else None
                number = number.inner_text().strip() if number else None
                car_vin = car_vin.inner_text().strip() if car_vin else None

                try:
                     page.locator('#sellerInfo button.size-large.conversion[data-action="showBottomPopUp"]').first.click()
                     phone_locator = page.locator(".popup-inner button[data-action='call']")
                     phone_locator.wait_for(state="visible", timeout=5000)
                     raw_phone = phone_locator.first.inner_text()
                     phone_number = raw_phone.strip()
    
                except Exception as e:
                    print(f"Не удалось получить номер: {e}")
                    phone_number = None


                data[link] = {
                    "url": link,
                    "title": title,
                    "price_usd": price_usd,
                    "odometer": odometer,
                    "username": username,
                    "image_url": image_url,
                    "images_count": images_count,
                    "car_number": number,
                    "car_vin": car_vin,
                    "phone_number": phone_number
                    }
        browser.close()
        print('Scrapping Finished')
    return data

    
#if __name__ == "__main__":
#    print(get_vehicle_data(get_links()))