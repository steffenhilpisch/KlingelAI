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
print(GeckoDriverManager().install())
import os

driver_path = GeckoDriverManager().install()

# Email-Funktion
def send_email(subject, new_entries):
    sender = "KI-Klingel@hs-ruhrwest.de"
    recipient = "steffen.hilpisch@hs-ruhrwest.de"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Erstelle den eigentlichen E-Mail-Text im HTML-Format
    body_content = ""
    for entry in new_entries:  # Hier übergeben wir nun die Liste der Dictionaries
        title = entry['title']
        abstract = entry['abstract']
        date = entry['date']
        authors = entry['authors']
        link = entry['link']

        # HTML für jede Publikation erstellen
        body_content += f"""
        <p><strong>{title}</strong></p>
        <p><strong>Autoren:</strong> {authors}</p>
        <p><strong>Datum:</strong> {date}</p>
        <p><strong>Abstract:</strong> {abstract}</p>
        <p><a href=\"{link}\">Link zur Publikation</a></p>
        <hr>
        """

    # HTML-Body der E-Mail
    html_body = f"""
    <html>
    <body>
        <h2 style="font-size: 24px; font-weight: bold;">Neue Publikationen</h2>
        {body_content}  <!-- Hier wird die generierte Liste eingefügt -->
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP("owa.hs-ruhrwest.de", 587) as server:
            server.starttls()
            server.login("KI-Klingel", "DWHRE3454653%f45")
            server.sendmail(sender, recipient, msg.as_string())
        print("✅ E-Mail gesendet!")
    except Exception as e:
        print(f"❌ Fehler beim Senden der E-Mail: {e}")



# Funktion zum Laden der bekannten Links aus einer Datei
def load_known_links(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return set(f.read().splitlines())
    return set()

# Funktion zum Speichern der Links in eine Datei
def save_known_links(filename, links):
    with open(filename, "w") as f:
        f.write("\n".join(links))

# Funktion zur Extraktion von Detailinformationen
def extract_details(link):
    options = Options()
    options.add_argument("--headless")

    service = Service(driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(link)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Titel extrahieren
        title_tag = soup.find("h1", class_="ng-star-inserted")
        title = title_tag.text.strip() if title_tag else "Kein Titel gefunden"

        # Abstract extrahieren
        abstract_tag = soup.find("div", attrs={"data-test": "formatted-text"})
        if abstract_tag:
            abstract = abstract_tag.get_text(strip=True)
        else:
            abstract = "Kein Abstract gefunden"

        # Datum extrahieren
        date_tag = soup.find("span", class_="text-value")
        date = date_tag.text.strip() if date_tag else "Kein Datum gefunden"

        # Autoren extrahieren
        author_tags = soup.select(".fp-ItemPage-metadata-author span.text-value")
        authors = ", ".join([author.text.strip() for author in author_tags]) if author_tags else "Keine Autoren gefunden"

        return title, abstract, date, authors

    except Exception as e:
        print(f"❌ Fehler beim Extrahieren der Details: {e}")
        return "Fehler", "Fehler", "Fehler", "Fehler"

    finally:
        driver.quit()

# Funktion zur Extraktion von Links
# Funktion zur Extraktion von Links
def scrape_fhg_links(url, known_links):
    options = Options()
    options.add_argument("--headless")

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fhg-grid-item"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

    except Exception as e:
        print(f"❌ Fehler beim Laden der Seite: {e}")
        driver.quit()
        return known_links, []  # Gibt bekannt Links und leere Liste zurück

    finally:
        driver.quit()

    container = soup.find("div", class_="fhg-grid-item fhg-grid-3-2-1")
    if not container:
        print("❌ Container mit der Tabelle nicht gefunden!")
        return known_links, []

    content = container.find("div", class_="fhg-content fhg-richtext")
    if not content:
        print("❌ Content-Bereich nicht gefunden!")
        return known_links, []

    table = content.find("table")
    if not table:
        print("❌ Tabelle nicht gefunden!")
        return known_links, []

    new_links = set(a_tag["href"] for a_tag in table.find_all("a", href=True) if a_tag["href"].startswith("http"))

    updated_links = known_links.union(new_links)
    new_entries = []

    for link in new_links - known_links:
        title, abstract, date, authors = extract_details(link)
        # Speichern als Dictionary
        new_entries.append({
            'title': title,
            'abstract': abstract,
            'date': date,
            'authors': authors,
            'link': link
        })

    if new_entries:
        print(f"✅ {len(new_entries)} neue Links gefunden!")
        # Übergabe der Liste von Dictionaries
        send_email("Neue Fraunhofer Publikationen", new_entries)
    else:
        print("🔍 Keine neuen Links gefunden.")

    return updated_links, new_entries  # Rückgabe von bekannten Links und neuen Einträgen als Liste von Dictionaries



# Hauptskript
url = "https://www.iuk.fraunhofer.de/de/forschung-entwicklung/wissenschaftliche-publikationen/ki.html"
link_file = "known_links.txt"

known_links = load_known_links(link_file)

# Links und neue Einträge extrahieren
known_links, new_entries = scrape_fhg_links(url, known_links)

save_known_links(link_file, known_links)

print("✅ Fertig! Bekannte Links aktualisiert.")

#TODO: website aufbau wurde geändert. neues link scraping aufsetzen