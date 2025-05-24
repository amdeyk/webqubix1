import os
import time
import json
import hashlib
import urllib.parse
import logging
import threading
import queue
from urllib.parse import urljoin, urlparse
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import shutil
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("micekart_crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    ENTRY_POINT = 'https://micekart.com/eventList'
    OUTPUT_DIR = 'micekart_website_backup'
    LINK_MAP_FILE = 'link_map.json'
    MAX_DEPTH = 5  # Maximum crawl depth
    DELAY = 1.0  # Delay between requests in seconds
    MAX_CONCURRENT = 5  # Maximum concurrent browser instances
    INCLUDE_STATIC_ASSETS = True  # Whether to download CSS, JS, images, etc.
    INCLUDE_EXTERNAL_LINKS = False  # Whether to follow links to other domains
    CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080
    WAIT_FOR_SELECTOR = '#root'  # Wait for this selector to be available on the page
    WAIT_TIMEOUT = 30  # 30 seconds timeout for page load
    SCREENSHOT_EACH_PAGE = True  # Take screenshots of each page
    MAX_RETRIES = 3  # Maximum number of retries for failed requests
    ALLOWED_DOMAINS = ['micekart.com']  # Domains to crawl (including subdomains)
    ASSET_EXTENSIONS = {
        'css': ['.css', '.scss', '.less'],
        'js': ['.js', '.jsx', '.ts', '.tsx'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico', '.bmp'],
        'fonts': ['.woff', '.woff2', '.ttf', '.eot', '.otf']
    }


class WebsiteCrawler:
    def __init__(self, config):
        self.config = config
        self.visited = set()  # URLs we've already processed
        self.queued = set()   # URLs we've already added to the queue
        self.failed_urls = set()  # URLs that failed to load
        self.link_map = {
            "nodes": {},  # URLs as keys, metadata as values
            "edges": [],  # Connections between pages
        }
        self.setup_directories()
        self.url_queue = queue.Queue()
        self.semaphore = threading.Semaphore(config.MAX_CONCURRENT)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.CHROME_USER_AGENT
        })

    def setup_directories(self):
        """Create necessary directories for storing the website backup"""
        dirs = [
            self.config.OUTPUT_DIR,
            os.path.join(self.config.OUTPUT_DIR, 'html'),
            os.path.join(self.config.OUTPUT_DIR, 'assets'),
            os.path.join(self.config.OUTPUT_DIR, 'assets', 'css'),
            os.path.join(self.config.OUTPUT_DIR, 'assets', 'js'),
            os.path.join(self.config.OUTPUT_DIR, 'assets', 'images'),
            os.path.join(self.config.OUTPUT_DIR, 'assets', 'fonts'),
            os.path.join(self.config.OUTPUT_DIR, 'screenshots'),
        ]

        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"Created directory: {dir_path}")

    def sanitize_filename(self, url):
        """Generate a safe filename from a URL"""
        # Generate a hash of the URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # Extract the pathname and remove leading/trailing slashes
        parsed_url = urlparse(url)
        pathname = parsed_url.path.strip('/')
        
        # Replace special characters and empty path
        if not pathname:
            pathname = 'index'
        else:
            pathname = pathname.replace('/', '_').replace('.', '_')
            pathname = ''.join(c if c.isalnum() or c == '_' else '_' for c in pathname)
        
        return f"{pathname}_{url_hash}"

    def get_asset_type(self, asset_url):
        """Determine the asset type from the URL"""
        parsed_url = urlparse(asset_url)
        extension = os.path.splitext(parsed_url.path)[1].lower()
        
        for asset_type, extensions in self.config.ASSET_EXTENSIONS.items():
            if extension in extensions:
                return asset_type
        
        return None

    def save_file(self, file_path, content, is_binary=False):
        """Save content to a file"""
        try:
            if is_binary:
                with open(file_path, 'wb') as f:
                    f.write(content)
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            logger.info(f"Saved: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {e}")
            return False

    def download_asset(self, asset_url, referrer_url=None):
        """Download a static asset (CSS, JS, image, etc.)"""
        if not self.config.INCLUDE_STATIC_ASSETS:
            return None
            
        try:
            # Skip if not in allowed domains
            asset_domain = urlparse(asset_url).netloc
            if not self.config.INCLUDE_EXTERNAL_LINKS and not any(
                asset_domain == domain or asset_domain.endswith(f".{domain}")
                for domain in self.config.ALLOWED_DOMAINS
            ):
                return None
                
            asset_type = self.get_asset_type(asset_url)
            if not asset_type:
                return None
                
            # Make the request with proper headers
            headers = {'Referer': referrer_url} if referrer_url else {}
            response = self.session.get(asset_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Create a safe filename
                asset_filename = self.sanitize_filename(asset_url)
                asset_dir = os.path.join(self.config.OUTPUT_DIR, 'assets', asset_type)
                asset_path = os.path.join(asset_dir, asset_filename)
                
                # Save the asset
                self.save_file(asset_path, response.content, is_binary=True)
                
                # Add to link map
                self.link_map["nodes"][asset_url] = {
                    "type": "asset",
                    "assetType": asset_type,
                    "localPath": asset_path,
                    "status": response.status_code,
                    "contentLength": len(response.content),
                }
                
                # Add the edge if there's a referrer
                if referrer_url:
                    self.link_map["edges"].append({
                        "source": referrer_url,
                        "target": asset_url,
                        "type": "asset_reference"
                    })
                    
                return asset_path
            else:
                logger.warning(f"Failed to download asset {asset_url}: Status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error downloading asset {asset_url}: {e}")
            return None

    def create_webdriver(self):
        """Create a new Chrome WebDriver instance"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--window-size={self.config.VIEWPORT_WIDTH},{self.config.VIEWPORT_HEIGHT}')
        chrome_options.add_argument(f'--user-agent={self.config.CHROME_USER_AGENT}')
        
        # Initialize the WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set window size
        driver.set_window_size(self.config.VIEWPORT_WIDTH, self.config.VIEWPORT_HEIGHT)
        
        return driver

    def process_url(self, url_info):
        """Process a single URL, downloading content and finding new links"""
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
            # Just add the edge if this is a new referrer
            if referrer and not any(e['source'] == referrer and e['target'] == current_url for e in self.link_map['edges']):
                self.link_map['edges'].append({
                    'source': referrer,
                    'target': current_url
                })
            return
            
        # Acquire semaphore (limit concurrent browser instances)
        with self.semaphore:
            logger.info(f"Crawling ({depth}): {current_url}")
            
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
                
                # Get page content
                content = driver.page_source
                
                # Save the HTML
                filename = self.sanitize_filename(final_url)
                file_path = os.path.join(self.config.OUTPUT_DIR, 'html', f"{filename}.html")
                self.save_file(file_path, content)
                
                # Add to link map
                self.link_map["nodes"][final_url] = {
                    "type": "page",
                    "depth": depth,
                    "title": driver.title,
                    "status": 200,  # Assuming success
                    "contentLength": len(content),
                    "localPath": file_path,
                }
                
                # Add the edge if there's a referrer
                if referrer:
                    self.link_map["edges"].append({
                        "source": referrer,
                        "target": final_url
                    })
                
                # Find all links on the page
                links = []
                try:
                    elements = driver.find_elements(By.TAG_NAME, 'a')
                    for element in elements:
                        try:
                            href = element.get_attribute('href')
                            if href:
                                links.append({
                                    'href': href,
                                    'text': element.text.strip(),
                                    'isNavigation': element.get_attribute('role') == 'button' or
                                                  'nav-link' in element.get_attribute('class') or
                                                  'navbar-nav' in element.find_element(By.XPATH, '..').get_attribute('class')
                                })
                        except Exception as e:
                            logger.debug(f"Error getting link attributes: {e}")
                except Exception as e:
                    logger.error(f"Error finding links on {current_url}: {e}")
                
                # Process assets if enabled
                if self.config.INCLUDE_STATIC_ASSETS:
                    self.process_page_assets(driver, final_url)
                
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
                        
                        # Skip external links if configured
                        if not self.config.INCLUDE_EXTERNAL_LINKS and not any(
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
                            
                            # Add link info to map
                            self.link_map["nodes"][full_link] = {
                                "type": "link",
                                "text": link['text'],
                                "isNavigation": link['isNavigation'],
                            }
                        
                        # Always add the edge even if already visited
                        if not any(e['source'] == final_url and e['target'] == full_link for e in self.link_map['edges']):
                            self.link_map["edges"].append({
                                "source": final_url,
                                "target": full_link,
                                "text": link['text'],
                                "isNavigation": link['isNavigation'],
                            })
                    except Exception as e:
                        logger.error(f"Error processing link {link.get('href')}: {e}")
                
                # Mark as visited
                self.visited.add(final_url)
                
                # Save the link map periodically
                self.save_link_map()
                
            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")
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
                else:
                    # Add to link map as error
                    self.link_map["nodes"][current_url] = {
                        "type": "error",
                        "depth": depth,
                        "error": str(e),
                    }
                    
                    # Add the edge if there's a referrer
                    if referrer:
                        self.link_map["edges"].append({
                            "source": referrer,
                            "target": current_url,
                            "status": "error"
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

    def process_page_assets(self, driver, page_url):
        """Find and download all static assets on a page"""
        try:
            # Get all CSS stylesheets
            for link in driver.find_elements(By.TAG_NAME, 'link'):
                try:
                    rel = link.get_attribute('rel')
                    href = link.get_attribute('href')
                    if rel and rel.lower() == 'stylesheet' and href:
                        self.download_asset(href, page_url)
                except Exception as e:
                    logger.debug(f"Error processing stylesheet: {e}")
            
            # Get all scripts
            for script in driver.find_elements(By.TAG_NAME, 'script'):
                try:
                    src = script.get_attribute('src')
                    if src:
                        self.download_asset(src, page_url)
                except Exception as e:
                    logger.debug(f"Error processing script: {e}")
            
            # Get all images
            for img in driver.find_elements(By.TAG_NAME, 'img'):
                try:
                    src = img.get_attribute('src')
                    if src and not src.startswith('data:'):
                        self.download_asset(src, page_url)
                except Exception as e:
                    logger.debug(f"Error processing image: {e}")
            
            # Get all fonts
            for font_element in driver.find_elements(By.CSS_SELECTOR, '@font-face'):
                try:
                    style = font_element.get_attribute('style')
                    if style and 'url(' in style:
                        # Extract URL from style
                        url_start = style.find('url(') + 4
                        url_end = style.find(')', url_start)
                        if url_start >= 4 and url_end > url_start:
                            font_url = style[url_start:url_end].strip('\'"')
                            self.download_asset(urljoin(page_url, font_url), page_url)
                except Exception as e:
                    logger.debug(f"Error processing font: {e}")
            
        except Exception as e:
            logger.error(f"Error processing assets for {page_url}: {e}")

    def save_link_map(self):
        """Save the current link map to a file"""
        try:
            link_map_path = os.path.join(self.config.OUTPUT_DIR, self.config.LINK_MAP_FILE)
            with open(link_map_path, 'w', encoding='utf-8') as f:
                json.dump(self.link_map, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving link map: {e}")
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

    def generate_site_map_visualization(self):
        """Create an HTML visualization of the site structure using D3.js"""
        logger.info("Generating site map visualization...")
        try:
            # Create the visualization HTML (D3.js)
            visualization_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MiceKart Website Structure</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: #f9f9f9;
    }
    #container {
      width: 100%%;
      height: 100vh;
      overflow: hidden;
    }
    .node {
      stroke: #fff;
      stroke-width: 1.5px;
    }
    .link {
      stroke: #999;
      stroke-opacity: 0.6;
    }
    .node text {
      font-size: 10px;
      fill: #333;
    }
    .controls {
      position: absolute;
      top: 10px;
      left: 10px;
      background: white;
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
      z-index: 1000;
    }
    .tooltip {
      position: absolute;
      background: white;
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
      opacity: 0;
      pointer-events: none;
      z-index: 1000;
      max-width: 300px;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <div class="controls">
    <h2>MiceKart Website Structure</h2>
    <p>Total pages: <span id="page-count">0</span></p>
    <p>Total links: <span id="link-count">0</span></p>
    <button id="zoom-in">Zoom In</button>
    <button id="zoom-out">Zoom Out</button>
    <button id="reset">Reset View</button>
    <div>
      <label for="node-size">Node Size:</label>
      <select id="node-size">
        <option value="fixed">Fixed</option>
        <option value="depth">By Depth</option>
        <option value="links">By # of Links</option>
      </select>
    </div>
    <div>
      <label for="color-scheme">Color Scheme:</label>
      <select id="color-scheme">
        <option value="type">By Type</option>
        <option value="depth">By Depth</option>
        <option value="status">By Status</option>
      </select>
    </div>
    <div>
      <label for="filter-type">Filter Type:</label>
      <select id="filter-type">
        <option value="all">All</option>
        <option value="page">Pages</option>
        <option value="link">Links</option>
        <option value="asset">Assets</option>
        <option value="failed">Failed</option>
        <option value="error">Errors</option>
      </select>
    </div>
  </div>
  
  <div id="container"></div>
  <div class="tooltip" id="tooltip"></div>
  
  <script>
    // Load the data
    const linkMapData = %s;
    
    // Format the data for D3
    const nodes = Object.entries(linkMapData.nodes).map(([url, data]) => {
      return {
        id: url,
        url: url,
        ...data
      };
    });
    
    const links = linkMapData.edges.map(edge => {
      return {
        source: edge.source,
        target: edge.target,
        text: edge.text || '',
        isNavigation: edge.isNavigation || false
      };
    });
    
    // Update counts
    document.getElementById('page-count').textContent = nodes.filter(n => n.type === 'page').length;
    document.getElementById('link-count').textContent = links.length;
    
    // Set up the D3 visualization
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    // Create a force simulation
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(width / 2).strength(0.1))
      .force("y", d3.forceY(height / 2).strength(0.1));
    
    // Create the SVG container
    const svg = d3.select("#container")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%%; height: auto;");
    
    // Add zoom behavior
    const g = svg.append("g");
    
    const zoom = d3.zoom()
      .scaleExtent([0.1, 10])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    
    svg.call(zoom);
    
    // Create the tooltip
    const tooltip = d3.select("#tooltip");
    
    // Color scale for types
    const typeColor = d3.scaleOrdinal()
      .domain(['page', 'link', 'asset', 'failed', 'error'])
      .range(['#4285F4', '#34A853', '#FBBC05', '#EA4335', '#9C27B0']);
    
    // Color scale for depth
    const depthColor = d3.scaleSequential()
      .domain([0, d3.max(nodes, d => d.depth || 0)])
      .interpolator(d3.interpolateViridis);
    
    // Color scale for status
    const statusColor = d3.scaleOrdinal()
      .domain(['200', '404', '500', 'No response', 'error'])
      .range(['#4CAF50', '#FF9800', '#F44336', '#9E9E9E', '#9C27B0']);
    
    // Function to update the node colors
    function updateNodeColors() {
      const colorScheme = document.getElementById("color-scheme").value;
      
      return d => {
        if (colorScheme === 'type') {
          return typeColor(d.type);
        } else if (colorScheme === 'depth') {
          return depthColor(d.depth || 0);
        } else if (colorScheme === 'status') {
          if (d.type === 'page') {
            return statusColor(d.status?.toString() || '200');
          } else if (d.type === 'error' || d.type === 'failed') {
            return statusColor('error');
          } else {
            return '#BBBBBB';
          }
        }
      };
    }
    
    // Function to update the node sizes
    function updateNodeSizes() {
      const sizeScheme = document.getElementById("node-size").value;
      
      return d => {
        if (sizeScheme === 'fixed') {
          return d.type === 'page' ? 8 : 5;
        } else if (sizeScheme === 'depth') {
          return Math.max(3, 10 - (d.depth || 0));
        } else if (sizeScheme === 'links') {
          // Count links connected to this node
          const count = links.filter(l => l.source.id === d.id || l.target.id === d.id).length;
          return Math.max(3, Math.min(15, 3 + count / 5));
        }
      };
    }
    
    // Function to filter nodes
    function filterNodes() {
      const filterType = document.getElementById("filter-type").value;
      
      if (filterType === 'all') {
        return nodes;
      } else {
        return nodes.filter(n => n.type === filterType);
      }
    }
    
    // Function to filter links
    function filterLinks(filteredNodes) {
      const nodeIds = new Set(filteredNodes.map(n => n.id));
      return links.filter(l => 
        nodeIds.has(typeof l.source === 'object' ? l.source.id : l.source) && 
        nodeIds.has(typeof l.target === 'object' ? l.target.id : l.target)
      );
    }
    
    // Function to update the visualization
    function updateVisualization() {
      // Get filtered nodes and links
      const filteredNodes = filterNodes();
      const filteredLinks = filterLinks(filteredNodes);
      
      // Update the simulation
      simulation.nodes(filteredNodes);
      simulation.force("link").links(filteredLinks);
      simulation.alpha(1).restart();
      
      // Update the links
      const link = g.selectAll(".link")
        .data(filteredLinks, d => `${d.source.id || d.source}-${d.target.id || d.target}`);
      
      link.exit().remove();
      
      const linkEnter = link.enter().append("line")
        .attr("class", "link")
        .style("stroke-width", d => d.isNavigation ? 2 : 1);
      
      // Update the nodes
      const node = g.selectAll(".node")
        .data(filteredNodes, d => d.id);
      
      node.exit().remove();
      
      const nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));
      
      nodeEnter.append("circle")
        .attr("r", updateNodeSizes())
        .style("fill", updateNodeColors())
        .on("mouseover", (event, d) => {
          tooltip.style("opacity", 1)
            .html(`
              <div>
                <strong>URL:</strong> ${d.url}<br>
                <strong>Type:</strong> ${d.type}<br>
                ${d.title ? `<strong>Title:</strong> ${d.title}<br>` : ''}
                ${d.depth !== undefined ? `<strong>Depth:</strong> ${d.depth}<br>` : ''}
                ${d.status ? `<strong>Status:</strong> ${d.status}<br>` : ''}
                ${d.localPath ? `<strong>Local:</strong> ${d.localPath.split('/').pop()}<br>` : ''}
              </div>
            `)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY + 10) + "px");
        })
        .on("mouseout", () => {
          tooltip.style("opacity", 0);
        })
        .on("click", (event, d) => {
          // Center and zoom on the clicked node
          const transform = d3.zoomIdentity
            .translate(width / 2, height / 2)
            .scale(1.2)
            .translate(-d.x, -d.y);
          
          svg.transition().duration(750).call(zoom.transform, transform);
          
          // Open the URL in a new tab if it's a page
          if (d.type === 'page' && d.localPath) {
            window.open(d.localPath.replace(/\\\\/g, '/'), '_blank');
          }
        });
    
      // Update simulation on tick
      simulation.on("tick", () => {
        link.merge(linkEnter)
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
        
        nodeEnter.merge(node)
          .attr("transform", d => `translate(${d.x},${d.y})`);
      });
      
      // Update node appearance
      g.selectAll(".node circle")
        .style("fill", updateNodeColors())
        .attr("r", updateNodeSizes());
    }
    
    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    
    // Add event listeners for controls
    document.getElementById("zoom-in").addEventListener("click", () => {
      svg.transition().duration(500).call(zoom.scaleBy, 1.5);
    });
    
    document.getElementById("zoom-out").addEventListener("click", () => {
      svg.transition().duration(500).call(zoom.scaleBy, 0.75);
    });
    
    document.getElementById("reset").addEventListener("click", () => {
      svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
    });
    
    document.getElementById("node-size").addEventListener("change", updateVisualization);
    document.getElementById("color-scheme").addEventListener("change", updateVisualization);
    document.getElementById("filter-type").addEventListener("change", updateVisualization);
    
    // Initial render
    updateVisualization();
  </script>
</body>
</html>
""" % json.dumps(self.link_map)
            
            # Save the visualization HTML
            visualization_path = os.path.join(self.config.OUTPUT_DIR, 'site_map.html')
            self.save_file(visualization_path, visualization_html)
            logger.info(f"Site map visualization saved to {visualization_path}")
            return True
        except Exception as e:
            logger.error(f"Error generating site map visualization: {e}")
            return False

    def generate_index_page(self):
        """Create an index.html page for browsing the backup"""
        logger.info("Generating index page...")
        try:
            # Count pages by type
            page_count = sum(1 for node in self.link_map["nodes"].values() if node.get("type") == "page")
            asset_count = sum(1 for node in self.link_map["nodes"].values() if node.get("type") == "asset")
            error_count = sum(1 for node in self.link_map["nodes"].values() if node.get("type") in ["error", "failed"])
            
            # Find the most important pages
            pages = [(url, data) for url, data in self.link_map["nodes"].items() if data.get("type") == "page"]
            pages.sort(key=lambda x: x[1].get("depth", 999))  # Sort by depth - lower depth is more important
            
            # Create the index HTML
            index_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MiceKart Website Backup</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background: #f9f9f9;
      color: #333;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    h1, h2, h3 {{
      color: #f2673c;
    }}
    .card {{
      background: white;
      border-radius: 5px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }}
    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin-bottom: 20px;
    }}
    .stat-card {{
      flex: 1;
      min-width: 200px;
      background: #fff;
      border-radius: 5px;
      padding: 15px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
      text-align: center;
    }}
    .stat-card h3 {{
      margin-top: 0;
    }}
    .stat-card .value {{
      font-size: 36px;
      font-weight: 700;
      color: #f2673c;
    }}
    .button {{
      display: inline-block;
      background: #f2673c;
      color: white;
      padding: 10px 15px;
      text-decoration: none;
      border-radius: 4px;
      margin-right: 10px;
      margin-bottom: 10px;
    }}
    .button:hover {{
      background: #e05a30;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }}
    th {{
      background-color: #f2f2f2;
    }}
    tr:hover {{
      background-color: #f5f5f5;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>MiceKart Website Backup</h1>
    <p>This is a complete backup of the MiceKart website, created on {time.strftime("%Y-%m-%d")}.</p>
    
    <div class="stats">
      <div class="stat-card">
        <h3>Pages</h3>
        <div class="value">{page_count}</div>
      </div>
      <div class="stat-card">
        <h3>Assets</h3>
        <div class="value">{asset_count}</div>
      </div>
      <div class="stat-card">
        <h3>Errors</h3>
        <div class="value">{error_count}</div>
      </div>
    </div>
    
    <div class="card">
      <h2>Tools</h2>
      <a href="site_map.html" class="button">View Site Map</a>
      <a href="link_map.json" class="button">Download Link Map</a>
      <a href="failed_urls.json" class="button">View Failed URLs</a>
    </div>
    
    <div class="card">
      <h2>Main Pages</h2>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>URL</th>
            <th>Depth</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
    """
            
            # Add rows for the first 20 most important pages
            for url, data in pages[:20]:
                title = data.get("title", "Untitled")
                depth = data.get("depth", "N/A")
                local_path = data.get("localPath", "").replace(self.config.OUTPUT_DIR + os.path.sep, "")
                
                index_html += f"""
          <tr>
            <td>{title}</td>
            <td>{url}</td>
            <td>{depth}</td>
            <td><a href="{local_path}" class="button">View</a></td>
          </tr>
        """
            
            index_html += """
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>
            """
            
            # Save the index HTML
            index_path = os.path.join(self.config.OUTPUT_DIR, 'index.html')
            self.save_file(index_path, index_html)
            logger.info(f"Index page saved to {index_path}")
            return True
        except Exception as e:
            logger.error(f"Error generating index page: {e}")
            return False

    def start(self):
        """Start the crawling process"""
        logger.info(f"Starting crawl from {self.config.ENTRY_POINT}")
        
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
                        executor.submit(self.process_url, url_info)
                    except queue.Empty:
                        # If queue is empty but threads are still running, wait a bit
                        time.sleep(1)
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
        
        logger.info(f"Crawl complete. Visited {len(self.visited)} URLs. Failed: {len(self.failed_urls)}")
        
        # Save final link map and failed URLs
        self.save_link_map()
        self.save_failed_urls()
        
        # Generate site map visualization and index page
        self.generate_site_map_visualization()
        self.generate_index_page()
        
        logger.info(f"Website backup complete. Output directory: {self.config.OUTPUT_DIR}")


def main():
    """Main entry point"""
    logger.info("Starting MiceKart website crawler")
    
    # Create and configure the crawler
    crawler = WebsiteCrawler(Config)
    
    # Start the crawling process
    crawler.start()


if __name__ == "__main__":
    main()
