#!/usr/bin/env python3
"""
Test email configuration for KlingelAI - Detailed Diagnostics
"""
import smtplib
import socket
from email.mime.text import MIMEText

# EMAIL CONFIGURATION - UPDATE THESE VALUES
EMAIL_CONFIG = {
    'sender_email': 'your-email@hs-ruhrwest.de',  # Replace with your email
    'sender_password': 'your-app-specific-password',  # Replace with your password
    'recipient_email': 'recipient@example.com',  # Replace with recipient email
    'smtp_server': 'owa.hs-ruhrwest.de',
    'smtp_port': 587
}

def check_email_configuration():
    """Check and report on email configuration."""
    print("🔍 Email Configuration Check")
    print("=" * 50)
    
    config_issues = []
    
    # Check each configuration value
    if EMAIL_CONFIG['sender_email'] == 'your-email@hs-ruhrwest.de':
        print("❌ SENDER_EMAIL: NOT CONFIGURED (still default value)")
        config_issues.append('sender_email')
    else:
        print(f"✅ SENDER_EMAIL: {EMAIL_CONFIG['sender_email']}")
    
    if EMAIL_CONFIG['sender_password'] == 'your-app-specific-password':
        print("❌ SENDER_PASSWORD: NOT CONFIGURED (still default value)")
        config_issues.append('sender_password')
    else:
        password_display = '*' * min(len(EMAIL_CONFIG['sender_password']), 8)
        print(f"✅ SENDER_PASSWORD: {password_display} ({len(EMAIL_CONFIG['sender_password'])} characters)")
    
    if EMAIL_CONFIG['recipient_email'] == 'recipient@example.com':
        print("❌ RECIPIENT_EMAIL: NOT CONFIGURED (still default value)")
        config_issues.append('recipient_email')
    else:
        print(f"✅ RECIPIENT_EMAIL: {EMAIL_CONFIG['recipient_email']}")
    
    print(f"✅ SMTP_SERVER: {EMAIL_CONFIG['smtp_server']}")
    print(f"✅ SMTP_PORT: {EMAIL_CONFIG['smtp_port']}")
    
    print()
    
    # Summary
    if config_issues:
        print("❌ CONFIGURATION ISSUES FOUND:")
        print(f"   Unconfigured values: {', '.join(config_issues)}")
        print()
        print("🛠️  TO FIX:")
        print("   1. Open this script in a text editor")
        print("   2. Find the EMAIL_CONFIG dictionary at the top")
        print("   3. Replace the default values with your actual credentials:")
        print("      - sender_email: Your HS-Ruhrwest email address")
        print("      - sender_password: Your app-specific password")
        print("      - recipient_email: Where to send notifications")
        print("   4. Save the file and run this test again")
        print()
        return False
    else:
        print("✅ All email configuration values are set!")
        return True

def test_network_connectivity(smtp_server, smtp_port):
    """Test network connectivity to SMTP server."""
    print(f"🌐 Network Connectivity Test")
    print("=" * 50)
    
    try:
        print(f"🔌 Testing connection to {smtp_server}:{smtp_port}...")
        socket.create_connection((smtp_server, smtp_port), timeout=10)
        print("✅ Network connection successful!")
        return True
    except socket.timeout:
        print(f"❌ Connection timeout to {smtp_server}:{smtp_port}")
        print("   Possible issues:")
        print("   - Server is down")
        print("   - Firewall blocking connection")
        print("   - VPN required for campus network")
        return False
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        print("   Possible issues:")
        print("   - Incorrect server hostname")
        print("   - DNS server issues")
        return False
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

