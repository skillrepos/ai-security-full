"""
Lab 4 - Secure MCP server (SKELETON)

A minimal JSON-RPC "MCP" server on :8000. Add security middleware:
  1. Require a valid Bearer JWT (else 401)
  2. For tools/call, require the matching tools:<name> scope (else 403)
  3. Only expose a restricted tool manifest

NOTE: incomplete. Merge in the auth + scope logic from
extra/secure_server_complete.txt before running.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import jwt_util

# TODO (merge): restricted tool manifest
TOOLS = {
    "add": lambda a, b: a + b,
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

    def _authenticate(self):
        """Return token claims, or None if the Bearer token is missing/invalid."""
        # TODO (merge): read Authorization header, verify Bearer JWT
        raise NotImplementedError("_authenticate not implemented yet")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n).decode() or "{}")
        rid = req.get("id")

        claims = self._authenticate()
        if claims is None:
            return self._send(401, {"id": rid, "error": "Missing or invalid token"})

        method = req.get("method")
        if method == "tools/list":
            return self._send(200, {"id": rid, "result": list(TOOLS)})

        if method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            scopes = claims.get("scope", "").split()
            # TODO (merge): per-tool scope enforcement -> 403 if missing
            raise NotImplementedError("scope enforcement not implemented yet")

        self._send(400, {"id": rid, "error": "unknown method"})


if __name__ == "__main__":
    print("[SECURE] secure MCP server on http://127.0.0.1:8000")
    print(f"[SECURE] tools exposed: {list(TOOLS)}")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
