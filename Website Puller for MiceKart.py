import os
import time
import json
import logging
import queue
import threading
from urllib.parse import urljoin, urlparse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("micekart_content_extractor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    ENTRY_POINT = 'https://micekart.com/eventList'
    OUTPUT_DIR = 'micekart_content'
    MAX_DEPTH = 5
    DELAY = 1.0
    MAX_CONCURRENT = 5
    WAIT_FOR_SELECTOR = '#root'
    WAIT_TIMEOUT = 30
    SCREENSHOT_EACH_PAGE = False
    MAX_RETRIES = 3
    ALLOWED_DOMAINS = ['micekart.com']
    EXTRACT_IMAGES = True  # Whether to extract image URLs and descriptions

class ContentExtractor:
    def __init__(self, config):
        self.config = config
        self.visited = set()
        self.queued = set()
        self.failed_urls = set()
        self.content_map = {}  # URL -> extracted content
        self.page_links = {}   # URL -> list of linked pages
        self.setup_directories()
        self.url_queue = queue.Queue()
        self.semaphore = threading.Semaphore(config.MAX_CONCURRENT)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def setup_directories(self):
        """Create necessary directories for storing the content"""
        dirs = [
            self.config.OUTPUT_DIR,
            os.path.join(self.config.OUTPUT_DIR, 'pages'),
            os.path.join(self.config.OUTPUT_DIR, 'images'),
        ]

        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")

    def sanitize_filename(self, url):
        """Generate a safe filename from a URL"""
        parsed_url = urlparse(url)
        pathname = parsed_url.path.strip('/')
        
        if not pathname:
            pathname = 'index'
        else:
            pathname = pathname.replace('/', '_').replace('.', '_')
            pathname = ''.join(c if c.isalnum() or c == '_' else '_' for c in pathname)
        
        return pathname

    def create_webdriver(self):
        """Create a new Chrome WebDriver instance"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver

    def extract_content(self, url_info):
        """Extract content from a single URL"""
        current_url = url_info['url']
        depth = url_info['depth']
        referrer = url_info.get('referrer')
        retry_count = url_info.get('retry_count', 0)
        
        # Skip if we've gone too deep
        if depth > self.config.MAX_DEPTH:
            logger.info(f"Skipping {current_url} - Max depth reached")
            return
            
        # Skip if we've already visited
        if current_url in self.visited:
            return
            
        # Acquire semaphore (limit concurrent browser instances)
        with self.semaphore:
            logger.info(f"Extracting content from ({depth}): {current_url}")
            
            driver = None
            try:
                # Create a new browser instance
                driver = self.create_webdriver()
                
                # Navigate to the URL with timeout
                driver.get(current_url)
                
                # Wait for main content to load
                try:
                    WebDriverWait(driver, self.config.WAIT_TIMEOUT).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.config.WAIT_FOR_SELECTOR))
                    )
                except TimeoutException:
                    logger.warning(f"Selector {self.config.WAIT_FOR_SELECTOR} not found on {current_url}")
                
                # Get the final URL (after redirects)
                final_url = driver.current_url
                
                # Take a screenshot if enabled
                if self.config.SCREENSHOT_EACH_PAGE:
                    screenshot_path = os.path.join(
                        self.config.OUTPUT_DIR,
                        'screenshots',
                        f"{self.sanitize_filename(final_url)}.png"
                    )
                    driver.save_screenshot(screenshot_path)
                
                # Get page title
                page_title = driver.title
                
                # Get page content using BeautifulSoup for better parsing
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Extract useful content - this may need customization based on the website structure
                extracted_content = {
                    'url': final_url,
                    'title': page_title,
                    'depth': depth,
                    'headings': self.extract_headings(soup),
                    'paragraphs': self.extract_paragraphs(soup),
                    'lists': self.extract_lists(soup),
                    'tables': self.extract_tables(soup),
                    'metadata': self.extract_metadata(soup),
                }
                
                # Extract images if enabled
                if self.config.EXTRACT_IMAGES:
                    extracted_content['images'] = self.extract_images(soup, driver, final_url)
                
                # Save the extracted content as JSON
                filename = self.sanitize_filename(final_url)
                file_path = os.path.join(self.config.OUTPUT_DIR, 'pages', f"{filename}.json")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(extracted_content, f, indent=2, ensure_ascii=False)
                
                # Store in content map
                self.content_map[final_url] = {
                    'title': page_title,
                    'file_path': file_path,
                    'extracted': extracted_content
                }
                
                # Find all links on the page
                links = []
                page_links = []
                
                try:
                    elements = driver.find_elements(By.TAG_NAME, 'a')
                    for element in elements:
                        try:
                            href = element.get_attribute('href')
                            if href:
                                link_text = element.text.strip()
                                links.append({
                                    'href': href,
                                    'text': link_text,
                                    'isNavigation': element.get_attribute('role') == 'button' or
                                                  'nav-link' in element.get_attribute('class') or
                                                  (element.find_elements(By.XPATH, '..') and 
                                                   'navbar-nav' in element.find_element(By.XPATH, '..').get_attribute('class'))
                                })
                        except Exception as e:
                            logger.debug(f"Error getting link attributes: {e}")
                except Exception as e:
                    logger.error(f"Error finding links on {current_url}: {e}")
                
                # Process each link
                for link in links:
                    try:
                        # Skip empty, javascript:, mailto:, tel:, etc.
                        if not link['href'] or \
                           link['href'].startswith('javascript:') or \
                           link['href'].startswith('mailto:') or \
                           link['href'].startswith('tel:') or \
                           link['href'].startswith('#'):
                            continue
                        
                        # Normalize the link
                        full_link = urljoin(final_url, link['href'])
                        
                        # Parse the link
                        parsed_link = urlparse(full_link)
                        
                        # Skip external links
                        if not any(
                            parsed_link.netloc == domain or parsed_link.netloc.endswith(f".{domain}")
                            for domain in self.config.ALLOWED_DOMAINS
                        ):
                            continue
                        
                        # Add to queue if not visited and not already queued
                        if full_link not in self.visited and full_link not in self.queued:
                            self.url_queue.put({
                                'url': full_link,
                                'depth': depth + 1,
                                'referrer': final_url,
                            })
                            self.queued.add(full_link)
                        
                        # Add to page links
                        page_links.append({
                            'url': full_link,
                            'text': link['text'],
                            'isNavigation': link['isNavigation']
                        })
                        
                    except Exception as e:
                        logger.error(f"Error processing link {link.get('href')}: {e}")
                
                # Store page links
                self.page_links[final_url] = page_links
                
                # Mark as visited
                self.visited.add(final_url)
                
                # Save the content map periodically
                self.save_content_map()
                
            except Exception as e:
                logger.error(f"Error extracting content from {current_url}: {e}")
                self.failed_urls.add(current_url)
                
                # Retry logic
                if retry_count < self.config.MAX_RETRIES:
                    logger.info(f"Retrying {current_url} ({retry_count + 1}/{self.config.MAX_RETRIES})")
                    self.url_queue.put({
                        'url': current_url,
                        'depth': depth,
                        'referrer': referrer,
                        'retry_count': retry_count + 1,
                    })
                
            finally:
                # Always close the browser
                if driver:
                    try:
                        driver.quit()
                    except Exception as e:
                        logger.error(f"Error closing browser: {e}")
                
                # Wait before next request
                time.sleep(self.config.DELAY)
    
    def extract_headings(self, soup):
        """Extract headings from the page"""
        headings = []
        for level in range(1, 7):
            for h in soup.find_all(f'h{level}'):
                text = h.get_text(strip=True)
                if text:  # Only add non-empty headings
                    headings.append({
                        'level': level,
                        'text': text
                    })
        return headings
    
    def extract_paragraphs(self, soup):
        """Extract paragraphs from the page"""
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text:  # Only add non-empty paragraphs
                paragraphs.append(text)
        return paragraphs
    
    def extract_lists(self, soup):
        """Extract lists from the page"""
        lists = []
        for list_tag in soup.find_all(['ul', 'ol']):
            list_items = []
            for li in list_tag.find_all('li'):
                text = li.get_text(strip=True)
                if text:  # Only add non-empty list items
                    list_items.append(text)
            
            if list_items:  # Only add non-empty lists
                lists.append({
                    'type': list_tag.name,  # 'ul' or 'ol'
                    'items': list_items
                })
        return lists
    
    def extract_tables(self, soup):
        """Extract tables from the page"""
        tables = []
        for table in soup.find_all('table'):
            rows = []
            # Extract headers
            headers = []
            for th in table.find_all('th'):
                text = th.get_text(strip=True)
                headers.append(text)
            
            # Extract rows
            for tr in table.find_all('tr'):
                row = []
                for td in tr.find_all('td'):
                    text = td.get_text(strip=True)
                    row.append(text)
                if row:  # Only add non-empty rows
                    rows.append(row)
            
            if headers or rows:  # Only add tables with content
                tables.append({
                    'headers': headers,
                    'rows': rows
                })
        return tables
    
    def extract_metadata(self, soup):
        """Extract metadata from the page"""
        metadata = {}
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Extract Open Graph tags
        for meta in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            property_name = meta.get('property')
            content = meta.get('content')
            if property_name and content:
                metadata[property_name] = content
        
        return metadata
    
    def extract_images(self, soup, driver, page_url):
        """Extract images from the page"""
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            alt = img.get('alt', '')
            
            if src:
                # Normalize image URL
                if src.startswith('data:'):
                    # Skip data URLs
                    continue
                
                full_src = urljoin(page_url, src)
                
                # Get image dimensions if possible
                width = img.get('width', '')
                height = img.get('height', '')
                
                images.append({
                    'src': full_src,
                    'alt': alt,
                    'width': width,
                    'height': height
                })
        
        # Additional logic to extract background images
        # This is a bit tricky and might not work for all cases
        try:
            bg_images = []
            elements_with_bg = driver.find_elements(By.CSS_SELECTOR, '*')
            for element in elements_with_bg:
                try:
                    style = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('background-image');", element)
                    if style and style.startswith('url(') and style != 'url("none")':
                        # Extract URL from style
                        url_start = style.find('url(') + 4
                        url_end = style.find(')', url_start)
                        if url_start >= 4 and url_end > url_start:
                            bg_url = style[url_start:url_end].strip('\'"')
                            if bg_url and not bg_url.startswith('data:'):
                                full_bg_url = urljoin(page_url, bg_url)
                                bg_images.append({
                                    'src': full_bg_url,
                                    'alt': 'Background Image',
                                    'is_background': True
                                })
                except:
                    pass
            
            # Add unique background images
            seen_urls = set(img['src'] for img in images)
            for bg in bg_images:
                if bg['src'] not in seen_urls:
                    images.append(bg)
                    seen_urls.add(bg['src'])
        except Exception as e:
            logger.debug(f"Error extracting background images: {e}")
        
        return images
    
    def save_content_map(self):
        """Save the current content map to a file"""
        try:
            # Create a simplified version for JSON serialization
            simplified_map = {}
            for url, data in self.content_map.items():
                simplified_map[url] = {
                    'title': data['title'],
                    'file_path': data['file_path']
                }
            
            content_map_path = os.path.join(self.config.OUTPUT_DIR, 'content_map.json')
            with open(content_map_path, 'w', encoding='utf-8') as f:
                json.dump(simplified_map, f, indent=2, ensure_ascii=False)
            
            # Save page links
            page_links_path = os.path.join(self.config.OUTPUT_DIR, 'page_links.json')
            with open(page_links_path, 'w', encoding='utf-8') as f:
                json.dump(self.page_links, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            logger.error(f"Error saving content map: {e}")
            return False
    
    def save_failed_urls(self):
        """Save the list of failed URLs to a file"""
        if self.failed_urls:
            try:
                failed_urls_path = os.path.join(self.config.OUTPUT_DIR, 'failed_urls.json')
                with open(failed_urls_path, 'w', encoding='utf-8') as f:
                    json.dump(list(self.failed_urls), f, indent=2)
                return True
            except Exception as e:
                logger.error(f"Error saving failed URLs: {e}")
                return False
        return True
    
    def generate_content_summary(self):
        """Generate a summary of all extracted content"""
        try:
            # Count pages by depth
            depth_counts = {}
            for url, data in self.content_map.items():
                depth = data['extracted']['depth']
                depth_counts[depth] = depth_counts.get(depth, 0) + 1
            
            # Count headings, paragraphs, lists, tables
            total_headings = sum(len(data['extracted']['headings']) for data in self.content_map.values())
            total_paragraphs = sum(len(data['extracted']['paragraphs']) for data in self.content_map.values())
            total_lists = sum(len(data['extracted']['lists']) for data in self.content_map.values())
            total_tables = sum(len(data['extracted']['tables']) for data in self.content_map.values())
            
            # Count images if extracted
            total_images = 0
            if self.config.EXTRACT_IMAGES:
                total_images = sum(len(data['extracted'].get('images', [])) for data in self.content_map.values())
            
            # Create summary
            summary = {
                'total_pages': len(self.content_map),
                'total_failed': len(self.failed_urls),
                'pages_by_depth': depth_counts,
                'total_headings': total_headings,
                'total_paragraphs': total_paragraphs,
                'total_lists': total_lists,
                'total_tables': total_tables,
                'total_images': total_images
            }
            
            # Save summary
            summary_path = os.path.join(self.config.OUTPUT_DIR, 'summary.json')
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"Content summary saved to {summary_path}")
            
            # Create README file
            readme_path = os.path.join(self.config.OUTPUT_DIR, 'README.md')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"# MiceKart Content Extraction\n\n")
                f.write(f"Content extracted on {time.strftime('%Y-%m-%d')}.\n\n")
                f.write(f"## Summary\n\n")
                f.write(f"- Total Pages: {summary['total_pages']}\n")
                f.write(f"- Failed Pages: {summary['total_failed']}\n")
                f.write(f"- Total Headings: {summary['total_headings']}\n")
                f.write(f"- Total Paragraphs: {summary['total_paragraphs']}\n")
                f.write(f"- Total Lists: {summary['total_lists']}\n")
                f.write(f"- Total Tables: {summary['total_tables']}\n")
                if self.config.EXTRACT_IMAGES:
                    f.write(f"- Total Images: {summary['total_images']}\n")
                f.write(f"\n## Pages by Depth\n\n")
                for depth, count in sorted(summary['pages_by_depth'].items()):
                    f.write(f"- Depth {depth}: {count} pages\n")
                f.write(f"\n## Files\n\n")
                f.write(f"- `content_map.json`: Maps URLs to extracted content files\n")
                f.write(f"- `page_links.json`: Contains link relationships between pages\n")
                f.write(f"- `failed_urls.json`: Lists URLs that couldn't be processed\n")
                f.write(f"- `summary.json`: This summary in JSON format\n")
                f.write(f"- `pages/`: Directory containing JSON files with extracted content\n")
                if self.config.EXTRACT_IMAGES:
                    f.write(f"- `images/`: Directory containing image information\n")
                
                f.write(f"\n## LLM Usage\n\n")
                f.write(f"The content in the `pages/` directory is structured for easy consumption by an LLM. Each JSON file contains:\n\n")
                f.write(f"- `url`: The original URL\n")
                f.write(f"- `title`: Page title\n")
                f.write(f"- `headings`: All headings with their levels\n")
                f.write(f"- `paragraphs`: All paragraph text\n")
                f.write(f"- `lists`: All lists (both ordered and unordered)\n")
                f.write(f"- `tables`: Table data\n")
                f.write(f"- `metadata`: Meta tags from the page\n")
                if self.config.EXTRACT_IMAGES:
                    f.write(f"- `images`: Information about images on the page\n")
                
                f.write(f"\n## Website Structure\n\n")
                f.write(f"The `page_links.json` file contains information about how pages link to each other,\n")
                f.write(f"which can be used to understand the website's navigation structure.\n")
            
            logger.info(f"README file saved to {readme_path}")
            
            return True
        except Exception as e:
            logger.error(f"Error generating content summary: {e}")
            return False
    
    def start(self):
        """Start the content extraction process"""
        logger.info(f"Starting content extraction from {self.config.ENTRY_POINT}")
        
        # Add entry point to queue
        self.url_queue.put({
            'url': self.config.ENTRY_POINT,
            'depth': 0,
            'referrer': None,
        })
        self.queued.add(self.config.ENTRY_POINT)
        
        # Process the queue with worker threads
        with ThreadPoolExecutor(max_workers=self.config.MAX_CONCURRENT) as executor:
            while not self.url_queue.empty() or len(executor._threads) > 0:
                try:
                    # Get the next URL from the queue (non-blocking)
                    try:
                        url_info = self.url_queue.get(block=False)
                        # Submit the URL for processing
                        executor.submit(self.extract_content, url_info)
                    except queue.Empty:
                        # If queue is empty but threads are still running, wait a bit
                        time.sleep(1)
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
        
        logger.info(f"Content extraction complete. Processed {len(self.visited)} URLs. Failed: {len(self.failed_urls)}")
        
        # Save final content map and failed URLs
        self.save_content_map()
        self.save_failed_urls()
        
        # Generate content summary
        self.generate_content_summary()
        
        logger.info(f"Content extraction complete. Output directory: {self.config.OUTPUT_DIR}")


def main():
    """Main entry point"""
    logger.info("Starting MiceKart content extractor")
    
    # Create and configure the extractor
    extractor = ContentExtractor(Config)
    
    # Start the extraction process
    extractor.start()


if __name__ == "__main__":
    main()
