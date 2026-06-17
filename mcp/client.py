"""
Lab 4 - MCP client (provided complete).

Gets a token from the auth server for each registered client, then tries all
three tools against the secure MCP server. Watch how scope controls access:
full-client succeeds on everything; limited-client is denied multiply/divide.
"""
import json
import urllib.request

AUTH = "http://127.0.0.1:9000"
MCP = "http://127.0.0.1:8000/mcp"


def _post(url, data, headers=None, form=False):
    if form:
        body = data.encode()
        hdr = {"Content-Type": "application/x-www-form-urlencoded"}
    else:
        body = json.dumps(data).encode()
        hdr = {"Content-Type": "application/json"}
    hdr.update(headers or {})
    req = urllib.request.Request(url, body, hdr)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def get_token(user, pw):
    _, resp = _post(f"{AUTH}/token", f"username={user}&password={pw}", form=True)
    return resp.get("access_token")


def call_tool(token, name, a, b):
    hdr = {"Authorization": f"Bearer {token}"}
    body = {"jsonrpc": "2.0", "id": name, "method": "tools/call",
            "params": {"name": name, "arguments": {"a": a, "b": b}}}
    return _post(MCP, body, hdr)


def run_as(user, pw):
    print(f"\n=== Running as {user} ===")
    token = get_token(user, pw)
    for name in ("add", "multiply", "divide"):
        code, resp = call_tool(token, name, 6, 3)
        if code == 200:
            print(f"  {name}(6,3) -> {resp['result']}  [OK]")
        else:
            print(f"  {name}(6,3) -> DENIED ({code}): {resp['error']}")


if __name__ == "__main__":
    # Unauthenticated request is rejected:
    code, resp = _post(MCP, {"jsonrpc": "2.0", "id": "x",
                             "method": "tools/list", "params": []})
    print(f"No-auth tools/list -> {code}: {resp.get('error')}")

    run_as("full-client", "fullpass")
    run_as("limited-client", "limitedpass")
