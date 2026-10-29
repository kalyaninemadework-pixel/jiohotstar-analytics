"""
JioHotstar Analytics Dashboard Launcher
Starts a local lightweight HTTP server and automatically opens the interactive dashboard in your browser.

Author: Kalyani Gajanan Nemade (Independent Analytics Project)
"""

import os
import sys
import webbrowser
import http.server
import socketserver

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

def start_dashboard():
    print("=" * 70)
    print("JIOHOTSTAR UNIFIED OTT ANALYTICS DASHBOARD")
    print("Created by: Kalyani Gajanan Nemade (Flagship Analytics Case Study)")
    print("=" * 70)
    print(f"\n[+] Serving interactive dashboard from: {DASHBOARD_DIR}")
    print(f"[+] Access URL: http://localhost:{PORT}/index.html")
    print("[+] Press Ctrl+C in terminal to stop the dashboard server.\n")

    # Open browser automatically
    webbrowser.open(f"http://localhost:{PORT}/index.html")

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard server stopped.")

if __name__ == "__main__":
    start_dashboard()
