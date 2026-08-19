#!/usr/bin/env python3
"""
heater_scheduler.py — holder kontorovner i riktig modus (komfort/spar).

Regel: komfort man–fre 07:30–16:00, spar ellers + hele helgen.
Poller hvert 5. minutt og setter kun ved avvik (idempotent, selv-helbredende):
mister en ovn settpunktet eller individuell kontroll slås av, rettes det automatisk.
Multi-device: legg nye kontorovner i DEVICES.

Kjøres via launchd (ai.openclaw.homey-heater) — eller nohup:
  nohup python3 homey/heater_scheduler.py > homey/heater_scheduler.log 2>&1 &
Config: homey/config.json (api_key, base_url).
"""
import json, os, time, datetime, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json")))
BASE = CFG["base_url"]; TOK = CFG["api_key"]
LOG = os.path.join(HERE, "heater.log")

# Ovner som styres. Legg til nye kontor her (id fra Homey, egne temp om ønskelig).
DEVICES = [
    {"id": "b7696811-0800-44fe-ae4c-b7d85faa6962", "name": "FL Varmovn (Frode)",  "comfort": 22, "eco": 17},
    {"id": "f48fc127-a512-4ef9-bdf7-ba9966280013", "name": "EO Varmovn (Erlend)", "comfort": 22, "eco": 17},
    {"id": "46772c70-1640-4869-a98f-6b7b80477b8b", "name": "AHB Varmovn (Alf Helge)", "comfort": 22, "eco": 17},
    {"id": "10bf35b7-1af0-4dc1-ae8c-39156b6300ea", "name": "Verksted Ovn", "comfort": 22, "eco": 17},
    {"id": "796d7233-0de5-41cf-8365-5d5033b18bf8", "name": "JTK Varmovn (Jan Tore)", "comfort": 23, "eco": 17},
    {"id": "8bb02ad1-1f3e-4a40-a782-b04529e95926", "name": "Møterom ovn H", "comfort": 22, "eco": 17},
    {"id": "2fafa833-610d-491c-89a9-8dbd85b64640", "name": "Møterom ovn V", "comfort": 22, "eco": 17},
]
POLL = 300  # sekunder

def get_device(dev):
    r = urllib.request.Request(BASE + f"/api/manager/devices/device/{dev}",
                               headers={"Authorization": "Bearer " + TOK})
    with urllib.request.urlopen(r, timeout=20) as x:
        return json.load(x)

def put(dev, cap, val):
    r = urllib.request.Request(BASE + f"/api/manager/devices/device/{dev}/capability/{cap}",
        data=json.dumps({"value": val}).encode(), method="PUT",
        headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=20) as x:
        return x.status

def desired_mode(now):
    # Mandag=0 .. Søndag=6. Komfort kun man–fre 07:30–15:59 (varmt kontor før 08:00).
    after_start = (now.hour > 7) or (now.hour == 7 and now.minute >= 30)
    if now.weekday() < 5 and after_start and now.hour < 16:
        return "comfort"
    return "eco"

def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def main():
    names = ", ".join(d["name"] for d in DEVICES)
    log(f"heater_scheduler startet (komfort man–fre 07:30–16 = 22°C, ellers 17°C) — ovner: {names}")
    last = {}
    while True:
        try:
            now = datetime.datetime.now()
            mode = desired_mode(now)
            for d in DEVICES:
                dev = d["id"]; temp = d["comfort"] if mode == "comfort" else d["eco"]
                try:
                    caps = (get_device(dev).get("capabilitiesObj") or {})
                    cur_t = caps.get("target_temperature", {}).get("value")
                    cur_ic = caps.get("individual_control", {}).get("value")
                    cur_on = caps.get("onoff", {}).get("value")
                    need = (cur_t != temp) or (cur_ic is not True) or (cur_on is not True)
                    if need:
                        if cur_ic is not True: put(dev, "individual_control", True)
                        if cur_on is not True: put(dev, "onoff", True)
                        if cur_t != temp:      put(dev, "target_temperature", temp)
                        log(f"{d['name']}: {mode} satte {temp}°C (var target={cur_t}, ic={cur_ic}, on={cur_on})")
                    elif last.get(dev) != mode:
                        log(f"{d['name']}: allerede {mode} {temp}°C — ok")
                    last[dev] = mode
                except urllib.error.HTTPError as e:
                    log(f"{d['name']}: HTTP-feil {e.code} {e.read().decode()[:100]}")
                except Exception as e:
                    log(f"{d['name']}: Feil {e!r}")
        except Exception as e:
            log(f"Løkke-feil: {e!r}")
        time.sleep(POLL)

if __name__ == "__main__":
    main()
