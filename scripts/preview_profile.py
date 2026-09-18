"""Serve a local GitHub-like README preview; GitHub is the final renderer."""

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import markdown

from build_profile import ROOT


STYLE = """
:root { color-scheme: dark light; }
* { box-sizing: border-box; }
body { margin: 0; background: #0d1117; color: #e6edf3;
       font: 16px/1.6 -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
main { max-width: 1012px; margin: 24px auto; padding: 32px;
       border: 1px solid #30363d; border-radius: 6px; }
img { max-width: 100%; vertical-align: middle; }
img[width]:not([height]) { height: auto; }
h1, h2 { line-height: 1.25; padding-bottom: .3em; border-bottom: 1px solid #30363d; }
h1 { font-size: 2em; } h2 { font-size: 1.5em; margin-top: 24px; }
p { margin: 16px 0; } a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }
pre { background: #161b22; padding: 16px; overflow: auto; border-radius: 6px; }
code { font: 13px/1.45 ui-monospace, monospace; }
@media (max-width: 600px) { main { margin: 0; padding: 16px; border: 0; } }
@media (prefers-color-scheme: light) {
  body { background: #fff; color: #1f2328; } a { color: #0969da; }
  main, h1, h2 { border-color: #d1d9e0; } pre { background: #f6f8fa; }
}
"""


class PreviewHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path != "/":
            return super().do_GET()
        content = markdown.markdown((ROOT / "README.md").read_text(), extensions=["fenced_code"])
        page = ("<!doctype html><html lang='en'><meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                "<title>GnuJason | Bunker 07</title>"
                f"<style>{STYLE}</style><body><main>{content}</main></body></html>")
        payload = page.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), PreviewHandler)
    print(f"Profile preview: http://localhost:{args.port}", flush=True)
    server.serve_forever()