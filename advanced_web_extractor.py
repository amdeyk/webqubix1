# Save this as fixed_advanced_web_extractor.py
import asyncio
import sys
import re
import os
from urllib.parse import urlparse
from datetime import datetime
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

class AdvancedWebExtractor:
    def __init__(self):
        self.output_dir = "extracted_websites"
        self.ensure_output_directory()
        self.interaction_strategies = self.get_interaction_strategies()
    
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def get_interaction_strategies(self):
        """Define various interaction strategies for different types of clickable elements"""
        return {
            "tabs": {
                "selectors": [
                    ".tab", ".tab-button", ".tab-link", ".tab-item",
                    "[role='tab']", ".nav-tab", ".ui-tab", ".tabs-nav a",
                    ".tab-pane", ".tabbed-content", ".tab-header"
                ],
                "script": """
                // Click all tab elements
                const tabSelectors = ['.tab', '.tab-button', '.tab-link', '.tab-item', '[role="tab"]', '.nav-tab', '.ui-tab', '.tabs-nav a'];
                for (const selector of tabSelectors) {
                    const tabs = document.querySelectorAll(selector);
                    for (let i = 0; i < tabs.length; i++) {
                        const tab = tabs[i];
                        if (tab.offsetParent !== null) { // Check if visible
                            tab.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            await new Promise(r => setTimeout(r, 500));
                            tab.click();
                            await new Promise(r => setTimeout(r, 1000));
                        }
                    }
                }
                """
            },
            "accordions": {
                "selectors": [
                    ".accordion", ".accordion-item", ".accordion-header", ".accordion-toggle",
                    ".collapsible", ".expandable", ".faq-item", ".dropdown-toggle",
                    "[data-toggle='collapse']", ".expand", ".show-more"
                ],
                "script": """
                // Click accordion/collapsible elements
                const accordionSelectors = ['.accordion-header', '.accordion-toggle', '.collapsible', '.expandable', '.faq-item', '[data-toggle="collapse"]', '.expand', '.show-more'];
                for (const selector of accordionSelectors) {
                    const items = document.querySelectorAll(selector);
                    for (let i = 0; i < items.length; i++) {
                        const item = items[i];
                        if (item.offsetParent !== null && !item.classList.contains('active')) {
                            item.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            await new Promise(r => setTimeout(r, 500));
                            item.click();
                            await new Promise(r => setTimeout(r, 1000));
                        }
                    }
                }
                """
            },
            "load_more": {
                "selectors": [
                    ".load-more", ".show-more", ".view-more", ".see-more", 
                    ".read-more", ".expand-more", "[data-load-more]",
                    ".pagination .next", ".load-next", ".infinite-scroll"
                ],
                "script": """
                // Click "Load More" type buttons
                const loadMoreSelectors = ['.load-more', '.show-more', '.view-more', '.see-more', '.read-more', '.expand-more', '[data-load-more]'];
                for (const selector of loadMoreSelectors) {
                    const buttons = document.querySelectorAll(selector);
                    for (let i = 0; i < buttons.length; i++) {
                        const button = buttons[i];
                        let clickCount = 0;
                        while (button.offsetParent !== null && clickCount < 5) { // Limit to 5 clicks
                            button.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            await new Promise(r => setTimeout(r, 500));
                            button.click();
                            await new Promise(r => setTimeout(r, 2000));
                            clickCount++;
                            if (button.disabled || button.style.display === 'none') break;
                        }
                    }
                }
                """
            },
            "menus": {
                "selectors": [
                    ".menu-item", ".nav-item", ".dropdown-item", ".submenu",
                    ".menu-toggle", ".hamburger", ".mobile-menu", ".nav-trigger"
                ],
                "script": """
                // Interact with menu items
                const menuSelectors = ['.menu-toggle', '.hamburger', '.mobile-menu', '.nav-trigger'];
                for (const selector of menuSelectors) {
                    const toggles = document.querySelectorAll(selector);
                    for (const toggle of toggles) {
                        if (toggle.offsetParent !== null) {
                            toggle.click();
                            await new Promise(r => setTimeout(r, 1000));
                        }
                    }
                }
                
                // Hover over dropdown menus
                const dropdowns = document.querySelectorAll('.dropdown, .menu-item');
                for (const dropdown of dropdowns) {
                    if (dropdown.offsetParent !== null) {
                        dropdown.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
                        await new Promise(r => setTimeout(r, 500));
                    }
                }
                """
            },
            "infinite_scroll": {
                "selectors": ["body"],
                "script": """
                // Handle infinite scroll
                let scrollCount = 0;
                const maxScrolls = 10;
                let lastHeight = document.body.scrollHeight;
                
                while (scrollCount < maxScrolls) {
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(r => setTimeout(r, 2000));
                    
                    const newHeight = document.body.scrollHeight;
                    if (newHeight === lastHeight) {
                        break; // No more content loaded
                    }
                    lastHeight = newHeight;
                    scrollCount++;
                }
                
                // Scroll back to top
                window.scrollTo(0, 0);
                """
            }
        }
    
    def detect_interactive_elements(self, html_content):
        """Detect what types of interactive elements are present on the page"""
        detected_elements = []
        
        for element_type, config in self.interaction_strategies.items():
            for selector in config["selectors"]:
                # Convert CSS selector to a simple regex pattern for detection
                pattern = selector.replace(".", r"\.").replace("[", r"\[").replace("]", r"\]")
                if re.search(pattern, html_content, re.IGNORECASE):
                    detected_elements.append(element_type)
                    break
        
        return detected_elements
    
    def create_comprehensive_interaction_script(self, detected_elements=None):
        """Create a comprehensive JavaScript script based on detected elements"""
        if detected_elements is None:
            detected_elements = list(self.interaction_strategies.keys())
        
        script_parts = [
            "console.log('Starting comprehensive interaction script...');",
            "const originalTimeout = 1000;",
            "let interactionCount = 0;",
        ]
        
        for element_type in detected_elements:
            if element_type in self.interaction_strategies:
                script_parts.append(f"// {element_type.upper()} INTERACTION")
                script_parts.append("try {")
                script_parts.append(self.interaction_strategies[element_type]["script"])
                script_parts.append("interactionCount++;")
                script_parts.append("} catch(e) { console.log('Error in " + element_type + ":', e); }")
                script_parts.append("")
        
        script_parts.extend([
            "// Final content loading",
            "for(let i = 0; i < 3; i++) {",
            "    window.scrollTo(0, document.body.scrollHeight);",
            "    await new Promise(r => setTimeout(r, 1000));",
            "    window.scrollTo(0, 0);",
            "    await new Promise(r => setTimeout(r, 500));",
            "}",
            "console.log('Interaction script completed. Interactions performed:', interactionCount);"
        ])
        
        return "\n".join(script_parts)
    
    async def extract_with_interactions(self, url, interaction_mode="auto"):
        """Extract content with intelligent interaction handling"""
        print(f"🌐 Starting interactive extraction from: {url}")
        
        # Fixed BrowserConfig - removed invalid parameters
        browser_config = BrowserConfig(
            headless=True,
            verbose=True
        )
        
        extraction_strategies = []
        
        if interaction_mode in ["auto", "basic"]:
            extraction_strategies.append({
                "name": "Basic Extraction",
                "config": CrawlerRunConfig(
                    wait_until="networkidle",
                    page_timeout=30000,
                )
            })
        
        if interaction_mode in ["auto", "interactive", "full"]:
            extraction_strategies.append({
                "name": "Light Interactions",
                "config": CrawlerRunConfig(
                    wait_until="networkidle",
                    page_timeout=45000,
                    js_code=[
                        "window.scrollTo(0, document.body.scrollHeight);",
                        "await new Promise(r => setTimeout(r, 2000));",
                        """
                        const showMoreBtns = document.querySelectorAll('.show-more, .load-more, .read-more, .see-more');
                        for (const btn of showMoreBtns) {
                            if (btn.offsetParent !== null) {
                                btn.click();
                                await new Promise(r => setTimeout(r, 1000));
                            }
                        }
                        """,
                        "window.scrollTo(0, 0);"
                    ]
                )
            })
            
            extraction_strategies.append({
                "name": "Comprehensive Interactions",
                "config": CrawlerRunConfig(
                    wait_until="networkidle",
                    page_timeout=90000,
                    js_code=[self.create_comprehensive_interaction_script()]
                )
            })
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            best_result = None
            best_content_length = 0
            
            for strategy in extraction_strategies:
                try:
                    print(f"📡 Trying: {strategy['name']}...")
                    
                    result = await crawler.arun(
                        url=url,
                        config=strategy['config'],
                        magic=True
                    )
                    
                    if result.success:
                        content = self.extract_content_from_result(result)
                        content_length = len(content) if content else 0
                        
                        print(f"✅ {strategy['name']} successful! Content length: {content_length}")
                        
                        if content_length > best_content_length:
                            best_result = result
                            best_content_length = content_length
                            
                            if content_length > 10000:
                                break
                    else:
                        print(f"⚠️ {strategy['name']} failed")
                        
                except Exception as e:
                    print(f"❌ {strategy['name']} error: {str(e)}")
                    continue
            
            if best_result:
                return self.process_extraction_result(best_result, url)
            else:
                print("🔄 All interactive strategies failed, trying simple fallback...")
                return await self.fallback_extraction(url)
    
    def extract_content_from_result(self, result):
        """Extract the best available content from result"""
        if result.markdown and result.markdown.fit_markdown:
            return result.markdown.fit_markdown
        elif result.markdown and result.markdown.raw_markdown:
            return result.markdown.raw_markdown
        elif result.cleaned_html:
            return result.cleaned_html
        elif result.html:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(result.html, 'html.parser')
                for element in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
                    element.decompose()
                return soup.get_text(separator='\n', strip=True)
            except:
                return result.html
        return ""
    
    def process_extraction_result(self, result, url):
        """Process successful extraction result with enhanced metadata"""
        content = self.extract_content_from_result(result)
        
        detected_elements = self.detect_interactive_elements(result.html) if result.html else []
        
        metadata = {
            'url': url,
            'status_code': result.status_code,
            'title': result.metadata.get('title', '') if result.metadata else '',
            'description': result.metadata.get('description', '') if result.metadata else '',
            'keywords': result.metadata.get('keywords', '') if result.metadata else '',
            'detected_interactive_elements': detected_elements,
            'has_javascript': 'script' in result.html.lower() if result.html else False,
            'extraction_method': 'interactive_crawl4ai',
            'success': True,
            'content_length': len(content)
        }
        
        return content, metadata
    
    async def fallback_extraction(self, url):
        """Enhanced fallback extraction"""
        try:
            import aiohttp
            from bs4 import BeautifulSoup
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        title_tag = soup.find('title')
                        title = title_tag.get_text().strip() if title_tag else ''
                        
                        desc_tag = soup.find('meta', attrs={'name': 'description'})
                        description = desc_tag.get('content', '') if desc_tag else ''
                        
                        detected_elements = self.detect_interactive_elements(html)
                        
                        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
                            element.decompose()
                        
                        content = soup.get_text(separator='\n', strip=True)
                        
                        metadata = {
                            'url': url,
                            'status_code': response.status,
                            'title': title,
                            'description': description,
                            'keywords': '',
                            'detected_interactive_elements': detected_elements,
                            'has_javascript': '<script' in html.lower(),
                            'extraction_method': 'fallback_http',
                            'success': True,
                            'content_length': len(content)
                        }
                        
                        return content, metadata
                        
        except Exception as e:
            print(f"❌ Fallback extraction failed: {e}")
            
        return None, {'url': url, 'success': False, 'error': 'All extraction methods failed'}
    
    def clean_url_for_filename(self, url):
        """Convert URL to a clean filename"""
        parsed = urlparse(url)
        domain = parsed.netloc.replace('www.', '')
        path = parsed.path.strip('/').replace('/', '_')
        
        clean_domain = re.sub(r'[^\w\-.]', '_', domain)
        clean_path = re.sub(r'[^\w\-]', '_', path) if path else ''
        
        if clean_path:
            return f"{clean_domain}_{clean_path}"
        return clean_domain
    
    def extract_title_keywords(self, content, max_words=3):
        """Extract key words from content for filename"""
        if not content:
            return ""
        
        title_patterns = [
            r'# (.+?)(?:\n|$)',
            r'## (.+?)(?:\n|$)',
            r'<title>(.+?)</title>',
            r'<h1[^>]*>(.+?)</h1>',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
                words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
                return '_'.join(words[:max_words])
        
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content[:500].lower())
        common_words = {'about', 'home', 'contact', 'services', 'company', 'welcome', 'this', 'that', 'with', 'from'}
        meaningful_words = [w for w in words if w not in common_words]
        
        return '_'.join(meaningful_words[:max_words]) if meaningful_words else 'content'
    
    def generate_filename(self, url, content="", timestamp=True):
        """Generate a descriptive filename from URL and content"""
        base_name = self.clean_url_for_filename(url)
        keywords = self.extract_title_keywords(content)
        
        if keywords:
            filename = f"{base_name}_{keywords}"
        else:
            filename = base_name
        
        if timestamp:
            ts = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"{filename}_{ts}"
        
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename
    
    def add_enhanced_annotations(self, content, metadata):
        """Add enhanced annotations including interactive element detection"""
        annotations = f"""---
# Advanced Web Content Extraction Report
**Source URL:** {metadata.get('url', 'Unknown')}
**Extracted on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Page Title:** {metadata.get('title', 'N/A')}
**Status Code:** {metadata.get('status_code', 'N/A')}
**Content Length:** {len(content)} characters
**Extraction Method:** {metadata.get('extraction_method', 'Unknown')}
**Has JavaScript:** {metadata.get('has_javascript', False)}

## Interactive Elements Detected:
"""
        
        interactive_elements = metadata.get('detected_interactive_elements', [])
        if interactive_elements:
            for element in interactive_elements:
                annotations += f"- {element.title()}\n"
        else:
            annotations += "- None detected\n"
        
        annotations += "\n"
        
        if metadata.get('description'):
            annotations += f"**Description:** {metadata['description']}\n\n"
        
        headers = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        if headers:
            annotations += "## Table of Contents\n"
            for i, header in enumerate(headers[:15], 1):
                annotations += f"{i}. {header.strip()}\n"
            annotations += "\n"
        
        annotations += "---\n\n"
        return annotations + content
    
    def save_content(self, content, metadata, custom_filename=None):
        """Save extracted content with enhanced annotations"""
        if not content:
            print("❌ No content to save")
            return None
        
        if custom_filename:
            filename = custom_filename
        else:
            filename = self.generate_filename(metadata['url'], content)
        
        if not filename.endswith('.md'):
            filename += '.md'
        
        filepath = os.path.join(self.output_dir, filename)
        
        annotated_content = self.add_enhanced_annotations(content, metadata)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(annotated_content)
        
        metadata_filepath = filepath.replace('.md', '_metadata.json')
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Content saved to: {filepath}")
        print(f"📊 Metadata saved to: {metadata_filepath}")
        print(f"📄 Content length: {len(content)} characters")
        
        interactive_elements = metadata.get('detected_interactive_elements', [])
        if interactive_elements:
            print(f"🎯 Interactive elements detected: {', '.join(interactive_elements)}")
        
        return filepath
    
    async def run_interactive(self):
        """Interactive mode with extraction options"""
        print("🕷️ Advanced Web Content Extractor with Interactive Element Support")
        print("=" * 70)
        print("Modes:")
        print("  auto - Automatically detect and interact with elements")
        print("  basic - Simple extraction without interactions")
        print("  interactive - Medium level interactions")
        print("  full - Comprehensive interaction with all detected elements")
        
        while True:
            try:
                url = input("\n🌐 Enter website URL (or 'quit' to exit): ").strip()
                
                if url.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                mode = input("🎯 Extraction mode [auto/basic/interactive/full] (default: auto): ").strip().lower()
                if not mode:
                    mode = "auto"
                
                custom_name = input("📝 Custom filename (optional): ").strip()
                custom_name = custom_name if custom_name else None
                
                print(f"\n🚀 Starting {mode} extraction...")
                content, metadata = await self.extract_with_interactions(url, mode)
                
                if metadata.get('success'):
                    filepath = self.save_content(content, metadata, custom_name)
                    
                    preview = content[:400] + "..." if len(content) > 400 else content
                    print(f"\n📖 Content preview:\n{preview}")
                    
                else:
                    print(f"❌ Extraction failed: {metadata.get('error', 'Unknown error')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")

async def main():
    """Main function with enhanced command line support"""
    extractor = AdvancedWebExtractor()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "auto"
        custom_filename = sys.argv[3] if len(sys.argv) > 3 else None
        
        # Validate mode
        valid_modes = ["auto", "basic", "interactive", "full"]
        if mode not in valid_modes:
            print(f"❌ Invalid mode '{mode}'. Valid modes: {', '.join(valid_modes)}")
            print("Usage: python script.py <url> [mode] [custom_filename]")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"🌐 Extracting content from: {url} (mode: {mode})")
        content, metadata = await extractor.extract_with_interactions(url, mode)
        
        if metadata.get('success'):
            extractor.save_content(content, metadata, custom_filename)
        else:
            print(f"❌ Extraction failed: {metadata.get('error')}")
    else:
        await extractor.run_interactive()

if __name__ == "__main__":
    try:
        import aiohttp
        from bs4 import BeautifulSoup
    except ImportError:
        print("📦 Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp", "beautifulsoup4"])
        import aiohttp
        from bs4 import BeautifulSoup
    
    asyncio.run(main())