"""
KlingelAI - Economic AI Publications Monitor

This script monitors Fraunhofer IUK AI publications and filters for those with economic focus.
It sends email notifications when new economic AI publications are found.

Updated for the new website structure (2025) and includes economic keyword filtering.

Author: Updated by OpenHands AI Assistant
Date: 2025-08-19
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webdriver_manager.firefox import GeckoDriverManager
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Economic keywords for filtering publications (German and English)
ECONOMIC_KEYWORDS = [
    # English keywords
    'economic', 'economy', 'business', 'financial', 'finance', 'market', 'industry', 'industrial',
    'commercial', 'trade', 'cost', 'profit', 'revenue', 'investment', 'banking', 'insurance',
    'management', 'enterprise', 'corporate', 'startup', 'entrepreneurship', 'innovation',
    'productivity', 'efficiency', 'optimization', 'supply chain', 'logistics', 'manufacturing',
    'retail', 'e-commerce', 'digital transformation', 'automation', 'workforce', 'employment',
    'labor', 'human resources', 'strategy', 'planning', 'decision making', 'analytics',
    'data-driven', 'business intelligence', 'competitive', 'sustainability', 'green economy',
    'circular economy', 'energy efficiency', 'smart city', 'smart grid', 'fintech',
    'insurtech', 'regtech', 'proptech', 'healthtech', 'edtech', 'agtech', 'cleantech',
    'blockchain', 'cryptocurrency', 'digital currency', 'payment', 'transaction',
    
    # German keywords
    'wirtschaft', 'ökonomie', 'geschäft', 'finanzen', 'markt', 'industrie', 'handel',
    'kosten', 'gewinn', 'umsatz', 'investition', 'unternehmen', 'startup', 'innovation',
    'produktivität', 'effizienz', 'optimierung', 'lieferkette', 'logistik', 'fertigung',
    'einzelhandel', 'digitalisierung', 'automatisierung', 'arbeitskraft', 'beschäftigung',
    'strategie', 'planung', 'entscheidung', 'analytik', 'wettbewerb', 'nachhaltigkeit',
    'kreislaufwirtschaft', 'energieeffizienz', 'intelligente stadt', 'fintech', 'blockchain',
    'kryptowährung', 'zahlung', 'transaktion', 'fachkräftemangel', 'arbeitsmarkt'
]

def has_economic_focus(title, abstract=""):
    """
    Check if a publication has economic focus based on keywords.
    
    Args:
        title (str): Publication title
        abstract (str): Publication abstract
        
    Returns:
        bool: True if publication has economic focus
    """
    text_to_check = (title + " " + abstract).lower()
    matches = sum(1 for keyword in ECONOMIC_KEYWORDS if keyword.lower() in text_to_check)
    return matches > 0

# EMAIL CONFIGURATION - UPDATE THESE VALUES
EMAIL_CONFIG = {
    'sender_email': 'your-email@hs-ruhrwest.de',  # Replace with your email
    'sender_password': 'your-app-specific-password',  # Replace with your password
    'recipient_email': 'recipient@example.com',  # Replace with recipient email
    'smtp_server': 'owa.hs-ruhrwest.de',
    'smtp_port': 587
}

def send_email(subject, new_entries):
    """
    Send email with new economic publications.
    
    Args:
        subject (str): Email subject
        new_entries (list): List of publication dictionaries
        
    Returns:
        bool: True if email sent successfully
    """
    # Get email credentials from configuration
    sender = EMAIL_CONFIG['sender_email']
    password = EMAIL_CONFIG['sender_password']
    recipient = EMAIL_CONFIG['recipient_email']
    smtp_server = EMAIL_CONFIG['smtp_server']
    smtp_port = EMAIL_CONFIG['smtp_port']
    
    # Check if credentials are still default values
    if sender == 'your-email@hs-ruhrwest.de' or password == 'your-app-specific-password':
        logger.warning("Email credentials not configured! Please update EMAIL_CONFIG in the script.")
        logger.warning("Set your actual email, password, and recipient in the EMAIL_CONFIG dictionary.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Create email content
    body_content = ""
    for entry in new_entries:
        title = entry['title']
        abstract = entry['abstract']
        date = entry['date']
        authors = entry['authors']
        link = entry['link']
        pub_type = entry.get('publication_type', 'Unknown')

        body_content += f"""
        <div style="margin-bottom: 20px; padding: 15px; border-left: 3px solid #0066cc;">
            <h3 style="color: #0066cc; margin-top: 0;">{title}</h3>
            <p><strong>Authors:</strong> {authors}</p>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Publication Type:</strong> {pub_type}</p>
            <p><strong>Abstract:</strong> {abstract}</p>
            <p><a href="{link}" style="color: #0066cc; text-decoration: none;">🔗 Link to Publication</a></p>
        </div>
        <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2 style="color: #0066cc; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">
            🔬 New Economic AI Publications from Fraunhofer
        </h2>
        <p>Found <strong>{len(new_entries)}</strong> new publications with economic focus:</p>
        {body_content}
        <footer style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; font-size: 12px;">
            <p>This email was automatically generated by KlingelAI</p>
            <p>Source: <a href="https://www.iuk.fraunhofer.de/de/forschung-entwicklung/wissenschaftliche-publikationen/ki.html">Fraunhofer IUK AI Publications</a></p>
        </footer>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        logger.info(f"Email sent successfully to {recipient}!")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def load_known_links(filename):
    """Load known links from file."""
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set()

def save_known_links(filename, links):
    """Save links to file."""
    with open(filename, "w", encoding='utf-8') as f:
        f.write("\n".join(links))

