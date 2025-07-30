# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import requests

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS for the frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def scrape_daraz(query: str, page: int = 1, max_products: int = 40):
#     """
#     Scrape Daraz Pakistan for products based on the search query.

#     Args:
#         query (str): Search query for Daraz.
#         page (int): The page number to fetch products from.
#         max_products (int): Maximum number of products to scrape per page.

#     Returns:
#         list: A list of dictionaries containing product details and reviews.
#     """
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--disable-extensions')
#     options.add_argument('--start-maximized')

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}&page={page}"
#     driver.get(url)

#     products = []

#     try:
#         wait = WebDriverWait(driver, 15)

#         # Wait for product elements to load
#         product_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Bm3ON')))

#         # Scroll through product elements to ensure lazy-loaded images are fully loaded
#         for product in product_elements:
#             driver.execute_script("arguments[0].scrollIntoView({ behavior: 'instant', block: 'center' });", product)
#             time.sleep(0.1)  # Brief pause for lazy-loaded content to appear

#         # Fetch product details
#         for product in product_elements:
#             if len(products) >= max_products:
#                 break
#             try:
#                 # Extract product details
#                 title_element = product.find_element(By.CSS_SELECTOR, '.RfADt a')
#                 title = title_element.get_attribute("title")
#                 link = title_element.get_attribute('href')

#                 price_element = product.find_element(By.CSS_SELECTOR, '.ooOxS')
#                 price_text = price_element.text.strip()
#                 price = parse_price(price_text)

#                 image_element = product.find_element(By.CSS_SELECTOR, '.picture-wrapper img')
#                 image_url = image_element.get_attribute("src") or image_element.get_attribute("data-src")

#                 # Extract additional details
#                 star_count = extract_star_count(product)
#                 review_count = extract_review_count(product)
#                 sold_count = extract_sold_count(product)

#                 # Append product details
#                 products.append({
#                     "title": title,
#                     "link": link,
#                     "price": price,
#                     "image_url": image_url,
#                     "stars": star_count,
#                     "reviews": review_count,
#                     "sold_count": sold_count
#                 })
#             except Exception as e:
#                 print(f"Error processing product: {e}")
#                 continue

#     finally:
#         driver.quit()

#     return products


# def extract_star_count(product):
#     """
#     Extract star rating for a product.

#     Args:
#         product: Web element representing the product.

#     Returns:
#         int: Star rating count.
#     """
#     try:
#         stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
#         return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
#     except Exception:
#         return 0


# def extract_review_count(product):
#     """
#     Extract review count for a product.

#     Args:
#         product: Web element representing the product.

#     Returns:
#         str: Review count as a string.
#     """
#     try:
#         review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
#         return review_count_element.text.strip().replace("(", "").replace(")", "")
#     except Exception:
#         return "No reviews"


# def extract_sold_count(product):
#     """
#     Extract sold count for a product.

#     Args:
#         product: Web element representing the product.

#     Returns:
#         str: Sold count as a string.
#     """
#     try:
#         sold_count_element = product.find_element(By.CSS_SELECTOR, '._1cEkb span')
#         return sold_count_element.text.strip()
#     except Exception:
#         return "No sales data"


# def parse_price(price: str) -> float:
#     """
#     Convert price string to numeric value.

#     Args:
#         price (str): The price string to convert.

#     Returns:
#         float: The numeric value of the price.
#     """
#     try:
#         price = price.replace('Rs.', '').replace(',', '').strip()
#         return float(price)
#     except ValueError:
#         return 0.0


# @app.get("/api/search")
# async def search_products(
#     query: str = Query(..., description="Search term for Daraz products"),
#     page: int = Query(1, ge=1, description="Page number to fetch")
# ):
#     """API endpoint to search products on Daraz."""
#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")