def test_smtp_connection(smtp_server, smtp_port):
    """Test SMTP server connection and capabilities."""
    print(f"📡 SMTP Server Test")
    print("=" * 50)
    
    try:
        print(f"🔌 Connecting to SMTP server {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print("✅ SMTP connection established!")
        
        # Get server capabilities
        print("📋 Server capabilities:")
        if hasattr(server, 'ehlo'):
            code, response = server.ehlo()
            if code == 250:
                capabilities = response.decode().split('\n')
                for cap in capabilities[1:]:  # Skip first line (server name)
                    if cap.strip():
                        print(f"   - {cap.strip()}")
        
        print("🔒 Testing TLS support...")
        server.starttls()
        print("✅ TLS connection established!")
        
        server.quit()
        return True
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_authentication(smtp_server, smtp_port, sender, password):
    """Test SMTP authentication."""
    print(f"🔑 Authentication Test")
    print("=" * 50)
    
    try:
        print(f"🔌 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        print("🔒 Starting TLS...")
        server.starttls()
        
        print(f"🔑 Attempting authentication for {sender}...")
        server.login(sender, password)
        
        print("✅ Authentication successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ AUTHENTICATION FAILED: {e}")
        print()
        print("🔍 DETAILED DIAGNOSIS:")
        error_code = str(e).split()[0] if str(e) else "Unknown"
        
        if "535" in str(e):
            print("   Error 535: Invalid credentials")
            print("   ➤ Your username/password combination is incorrect")
            print()
            print("💡 SOLUTIONS:")
            print("   1. ✅ Verify your email address is exactly correct")
            print("   2. 🔑 Use an APP-SPECIFIC PASSWORD (not your regular password)")
            print("   3. 🔐 Check if 2FA is enabled (requires app password)")
            print("   4. 📞 Contact HS-Ruhrwest IT support")
            
        elif "534" in str(e):
            print("   Error 534: Authentication mechanism not supported")
            print("   ➤ Server requires different authentication method")
            
        elif "530" in str(e):
            print("   Error 530: Authentication required")
            print("   ➤ Server requires authentication but credentials failed")
            
        else:
            print(f"   Unknown authentication error: {e}")
        
        print()
        print("🛠️  NEXT STEPS:")
        print("   1. Generate app-specific password in your email account")
        print("   2. Update environment variable:")
        print("      export SENDER_PASSWORD='your-app-specific-password'")
        print("   3. Run this test again")
        
        server.quit()
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error during authentication: {e}")
        return False

def test_email_sending(smtp_server, smtp_port, sender, password, recipient):
    """Test actual email sending."""
    print(f"📧 Email Sending Test")
    print("=" * 50)
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender, password)
        
        print("📝 Composing test email...")
        msg = MIMEText("This is a test email from KlingelAI configuration test.\n\nIf you receive this, your email setup is working correctly!")
        msg['Subject'] = 'KlingelAI Email Configuration Test - SUCCESS'
        msg['From'] = sender
        msg['To'] = recipient
        
        print(f"📤 Sending test email to {recipient}...")
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check {recipient} for the test message")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def test_email_connection():
    """Complete email configuration test with detailed diagnostics."""
    
    print("🔧 KlingelAI Email Configuration Diagnostics")
    print("=" * 60)
    print()
    
    # Step 1: Check email configuration
    if not check_email_configuration():
        print("❌ CRITICAL: Fix email configuration before proceeding!")
        return False
    
    print()
    
    # Get configuration
    sender = EMAIL_CONFIG['sender_email']
    password = EMAIL_CONFIG['sender_password']
    recipient = EMAIL_CONFIG['recipient_email']
    smtp_server = EMAIL_CONFIG['smtp_server']
    smtp_port = EMAIL_CONFIG['smtp_port']
    
    # Step 2: Test network connectivity
    if not test_network_connectivity(smtp_server, smtp_port):
        print("❌ CRITICAL: Cannot reach SMTP server!")
        return False
    
    print()
    
    # Step 3: Test SMTP connection
    if not test_smtp_connection(smtp_server, smtp_port):
        print("❌ CRITICAL: SMTP server connection failed!")
        return False
    
    print()
    
    # Step 4: Test authentication
    if not test_authentication(smtp_server, smtp_port, sender, password):
        print("❌ CRITICAL: Authentication failed!")
        return False
    
    print()
    
    # Step 5: Test email sending
    if not test_email_sending(smtp_server, smtp_port, sender, password, recipient):
        print("❌ WARNING: Email sending failed!")
        return False
    
    print()
    print("🎉 ALL TESTS PASSED!")
    print("✅ Your KlingelAI email configuration is working perfectly!")
    print()
    print("🚀 You can now run KlingelAI with confidence!")
    
    return True

if __name__ == "__main__":
    test_email_connection()