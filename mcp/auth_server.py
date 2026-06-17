"""
Lab 4 - Authorization server (provided complete).

Issues scoped JWT access tokens. Each client is registered with the set of
per-tool scopes it is allowed. Run this first; it listens on :9000.

  POST /token        username=&password=   -> {"access_token": ...}
  POST /introspect   {"token": "..."}       -> decoded claims
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import jwt_util

# Client registry: credentials -> identity + granted per-tool scopes.
CLIENTS = {
    "full-client":    {"password": "fullpass",
                       "scopes": ["tools:add", "tools:multiply", "tools:divide"]},
    "limited-client": {"password": "limitedpass",
                       "scopes": ["tools:add"]},
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n).decode()
        if self.path == "/token":
            form = parse_qs(raw)
            user = form.get("username", [""])[0]
            pw = form.get("password", [""])[0]
            client = CLIENTS.get(user)
            if not client or client["password"] != pw:
                return self._send(401, {"error": "invalid_client"})
            token = jwt_util.encode({"sub": user,
                                     "scope": " ".join(client["scopes"])})
            print(f"[AUTH] issued token for {user} "
                  f"with scopes: {client['scopes']}")
            return self._send(200, {"access_token": token,
                                    "token_type": "bearer"})
        if self.path == "/introspect":
            token = json.loads(raw).get("token", "")
            try:
                return self._send(200, jwt_util.decode(token))
            except ValueError as e:
                return self._send(200, {"active": False, "error": str(e)})
        self._send(404, {"error": "not_found"})


if __name__ == "__main__":
    print("[AUTH] authorization server on http://127.0.0.1:9000")
    ThreadingHTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