#     try:
#         products = scrape_daraz(query, page)
#         if not products:
#             return JSONResponse(
#                 status_code=404,
#                 content={"success": False, "message": "No products found."}
#             )
#         return {"success": True, "data": products}
#     except Exception as e:
#         print(f"Error during API request: {e}")
#         raise HTTPException(status_code=500, detail="An error occurred while processing your request.")

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize sentiment analysis pipeline with a BERT model
sentiment_analyzer = pipeline('sentiment-analysis', model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment_of_all_reviews(reviews):
    """
    Analyze the sentiment of all reviews by concatenating them and 
    analyzing the combined text.
    """
    combined_reviews = " ".join(reviews)
    sentiment = sentiment_analyzer(combined_reviews)
    label = sentiment[0]['label']
    # Map labels to scores: '1 star' -> 1, '2 stars' -> 2, ..., '5 stars' -> 5
    sentiment_map = {'1 star': 1, '2 stars': 2, '3 stars': 3, '4 stars': 4, '5 stars': 5}
    return sentiment_map.get(label, 0)  # Default to 0 if not found

def scrape_daraz(query: str, page: int = 1, max_products: int = 40):
    """
    Scrape Daraz Pakistan for products based on the search query.

    Args:
        query (str): Search query for Daraz.
        page (int): The page number to fetch products from.
        max_products (int): Maximum number of products to scrape per page.

    Returns:
        list: A list of dictionaries containing product details and reviews.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}&page={page}"
    driver.get(url)

    products = []

    try:
        wait = WebDriverWait(driver, 30)  # Increased wait time for dynamic content

        # Wait for product elements to load
        product_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Bm3ON')))
        print(f"Number of products found on the page: {len(product_elements)}")

        # Scroll through product elements to ensure lazy-loaded images are fully loaded
        for i in range(len(product_elements)):
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'instant', block: 'center' });", product_elements[i])
            time.sleep(0.3)  # Increased sleep for lazy-loaded content

        # Re-fetch product elements after scrolling to make sure they are not stale
        product_elements = driver.find_elements(By.CLASS_NAME, 'Bm3ON')
        print(f"Refetched number of products: {len(product_elements)}")

        # Fetch product details
        for i in range(len(product_elements)):
            if len(products) >= max_products:
                break
            try:
                # Re-locate product element to avoid stale reference
                product = product_elements[i]

                # Extract product details
                title_element = product.find_element(By.CSS_SELECTOR, '.RfADt a')
                title = title_element.get_attribute("title")
                link = title_element.get_attribute('href')

                price_element = product.find_element(By.CSS_SELECTOR, '.ooOxS')
                price_text = price_element.text.strip()
                price = parse_price(price_text)

                image_element = product.find_element(By.CSS_SELECTOR, '.picture-wrapper img')
                image_url = image_element.get_attribute("src") or image_element.get_attribute("data-src")

                # Extract additional details
                star_count = extract_star_count(product)
                review_count = extract_review_count(product)
                sold_count = extract_sold_count(product)

                # Scrape reviews for the product
                reviews = scrape_product_reviews(driver, link)

                # Analyze sentiment of all reviews combined
                sentiment_score = analyze_sentiment_of_all_reviews(reviews)

                # Append product details
                products.append({
                    "title": title,
                    "link": link,
                    "price": price,
                    "image_url": image_url,
                    "stars": star_count,
                    "reviews": review_count,
                    "sold_count": sold_count,
                    "sentiment_score": sentiment_score,  # Adding the sentiment score to the product data
                    "user_reviews": reviews  # Adding all reviews to the product data
                })
            except Exception as e:
                print(f"Error processing product: {e}")
                continue

    finally:
        driver.quit()

    return products

def scrape_product_reviews(driver, product_url):
    """
    Scrape review text from a product's page.

    Args:
        driver: The Selenium WebDriver instance.
        product_url (str): The URL of the product page.

    Returns:
        list: A list of review texts.
    """
    driver.get(product_url)
    review_texts = []

    try:
        # Wait for reviews section to load
        wait = WebDriverWait(driver, 30)
        review_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.mod-reviews .item')))

        # Add a small sleep after loading reviews to ensure everything has been rendered
        time.sleep(0.5)

        for review in review_elements:
            try:
                # Extract review text content
                review_text_element = review.find_element(By.CSS_SELECTOR, '.item-content .content')
                review_text = review_text_element.text.strip() if review_text_element else "No content"
                
                # Add the review text to the list
                review_texts.append(review_text)
            except Exception as e:
                print(f"Error extracting review text: {e}")
                continue
    except Exception as e:
        print(f"Error loading reviews: {e}")
    
    return review_texts

def extract_review_count(product):
    """
    Extract review count for a product.

    Args:
        product: Web element representing the product.

    Returns:
        str: Review count as a string.
    """
    try:
        review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
        return review_count_element.text.strip().replace("(", "").replace(")", "")
    except Exception:
        return "No reviews"


def extract_sold_count(product):
    """
    Extract sold count for a product.

    Args:
        product: Web element representing the product.

    Returns:
        str: Sold count as a string.
    """
    try:
        sold_count_element = product.find_element(By.CSS_SELECTOR, '._1cEkb span')
        return sold_count_element.text.strip()
    except Exception:
        return "No sales data"


def parse_price(price: str) -> float:
    """
    Convert price string to numeric value.

    Args:
        price (str): The price string to convert.

    Returns:
        float: The numeric value of the price.
    """
    try:
        price = price.replace('Rs.', '').replace(',', '').strip()
        return float(price)
    except ValueError:
        return 0.0

def extract_star_count(product):
    """
    Extract star rating for a product.

    Args:
        product: Web element representing the product.

    Returns:
        int: Star rating count.
    """
    try:
        stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
        return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
    except Exception:
        return 0

# FastAPI endpoint
@app.get("/api/search")
async def search_products(
    query: str = Query(..., description="Search term for Daraz products"),
    page: int = Query(1, ge=1, description="Page number to fetch")
):
    """API endpoint to search products on Daraz."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")

    try:
        products = scrape_daraz(query, page)
        if not products:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "No products found."}
            )
        return {"success": True, "data": products}
    except Exception as e:
        print(f"Error during API request: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
