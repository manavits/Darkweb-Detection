import requests
from bs4 import BeautifulSoup
from app.models import DarkWebThreat
from app import db, mail
from datetime import datetime
from flask_mail import Message
import subprocess
import os
import time
import socket

# ------------------- TOR BOOTSTRAP -------------------

def wait_for_tor(timeout=60):
    attempts = 0
    while attempts < timeout:
        try:
            with socket.create_connection(("127.0.0.1", 9050), timeout=5):
                print("🟢 Tor is ready.")
                return True
        except socket.error:
            attempts += 1
            time.sleep(1)
    print("❌ Tor failed to start within timeout.")
    return False

def start_tor():
    tor_path = r"C:\tor\tor.exe"
    torrc_path = r"C:\tor\torrc"
    data_dir = r"C:\tor\Data\Tor"

    os.makedirs(data_dir, exist_ok=True)

    try:
        subprocess.Popen(
            [tor_path, "-f", torrc_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("⏳ Starting Tor...")
        if not wait_for_tor():
            raise RuntimeError("Tor proxy not available.")
    except Exception as e:
        print(f"❌ Failed to start Tor: {e}")
        exit(1)

# ------------------- ALERT MAIL -------------------

def send_alert(subject, body, recipients):
    try:
        message = Message(subject=subject, body=body, recipients=[recipients])
        mail.send(message)
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

# ------------------- SCAN TOR SITES -------------------

def scan_tor_sites(keywords):
    start_tor()

    # ✅ Use known good legal onion site for testing
    tor_sites = [
        "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion"

    ]

    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    for site in tor_sites:
        success = False
        for attempt in range(3):  # Retry 3 times
            try:
                print(f"🔍 Scanning {site} (Attempt {attempt+1})")
                response = requests.get(site, proxies=proxies, timeout=30)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    text_content = soup.get_text()

                    for keyword in keywords:
                        if keyword.lower() in text_content.lower():
                            print(f"🚨 Keyword '{keyword}' found on {site}")
                            threat = DarkWebThreat(
                                url=site,
                                threat_description=f"Keyword '{keyword}' found.",
                                timestamp=datetime.utcnow()
                            )
                            db.session.add(threat)
                            db.session.commit()

                            send_alert(
                                subject="🚨 Dark Web Threat Found",
                                body=f"Keyword: {keyword}\nSite: {site}",
                                recipients='admin@example.com'
                            )
                    success = True
                    break
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Failed to scan {site}: {e}")
                time.sleep(5)
        if not success:
            print(f"❌ Could not scan {site} after 3 attempts.")

# ------------------- Example usage -------------------

if __name__ == "__main__":
    keywords = ["email", "login", "bitcoin", "encryption"]
    scan_tor_sites(keywords)
