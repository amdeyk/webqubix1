# Save this as fixed_qubix_extract.py
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def extract_qubix_content():
    browser_config = BrowserConfig(
        headless=True,
        verbose=True
    )
    
    # Fixed configuration - removed problematic wait_for parameter
    run_config = CrawlerRunConfig(
        # Don't use wait_for with integer, use wait_until instead
        wait_until="networkidle",  # Wait until network activity stops
        page_timeout=30000,  # 30 seconds timeout
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            result = await crawler.arun(
                url="https://www.qubixsolutions.in",
                config=run_config
            )
            
            print("=== EXTRACTION RESULTS ===")
            print(f"✅ Success: {result.success}")
            print(f"📄 Status Code: {result.status_code}")
            
            if result.success and result.markdown:
                content = result.markdown.fit_markdown or result.markdown.raw_markdown
                
                if content and content.strip():
                    with open("qubix_content_fixed.md", "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"✅ Content extracted successfully!")
                    print(f"📄 Content length: {len(content)} characters")
                    print(f"💾 Saved to: qubix_content_fixed.md")
                else:
                    print("⚠️ Content is empty, trying alternative extraction...")
                    
                    # Try to get content from HTML
                    if result.html:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(result.html, 'html.parser')
                        
                        # Remove unwanted elements
                        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                            element.decompose()
                        
                        text_content = soup.get_text(separator='\n', strip=True)
                        
                        if text_content:
                            with open("qubix_content_from_html.txt", "w", encoding="utf-8") as f:
                                f.write(text_content)
                            print(f"✅ Extracted from HTML: {len(text_content)} characters")
                        else:
                            print("❌ No content found in HTML either")
            else:
                print(f"❌ Extraction failed: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}")
                
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(extract_qubix_content())