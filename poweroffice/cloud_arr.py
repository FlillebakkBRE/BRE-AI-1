#!/usr/bin/env python3
"""
cloud_arr.py — BRE Cloud (IoT Cloud) bokført inntekt fra PowerOffice Go.
Skriver JSON: {ytdLabel, ytd, priorYearLabel, priorTotal, runRate, byAccount}
Konti: 3610 + 3613 + 3615 (BRE IoT Cloud). Inntekt bokføres kredit => snus til positivt.
Bruk: python3 poweroffice/cloud_arr.py
"""
import os, sys, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poweroffice as po

CLOUD_ACCS = [3610, 3613, 3615]

def rev(frm, to):
    accs = ",".join(str(a) for a in CLOUD_ACCS)
    tx = po.api("GET", f"/AccountTransactions?fromDate={frm}&toDate={to}&accountNos={accs}&PageSize=5000")
    tl = tx if isinstance(tx, list) else tx.get("value", [])
    by = {a: 0.0 for a in CLOUD_ACCS}
    for t in tl:
        a = t.get("AccountNo")
        if a in by:
            by[a] += float(t.get("Amount") or 0)
    # kredit-inntekt: snu fortegn til positivt
    return {a: round(-v) for a, v in by.items()}

def main():
    today = datetime.date.today()
    y = today.year
    ytd_by = rev(f"{y}-01-01", today.isoformat())
    prior_by = rev(f"{y-1}-01-01", f"{y-1}-12-31")
    ytd = sum(ytd_by.values())
    prior = sum(prior_by.values())
    # årstakt: lineær framskrivning på antall dager gått
    doy = (today - datetime.date(y, 1, 1)).days + 1
    run_rate = round(ytd / doy * 365) if doy > 0 else 0
    out = {
        "ytdLabel": f"{y} hittil (01.01–{today.strftime('%d.%m')})",
        "ytd": ytd,
        "priorYearLabel": f"{y-1} helår",
        "priorTotal": prior,
        "runRate": run_rate,
        "byAccount": ytd_by,
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
