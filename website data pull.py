from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def scrape_micekart_page():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to the page
        url = "https://micekart.com/mice-event/corporate-event-basic-conference-setup/Mzg="
        driver.get(url)
        
        # Wait for JavaScript to load the content
        time.sleep(5)
        
        # Get the page source after JavaScript execution
        page_content = driver.page_source
        
        # You can also capture specific elements
        # For example, getting the main content section:
        try:
            main_content = driver.find_element("id", "main-content").get_attribute('innerHTML')
        except:
            main_content = "Main content element not found"
        
        # Get page title
        page_title = driver.title
        
        # Capture all images
        images = []
        img_elements = driver.find_elements("tag name", "img")
        for img in img_elements:
            images.append({
                "src": img.get_attribute("src"),
                "alt": img.get_attribute("alt")
            })
        
        # Save the results to a file
        result = {
            "title": page_title,
            "full_html": page_content,
            "main_content": main_content,
            "images": images
        }
        
        with open("micekart_page_content.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print("Scraping completed. Content saved to 'micekart_page_content.json'")
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    scrape_micekart_page()
