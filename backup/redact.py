#!/usr/bin/env python3
"""
backup/redact.py — leser en JSON-configfil og skriver en KOPI med alle
hemmeligheter erstattet av "<REDACTED>", trygg å legge i git.
Redakterer verdier hvis nøkkelnavnet ligner en hemmelighet (token, secret,
password, apikey, authorization, key, credential, clientsecret, refresh/access token).
Bruk: python3 redact.py <sti-til-config.json>  (skriver redigert JSON til stdout)
"""
import json, sys, re

SECRET_HINTS = re.compile(
    r"(token|secret|password|passwd|api[_-]?key|apikey|authorization|"
    r"client[_-]?secret|refresh|access[_-]?token|credential|private[_-]?key|bearer)",
    re.IGNORECASE,
)
# nøkler som ligner hemmelig men er ufarlig struktur (ikke rediger disse)
SAFE_KEYS = {"tokenlimit", "maxtokens", "token_budget"}

def redact(obj, parent_key=""):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(v, str) and SECRET_HINTS.search(str(k)) and k.lower() not in SAFE_KEYS and v.strip():
                out[k] = "<REDACTED>"
            else:
                out[k] = redact(v, k)
        return out
    if isinstance(obj, list):
        return [redact(x, parent_key) for x in obj]
    return obj

def main():
    src = sys.argv[1]
    data = json.load(open(src))
    print(json.dumps(redact(data), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
