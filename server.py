#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Studio · yerel sunucu
- Arayüzü (index.html) http://127.0.0.1:8765 üzerinden sunar.
- Ollama'ya SUNUCU TARAFINDAN proxy yapar; böylece tarayıcı CORS/izin
  ayarı (OLLAMA_ORIGINS) olmadan yerel modeli kullanabilir.
Sadece Python standart kütüphanesini kullanır — pip kurulumu gerekmez.
"""
import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
import sys
import threading
import webbrowser

OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
PORT = int(os.environ.get("PORT", "8765"))
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass  # sessiz

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        try:
            self.wfile.write(data)
        except Exception:
            pass

    # ---- GET: statik dosyalar + Ollama etiketleri ----
    def do_GET(self):
        if self.path.startswith("/api/ollama/tags"):
            try:
                req = urllib.request.Request(OLLAMA + "/api/tags")
                with urllib.request.urlopen(req, timeout=10) as r:
                    self._json(json.loads(r.read().decode("utf-8")))
            except Exception as e:
                self._json({"error": str(e)}, 502)
            return
        # kök -> index.html
        if self.path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    # ---- POST: sohbet ve model indirme ----
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(length) if length else b""

        if self.path.startswith("/api/ollama/chat"):
            try:
                req = urllib.request.Request(
                    OLLAMA + "/api/chat", data=body,
                    headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=600) as r:
                    self._json(json.loads(r.read().decode("utf-8")))
            except urllib.error.HTTPError as e:
                self._json({"error": e.read().decode("utf-8", "ignore")}, e.code)
            except Exception as e:
                self._json({"error": str(e)}, 502)
            return

        if self.path.startswith("/api/ollama/pull"):
            # model indirmeyi akış olarak geçir (ilerleme için)
            try:
                req = urllib.request.Request(
                    OLLAMA + "/api/pull", data=body,
                    headers={"Content-Type": "application/json"})
                up = urllib.request.urlopen(req, timeout=3600)
                self.send_response(200)
                self.send_header("Content-Type", "application/x-ndjson")
                self.end_headers()
                while True:
                    chunk = up.read(1024)
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    except Exception:
                        break
            except Exception as e:
                self._json({"error": str(e)}, 502)
            return

        self.send_error(404)


def main():
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler)
    except OSError as e:
        print("Port %d kullanımda olabilir. Hata: %s" % (PORT, e))
        input("Kapatmak için Enter...")
        sys.exit(1)
    httpd.daemon_threads = True
    url = "http://127.0.0.1:%d/" % PORT
    print("=" * 48)
    print("  STUDIO calisiyor:  %s" % url)
    print("  Ollama adresi:     %s" % OLLAMA)
    print("  Kapatmak icin bu pencerede Ctrl+C")
    print("=" * 48)
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKapatiliyor...")
        httpd.shutdown()


if __name__ == "__main__":
    main()
