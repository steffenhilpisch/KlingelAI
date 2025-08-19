#!/usr/bin/env python3
"""
Test email configuration for KlingelAI - Detailed Diagnostics
"""
import smtplib
import os
import socket
from email.mime.text import MIMEText

def check_environment_variables():
    """Check and report on all environment variables."""
    print("🔍 Environment Variables Check")
    print("=" * 50)
    
    # Required variables
    required_vars = {
        'SENDER_EMAIL': 'Email address to send from',
        'SENDER_PASSWORD': 'Password or app-specific password',
        'RECIPIENT_EMAIL': 'Email address to send to'
    }
    
    # Optional variables with defaults
    optional_vars = {
        'SMTP_SERVER': ('SMTP server hostname', 'owa.hs-ruhrwest.de'),
        'SMTP_PORT': ('SMTP server port', '587')
    }
    
    missing_required = []
    empty_required = []
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value is None:
            print(f"❌ {var}: NOT SET ({description})")
            missing_required.append(var)
        elif value.strip() == "":
            print(f"⚠️  {var}: EMPTY ({description})")
            empty_required.append(var)
        else:
            # Show partial value for security
            if 'PASSWORD' in var:
                display_value = f"{'*' * min(len(value), 8)} ({len(value)} characters)"
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
    
    print()
    
    # Check optional variables
    print("📋 Optional Variables (with defaults)")
    print("-" * 30)
    for var, (description, default) in optional_vars.items():
        value = os.getenv(var, default)
        is_default = os.getenv(var) is None
        status = "DEFAULT" if is_default else "SET"
        print(f"{'🔧' if is_default else '✅'} {var}: {value} ({status})")
    
    print()
    
    # Summary
    if missing_required or empty_required:
        print("❌ CONFIGURATION ISSUES FOUND:")
        if missing_required:
            print(f"   Missing variables: {', '.join(missing_required)}")
        if empty_required:
            print(f"   Empty variables: {', '.join(empty_required)}")
        print()
        print("🛠️  TO FIX, RUN THESE COMMANDS:")
        for var in missing_required + empty_required:
            if var == 'SENDER_EMAIL':
                print(f"   export {var}='your-email@hs-ruhrwest.de'")
            elif var == 'SENDER_PASSWORD':
                print(f"   export {var}='your-app-specific-password'")
            elif var == 'RECIPIENT_EMAIL':
                print(f"   export {var}='recipient@example.com'")
        print()
        return False
    else:
        print("✅ All required environment variables are set!")
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
    
    # Step 1: Check environment variables
    if not check_environment_variables():
        print("❌ CRITICAL: Fix environment variables before proceeding!")
        return False
    
    print()
    
    # Get configuration
    sender = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    recipient = os.getenv('RECIPIENT_EMAIL')
    smtp_server = os.getenv('SMTP_SERVER', 'owa.hs-ruhrwest.de')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
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