import os
import requests
BASE = os.environ.get("VIS_SERVER", "http://127.0.0.1:5000").rstrip("/")

class ServerNedostupen(Exception):
    pass

def _zapros(method, path, **kwargs):
    try:
        r = requests.request(method, BASE + path, timeout=3, **kwargs)
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise ServerNedostupen(str(exc)) from exc
    if r.status_code >= 500:
        raise ServerNedostupen(f"HTTP {r.status_code}: {r.text}")
    return r

def vse():
    r = _zapros("GET", "/anketi")
    r.raise_for_status()
    return r.json()

def odna(nomer):
    r = _zapros("GET", f"/anketi/{nomer}")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

def proverit(mail):
    r = _zapros("POST", "/proverka", json={"mail": mail})
    if r.status_code not in (200,400):
        r.raise_for_status()
    return bool(r.json()["prinyato"])

def statistika():
    r = _zapros("GET", "/statistika")
    r.raise_for_status()
    return r.json()