def extract_details(link):
    """
    Extract details from a publication link.
    
    Args:
        link (str): Publication URL
        
    Returns:
        tuple: (title, abstract, date, authors)
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        logger.info(f"Extracting details from: {link}")
        driver.get(link)
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Try different selectors for title
        title = "No title found"
        title_selectors = [
            "h1.ng-star-inserted",
            "h1",
            ".title",
            "[data-test='title']",
            ".publication-title"
        ]
        
        for selector in title_selectors:
            title_tag = soup.select_one(selector)
            if title_tag:
                title = title_tag.get_text(strip=True)
                break

        # Try different selectors for abstract
        abstract = "No abstract found"
        abstract_selectors = [
            "[data-test='formatted-text']",
            ".abstract",
            ".description",
            ".summary",
            "[data-test='abstract']"
        ]
        
        for selector in abstract_selectors:
            abstract_tag = soup.select_one(selector)
            if abstract_tag:
                abstract = abstract_tag.get_text(strip=True)
                break

        # Try different selectors for date
        date = "No date found"
        date_selectors = [
            "span.text-value",
            ".date",
            ".publication-date",
            "[data-test='date']"
        ]
        
        for selector in date_selectors:
            date_tag = soup.select_one(selector)
            if date_tag:
                date = date_tag.get_text(strip=True)
                break

        # Try different selectors for authors
        authors = "No authors found"
        author_selectors = [
            ".fp-ItemPage-metadata-author span.text-value",
            ".authors",
            ".author",
            "[data-test='authors']"
        ]
        
        for selector in author_selectors:
            author_tags = soup.select(selector)
            if author_tags:
                authors = ", ".join([author.get_text(strip=True) for author in author_tags])
                break

        logger.info(f"Successfully extracted: {title[:50]}...")
        return title, abstract, date, authors

    except Exception as e:
        logger.error(f"Error extracting details from {link}: {e}")
        return "Error", "Error", "Error", "Error"

    finally:
        driver.quit()

def scrape_fhg_links(url, known_links):
    """
    Scrape links from the Fraunhofer AI publications page and filter for economic focus.
    
    Args:
        url (str): URL to scrape
        known_links (set): Set of already known publication links
        
    Returns:
        tuple: (updated_known_links, economic_entries)
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        logger.info(f"Loading page: {url}")
        driver.get(url)

        # Wait for the content to load - updated selector for new website structure
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        logger.info("Page loaded successfully")

    except Exception as e:
        logger.error(f"Error loading page: {e}")
        driver.quit()
        return known_links, []

    finally:
        driver.quit()

    # Find the table with publications - updated for new website structure
    table = soup.find("table")
    if not table:
        logger.error("Publications table not found!")
        return known_links, []

    logger.info("Found publications table")

    # Extract all links from the table
    links_in_table = []
    rows = table.find_all("tr")
    
    for row in rows[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) >= 2:  # Year, Title/Author, Type
            title_cell = cells[1]  # Title/Author column
            link_tag = title_cell.find("a", href=True)
            if link_tag and link_tag["href"].startswith("http"):
                links_in_table.append({
                    'link': link_tag["href"],
                    'title': link_tag.get_text(strip=True),
                    'year': cells[0].get_text(strip=True) if cells[0] else "Unknown",
                    'pub_type': cells[2].get_text(strip=True) if len(cells) > 2 else "Unknown"
                })

    logger.info(f"Found {len(links_in_table)} total publications")

    # Filter for new links
    new_link_data = [item for item in links_in_table if item['link'] not in known_links]
    logger.info(f"Found {len(new_link_data)} new publications")

    # Process new links and filter for economic focus
    economic_entries = []
    
    for item in new_link_data:
        link = item['link']
        basic_title = item['title']
        
        # First check if title has economic keywords (quick filter)
        if has_economic_focus(basic_title):
            logger.info(f"Economic relevance detected in title: {basic_title[:50]}...")
            
            # Extract detailed information
            title, abstract, date, authors = extract_details(link)
            
            # Double-check with full content
            if has_economic_focus(title, abstract):
                entry = {
                    'title': title,
                    'abstract': abstract,
                    'date': date,
                    'authors': authors,
                    'link': link,
                    'publication_type': item['pub_type'],
                    'year': item['year']
                }
                economic_entries.append(entry)
                logger.info(f"Added economic publication: {title[:50]}...")
            else:
                logger.info(f"Filtered out after detailed check: {title[:50]}...")
        else:
            logger.debug(f"Skipped non-economic: {basic_title[:50]}...")
        
        # Small delay to be respectful to the server
        time.sleep(1)

    # Update known links with all new links (not just economic ones)
    all_links = set(item['link'] for item in links_in_table)
    updated_links = known_links.union(all_links)

    logger.info(f"Summary: {len(links_in_table)} total, {len(new_link_data)} new, {len(economic_entries)} economic")

    if economic_entries:
        logger.info(f"{len(economic_entries)} new economic AI publications found!")
        send_email("New Economic AI Publications from Fraunhofer", economic_entries)
    else:
        logger.info("No new economic AI publications found.")

    return updated_links, economic_entries

def main():
    """Main function to run the scraper."""
    logger.info("KlingelAI - Economic AI Publications Monitor")
    logger.info("=" * 50)
    
    url = "https://www.iuk.fraunhofer.de/de/forschung-entwicklung/wissenschaftliche-publikationen/ki.html"
    link_file = "known_links.txt"

    # Load known links
    known_links = load_known_links(link_file)
    logger.info(f"Loaded {len(known_links)} known publications")

    # Scrape for new economic publications
    known_links, new_entries = scrape_fhg_links(url, known_links)

    # Save updated links
    save_known_links(link_file, known_links)
    logger.info(f"Saved {len(known_links)} total known publications")

    logger.info("Monitoring complete!")

if __name__ == "__main__":
    main()