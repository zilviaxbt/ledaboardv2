import http.server
import socketserver
import webbrowser
import threading
import os
import json

try:
    # Import the balance fetcher if available
    import fetch_galachain_balances as balance_fetcher
except Exception:
    balance_fetcher = None


def open_browser(url: str) -> None:
    try:
        webbrowser.open_new_tab(url)
    except Exception:
        pass


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, status: int = 200, content_type: str = "application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_POST(self):
        if self.path == "/api/refresh":
            if balance_fetcher is None:
                self._set_headers(500)
                self.wfile.write(json.dumps({"ok": False, "error": "fetch_galachain_balances not available"}).encode("utf-8"))
                return
            try:
                # Run the balance fetcher synchronously
                balance_fetcher.main()
                self._set_headers(200)
                self.wfile.write(json.dumps({"ok": True, "message": "balances.csv refreshed"}).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode("utf-8"))
        else:
            super().do_POST()


def run_server(port: int = 8000) -> None:
    # Ensure we serve files from the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("127.0.0.1", port), RequestHandler) as httpd:
        print(f"Serving at http://localhost:{port}")
        print("Press Ctrl+C to stop.")
        # Open browser shortly after server starts
        threading.Timer(0.8, open_browser, args=(f"http://localhost:{port}",)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")


if __name__ == "__main__":
    run_server(8000)


