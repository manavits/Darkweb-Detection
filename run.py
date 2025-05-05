import os
import subprocess
import time
import threading
from app import create_app, db
from app.darkweb_scanner import scan_tor_sites
from app.config import Config

app = create_app()

# ✅ Function to start Tor
def start_tor():
    tor_path = r"C:\tor\tor.exe"  # Adjust this path if necessary
    if not os.path.exists(tor_path):
        print(f"❌ Tor not found at {tor_path}")
        return None

    try:
        tor_process = subprocess.Popen([tor_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("🟢 Tor started successfully.")
        time.sleep(7)  # Wait for Tor to initialize
        return tor_process
    except Exception as e:
        print(f"❌ Could not start Tor: {e}")
        return None

def background_scanner():
    with app.app_context():  # Ensure Flask context is available
        while True:
            print("🔍 Scanning Dark Web...")
            try:
                scan_tor_sites(Config.SCAN_KEYWORDS)
                print(f"✅ Scan complete. Sleeping for {Config.SCAN_INTERVAL_SECONDS} seconds...")
            except Exception as e:
                print(f"⚠ Scan failed: {e}")
            time.sleep(Config.SCAN_INTERVAL_SECONDS)

if __name__ == '__main__':
    tor_process = start_tor()

    if tor_process:
        try:
            # Start scanner in a background thread
            scanner_thread = threading.Thread(target=background_scanner, daemon=True)
            scanner_thread.start()

            # Run the Flask app
            app.run(debug=True, use_reloader=False)  # `use_reloader=False` to avoid restarting multiple times

        except Exception as e:
            print(f"❌ Error occurred: {e}")
        finally:
            # Terminate Tor process once the app is stopped
            print("🛑 Shutting down Flask app...")
            tor_process.terminate()
            tor_process.wait()  # Ensure the process terminates properly
            print("🛑 Tor process terminated.")
    else:
        print("❌ Tor did not start. Exiting.")



