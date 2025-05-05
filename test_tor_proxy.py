import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

try:
    r = requests.get("https://check.torproject.org", proxies=proxies, timeout=10)
    print("✓ Response status:", r.status_code)
    if "Congratulations" in r.text:
        print("✓ You are using Tor!")
    else:
        print("✗ Not using Tor.")
except Exception as e:
    print("✗ Error using Tor proxy:", e)
