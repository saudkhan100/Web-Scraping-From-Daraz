from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def scrape_daraz(query, max_products=20):
    # Configure Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for production
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("E:\\WebScrapping\\driver\\chromedriver.exe")  # Update to your path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the Daraz search URL
        url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
        driver.get(url)
        driver.implicitly_wait(10)

        products = []
        seen_items = set()
        scroll_attempts = 0

        while len(products) < max_products and scroll_attempts < 10:
            items = driver.find_elements(By.CLASS_NAME, "Bm3ON")  # Adjusted to Daraz class structure
            for item in items:
                if len(products) >= max_products:
                    break

                try:
                    # Extract product title
                    title_element = item.find_element(By.CSS_SELECTOR, ".RfADt a")
                    title = title_element.get_attribute("title")

                    # Extract product price
                    price_element = item.find_element(By.CSS_SELECTOR, ".ooOxS")
                    price = price_element.text.strip()

                    # Extract product image
                    image_element = item.find_element(By.CSS_SELECTOR, ".picture-wrapper img")
                    image = image_element.get_attribute("src") or image_element.get_attribute("data-src")

                    # Retry loading image if still missing
                    if not image:
                        ActionChains(driver).move_to_element(image_element).perform()
                        time.sleep(0.5)
                        image = image_element.get_attribute("src") or image_element.get_attribute("data-src")

                    # Extract product link
                    link = title_element.get_attribute("href")
                    full_link = f"https://www.daraz.pk{link}" if link.startswith("/") else link

                    # Avoid duplicate products
                    if (title, price, image) in seen_items:
                        continue
                    seen_items.add((title, price, image))

                    # Append product details
                    products.append({
                        "title": title,
                        "price": price,
                        "image_url": image,
                        "link": full_link,
                        "rating": "N/A",  # Placeholder for now
                        "score": "N/A"  # Placeholder for now
                    })
                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue

            # Scroll to load more products
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_attempts += 1

        return products

    finally:
        driver.quit()
