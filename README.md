# KlingelAI - Economic AI Publications Monitor

An automated monitoring system for Fraunhofer IUK AI publications with economic focus. The system scrapes the Fraunhofer website, filters publications based on economic keywords, and sends email notifications for new relevant publications.

## 🚀 Features

- **Economic Focus Filtering**: Automatically filters AI publications for economic relevance using comprehensive keyword matching (German and English)
- **Website Structure Adaptation**: Updated for the current Fraunhofer website structure (2025)
- **Email Notifications**: Sends beautifully formatted HTML emails with new economic publications
- **Duplicate Prevention**: Tracks known publications to avoid duplicate notifications
- **Robust Error Handling**: Comprehensive error handling and logging
- **Security**: Uses environment variables for email credentials (no hardcoded passwords)

## 📋 Requirements

- Python 3.7+
- Firefox browser
- Required Python packages (install with pip):
  ```bash
  pip install selenium beautifulsoup4 webdriver-manager requests
  ```

## 🔧 Setup

1. **Install Dependencies**:
   ```bash
   pip install selenium beautifulsoup4 webdriver-manager requests
   ```

2. **Install Firefox** (if not already installed):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install firefox-esr
   
   # macOS
   brew install firefox
   
   # Windows: Download from https://www.mozilla.org/firefox/
   ```

3. **Configure Email Credentials** (set environment variables):
   ```bash
   export SENDER_EMAIL="your-email@example.com"
   export SENDER_PASSWORD="your-password"
   export RECIPIENT_EMAIL="recipient@example.com"
   export SMTP_SERVER="your-smtp-server.com"  # Optional, defaults to owa.hs-ruhrwest.de
   export SMTP_PORT="587"  # Optional, defaults to 587
   ```

## 🏃‍♂️ Usage

### Basic Usage
```bash
python KlingelAI.py
```

### Email Configuration Test
```bash
python test_email.py
```

This diagnostic tool will:
- ✅ Check all environment variables
- 🌐 Test network connectivity to SMTP server
- 📡 Verify SMTP server capabilities
- 🔑 Test authentication with your credentials
- 📧 Send a test email
- 🔍 Provide detailed error diagnosis if anything fails

## 📊 Economic Keywords

The system filters publications based on a comprehensive list of economic keywords in both German and English:

**English**: economic, economy, business, financial, finance, market, industry, industrial, commercial, trade, cost, profit, revenue, investment, banking, insurance, management, enterprise, corporate, startup, entrepreneurship, innovation, productivity, efficiency, optimization, supply chain, logistics, manufacturing, retail, e-commerce, digital transformation, automation, workforce, employment, labor, human resources, strategy, planning, decision making, analytics, data-driven, business intelligence, competitive, sustainability, green economy, circular economy, energy efficiency, smart city, smart grid, fintech, insurtech, regtech, proptech, healthtech, edtech, agtech, cleantech, blockchain, cryptocurrency, digital currency, payment, transaction

**German**: wirtschaft, ökonomie, geschäft, finanzen, markt, industrie, handel, kosten, gewinn, umsatz, investition, unternehmen, startup, innovation, produktivität, effizienz, optimierung, lieferkette, logistik, fertigung, einzelhandel, digitalisierung, automatisierung, arbeitskraft, beschäftigung, strategie, planung, entscheidung, analytik, wettbewerb, nachhaltigkeit, kreislaufwirtschaft, energieeffizienz, intelligente stadt, fintech, blockchain, kryptowährung, zahlung, transaktion, fachkräftemangel, arbeitsmarkt

## 📁 Files

- `KlingelAI.py` - Main production script
- `test_email.py` - Email configuration diagnostic tool
- `requirements.txt` - Python dependencies
- `.env.example` - Configuration template
- `known_links.txt` - Automatically generated file to track processed publications
- `README.md` - This documentation

## 🔄 How It Works

1. **Web Scraping**: Uses Selenium to load the Fraunhofer AI publications page
2. **Table Parsing**: Extracts publication information from the HTML table
3. **Economic Filtering**: Applies keyword matching to identify economically relevant publications
4. **Detail Extraction**: For relevant publications, extracts detailed information (title, abstract, authors, date)
5. **Duplicate Prevention**: Compares against known publications to avoid duplicates
6. **Email Notification**: Sends formatted HTML email with new economic publications
7. **State Persistence**: Saves processed publications to avoid future duplicates

## 🛠️ Customization

### Adding Keywords
Edit the `ECONOMIC_KEYWORDS` list in the script to add more relevant keywords.

### Changing Email Format
Modify the `send_email()` function to customize the email template.

### Adjusting Filters
Modify the `has_economic_focus()` function to change filtering logic.

## 🔒 Security Notes

- **Never commit email credentials to version control**
- Use environment variables for sensitive information
- The script uses headless browser mode for security
- Email passwords should use app-specific passwords when possible

## 🐛 Troubleshooting

### Common Issues

1. **Firefox not found**: Install Firefox browser
2. **Email authentication failed**: Check credentials and use app-specific passwords
3. **Website structure changed**: The script includes multiple selectors for robustness
4. **Timeout errors**: Increase wait times in WebDriverWait calls

### Logging
The script includes comprehensive logging. Check the console output for detailed information about the scraping process.

## 📈 Performance

- Processing time: ~1-2 seconds per publication for detail extraction
- Memory usage: Minimal (headless browser mode)
- Network usage: Respectful with 1-second delays between requests

## 🔄 Automation

To run automatically, set up a cron job:

```bash
# Run every day at 9 AM
0 9 * * * cd /path/to/KlingelAI && python KlingelAI.py >> klingelai.log 2>&1
```

## 📝 Changelog

### Version 2.0 (2025-08-19)
- ✅ Updated for new Fraunhofer website structure
- ✅ Added economic keyword filtering
- ✅ Improved security (environment variables for credentials)
- ✅ Enhanced error handling and logging
- ✅ Better email formatting
- ✅ Comprehensive documentation

### Version 1.0 (Original)
- Basic web scraping functionality
- Email notifications
- Link tracking

## 📄 License

This project is for educational and research purposes. Please respect the Fraunhofer website's terms of service and robots.txt when using this script.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!