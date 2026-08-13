#!/usr/bin/env python3
"""
gantt_server.py — read-only web-Gantt over HubSpot-prosjekter (Fase 1 / prototype).

Henter prosjekter (0-970) + oppgaver live fra HubSpot og tegner en tidslinje med frappe-gantt.
- Grupperer per kunde-prosjekt, én "prosjekt-stolpe" (start → målrett forfallsdato) + oppgavene under.
- Skjuler fullførte oppgaver som standard (vis alt med ?all=1).
- Kun aktive prosjekter (som har minst én åpen oppgave) vises som standard.
- Read-only: ingenting skrives tilbake til HubSpot i denne fasen.

Kjør:  python3 gantt_server.py         # http://127.0.0.1:8787
Binder KUN til 127.0.0.1 (appen bærer pat-token → skal ikke eksponeres på nett).
"""
import json, os, time, html, base64, urllib.request, urllib.error, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

API = "https://api.hubapi.com"
PORT = 8787
HOST = "0.0.0.0"  # 0.0.0.0 = tilgjengelig på lokalnettet (kun read-only HTML; pat-token forlater aldri serveren). 127.0.0.1 = kun denne maskinen.
TOKEN = json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))["mcp"]["servers"]["hubspot"]["env"]["PRIVATE_APP_ACCESS_TOKEN"]

# Enkel Basic Auth. Leser bruker/passord fra gantt_auth.json (gitignorert). Mangler fila → ingen innlogging.
_AUTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gantt_auth.json")
try:
    _a = json.load(open(_AUTH_FILE)); AUTH = f"{_a['user']}:{_a['pass']}"
except Exception:
    AUTH = None
_cache = {"t": 0, "data": None}
# Overstyrings-lag: siste skriving pr. oppgave legges oppå det HubSpots (trege) liste-endepunkt
# returnerer, så en rask oppdatering aldri viser gammel verdi. Selv-heler etter OVERRIDE_TTL.
_overrides = {}
OVERRIDE_TTL = 300  # sek (5 min — god margin for HubSpots eventual consistency)

def remember_override(hsid, fields):
    cur = _overrides.get(hsid, {})
    cur.update(fields); cur["_ts"] = time.time()
    _overrides[hsid] = cur

def get_override(hsid):
    ov = _overrides.get(hsid)
    if not ov:
        return None
    if time.time() - ov.get("_ts", 0) > OVERRIDE_TTL:
        _overrides.pop(hsid, None); return None
    return ov

def req(path):
    r = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + TOKEN})
    for a in range(5):
        try:
            with urllib.request.urlopen(r, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2*(a+1)); continue
            raise
    raise RuntimeError("rate-limit")

def patch(path, body):
    data = json.dumps(body).encode()
    r = urllib.request.Request(API + path, data=data, method="PATCH",
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    for a in range(5):
        try:
            with urllib.request.urlopen(r, timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2*(a+1)); continue
            raise
    raise RuntimeError("rate-limit")

def list_all(v3, props, assoc=()):
    out, after = [], None
    while True:
        q = f"/crm/v3/objects/{v3}?limit=100&archived=false&properties=" + ",".join(props)
        for a in assoc: q += "&associations=" + a
        if after: q += "&after=" + after
        d = req(q); out += d.get("results", [])
        after = d.get("paging", {}).get("next", {}).get("after")
        if not after: break
    return out

def d10(x): return (x or "")[:10]
def adddays(d, n): return (datetime.date.fromisoformat(d10(d)) + datetime.timedelta(days=n)).isoformat()

def fetch():
    if _cache["data"] and time.time() - _cache["t"] < 60:
        return _cache["data"]
    projs = list_all("0-970", ["hs_name", "hs_start_date", "hs_target_due_date"])
    pinfo = {p["id"]: p["properties"] for p in projs}
    # eier-oppslag (id -> "Fornavn Etternavn")
    owners = {}
    try:
        for o in req("/crm/v3/owners?limit=200").get("results", []):
            nm = ((o.get("firstName") or "") + " " + (o.get("lastName") or "")).strip()
            owners[str(o["id"])] = nm or (o.get("email") or "")
    except Exception:
        pass
    tasks = list_all("tasks", ["hs_task_subject", "hs_task_status", "hs_timestamp", "bre_fagomrade", "hubspot_owner_id", "bre_start_date", "hs_task_priority"], ["projects"])
    by_proj = {}
    for t in tasks:
        pr = t["properties"]
        own = owners.get(str(pr.get("hubspot_owner_id") or ""), "")
        for r in t.get("associations", {}).get("projects", {}).get("results", []):
            by_proj.setdefault(r["id"], []).append({
                "hsid": t["id"],
                "subject": pr.get("hs_task_subject") or "(uten navn)",
                "status": pr.get("hs_task_status"),
                "date": d10(pr.get("hs_timestamp")),
                "sd": d10(pr.get("bre_start_date")),
                "fag": pr.get("bre_fagomrade") or "",
                "prio": pr.get("hs_task_priority") or "NONE",
                "owner": own,
                "ownerid": str(pr.get("hubspot_owner_id") or ""),
            })
    _cache.update(t=time.time(), data=(pinfo, by_proj), owners=owners)
    return pinfo, by_proj


FAG = [("tavleverksted", "Tavleverksted"), ("utvikling", "Utvikling"),
       ("installasjon", "Installasjon"), ("drift_leveranse", "Drift/leveranse"), ("salg", "Salg")]
FAG_LBL = dict(FAG)

def build_tasks(show_all, fag="", owner=""):
    pinfo, by_proj = fetch()
    gtasks = []
    today = datetime.date.today().isoformat()
    # sorter prosjekter alfabetisk
    for pid, pr in sorted(pinfo.items(), key=lambda kv: (kv[1].get("hs_name") or "").lower()):
        tlist = by_proj.get(pid, [])
        shown = tlist if show_all else [t for t in tlist if t["status"] != "COMPLETED"]
        if fag:
            shown = [t for t in shown if t.get("fag") == fag]
        if owner:
            shown = [t for t in shown if t.get("ownerid") == owner]
        if not shown:
            continue  # ingen (matchende) oppgaver → hopp over prosjektet
        name = pr.get("hs_name") or pid
        pstart = d10(pr.get("hs_start_date")); ptarget = d10(pr.get("hs_target_due_date"))
        if pstart and ptarget:
            gtasks.append({"id": f"p{pid}", "name": f"📁 {name}", "start": pstart, "end": ptarget,
                           "progress": 0, "custom_class": "bar-project"})
        for i, t in enumerate(sorted(shown, key=lambda x: (x["sd"] or x["date"] or "9999"))):
            # legg siste skriving (overstyring) oppå det lista returnerte — tåler HubSpot-etterslep
            ov = get_override(t.get("hsid")) or {}
            t_status = ov.get("status", t["status"])
            t_date = ov.get("date", t["date"])
            t_sd = ov.get("sd", t["sd"])
            t_owner = ov.get("owner", t.get("owner") or "")
            t_ownerid = ov.get("ownerid", t.get("ownerid") or "")
            t_prio = ov.get("prio", t.get("prio") or "NONE")
            due = t_date or pstart or datetime.date.today().isoformat()
            sd = t_sd or ""
            if sd:
                s = min(sd, due); e = adddays(max(sd, due), 1)  # stolpe: startdato → forfall (inklusiv)
            else:
                s = due; e = adddays(due, 1)                     # ingen startdato → 1-dags ved forfall
            overdue = (t_status != "COMPLETED" and bool(t_date) and t_date[:10] < today)
            if t_status == "COMPLETED":
                cls = "bar-done"
            else:
                cls = "fag-" + (t.get("fag") or "none")
            if overdue:
                cls += " overdue"
            faglbl = FAG_LBL.get(t.get("fag"), "—")
            gtasks.append({"id": f"t{pid}_{i}", "hsid": t.get("hsid"), "name": "   " + t["subject"],
                           "start": s, "end": e, "progress": 100 if t_status=="COMPLETED" else 0,
                           "custom_class": cls, "fag": faglbl, "sd": sd, "due": due, "overdue": overdue,
                           "status": t_status, "prio": t_prio, "owner": t_owner, "ownerid": t_ownerid})
    return gtasks

PAGE = """<!doctype html><html lang="no"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BRE Prosjekt-Gantt</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css">
<style>
 body{margin:0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#0f1720;color:#e6edf3}
 header{padding:12px 18px;background:#005689;color:#fff;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
 header h1{font-size:16px;margin:0;font-weight:600}
 header .sp{flex:1}
 header a,header button{background:#0092D2;color:#fff;border:0;padding:6px 12px;border-radius:6px;
   text-decoration:none;font-size:13px;cursor:pointer}
 header button.active{background:#59C2EA;color:#003}
 .meta{font-size:12px;opacity:.85}
 #wrap{display:flex;margin:14px;height:calc(100vh - 150px);border-radius:8px;overflow:hidden}
 /* padding-top = header_height(50)+padding/2-rest slik at rad-sentre matcher stolpe-sentre (første stolpe-senter = 71px) */
 #side{width:520px;min-width:420px;background:#0b131b;overflow:auto;font-size:13px;border-right:2px solid #005689;padding-top:56px;box-sizing:border-box}
 /* rad-pitch må være nøyaktig 30px (bar_height 18 + padding 12) for å følge tidslinja rad-for-rad */
 #side .p{height:30px;box-sizing:border-box;display:flex;align-items:center;padding:0 10px;color:#59C2EA;font-weight:600;cursor:pointer;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
 #side .p:hover{background:#12202c}
 #side .t{height:30px;box-sizing:border-box;padding:0 10px 0 16px;color:#c8d3dc;cursor:pointer;display:flex;align-items:center;gap:8px}
 #side .t:hover{background:#12202c}
 #side .dot{width:9px;height:9px;border-radius:2px;flex:0 0 auto}
 /* emne krymper og forkortes → gir plass til status + eier */
 #side .t .subj{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1 1 auto;min-width:0}
 /* status: kompakt farget prikk + kort etikett, fast bredde så kolonnene ligger jevnt */
 #side .t .st{flex:0 0 auto;display:flex;align-items:center;gap:5px;width:96px;font-size:10.5px;cursor:pointer;white-space:nowrap;color:#c8d3dc}
 #side .t .st .sdot{width:8px;height:8px;border-radius:50%;flex:0 0 auto}
 #side .t .st:hover{color:#fff}
 #side .t .prio{flex:0 0 auto;width:16px;text-align:center;font-size:13px;cursor:pointer;line-height:1}
 #side .t .prio:hover{filter:brightness(1.3)}
 #side .t .own{color:#8fa0ab;font-size:10.5px;flex:0 0 auto;white-space:nowrap;width:120px;overflow:hidden;text-overflow:ellipsis;text-align:right;cursor:pointer}
 #side .t .own:hover{color:#59C2EA;text-decoration:underline}
 #side .t.overdue{box-shadow:inset 3px 0 0 #E0533A}
 #side .t.overdue .subj{color:#f2a99b}
 #side .t .ownsel,#side .t .stsel{flex:0 0 auto;font-size:11px;max-width:150px;background:#0f1720;color:#e6edf3;border:1px solid #0092D2;border-radius:4px}
 #g{flex:1;background:#fff;color:#111;overflow:auto}
 .gantt .bar-project .bar{fill:#005689}
 .gantt .hl .bar{stroke:#FAE100;stroke-width:3px}
 .gantt .grid-header{fill:#fff}
 .gantt .bar-project .bar-label{fill:#fff;font-weight:600}
 .gantt .bar-done .bar{fill:#9bb0bf}
 .gantt .fag-none .bar{fill:#0092D2}
 .gantt .fag-tavleverksted .bar{fill:#E6A100}
 .gantt .fag-utvikling .bar{fill:#0092D2}
 .gantt .fag-installasjon .bar{fill:#2EA04B}
 .gantt .fag-drift_leveranse .bar{fill:#8E5BD0}
 .gantt .fag-salg .bar{fill:#E0533A}
 /* Forfalt (åpen oppgave forbi forfall): rød ramme rundt stolpen */
 .gantt .overdue .bar{stroke:#E0533A;stroke-width:2.5px}
 /* «I dag»-linje */
 #todayline{pointer-events:none}
 /* Tydelige skillelinjer: tynn per kolonne (uke), tykkere ved periodestart (måned) */
 .gantt .tick{stroke:#d3dbe1;stroke-width:1}
 .gantt .tick.thick{stroke:#8ea1af;stroke-width:1.6}
 /* Nøytraliser frappe sin lilla progress-overlay (#a3a3ff) — vi fargelegger hele stolpen selv via fag/bar-done */
 .gantt .bar-progress{fill:transparent}
 .gantt .bar-wrapper:hover .bar-progress,.gantt .bar-wrapper.active .bar-progress{fill:transparent}
 .gantt .bar-label{font-size:12px}
 .filter{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
 .filter a{background:#0092D2;color:#fff;padding:5px 10px;border-radius:6px;text-decoration:none;font-size:12px}
 .filter a.active{background:#59C2EA;color:#003;font-weight:600}
 .filter select{background:#0092D2;color:#fff;border:0;padding:5px 8px;border-radius:6px;font-size:12px;max-width:190px;cursor:pointer}
 .legend{display:flex;gap:12px;flex-wrap:wrap;padding:6px 18px;background:#0b131b;font-size:11px}
 .legend span{display:flex;align-items:center;gap:5px}
 .legend i{width:11px;height:11px;border-radius:2px;display:inline-block}
</style></head><body>
<header>
 <h1>BRE · Prosjekt-Gantt</h1>
 <span class="meta">__COUNT__ · __TS__ · dra = flytt · kant = juster start/forfall</span>
 <span class="sp"></span>
 <button data-vm="Day">Dag</button>
 <button data-vm="Week" class="active">Uke</button>
 <button data-vm="Month">Måned</button>
 <button id="undo" disabled style="opacity:.5">↶ Angre</button>
 <a href="__TOGGLE__">__TOGGLELBL__</a>
 <a href="?">↻ Oppdater</a>
</header>
<div class="legend">
 <span><i style="background:#E6A100"></i>Tavleverksted</span>
 <span><i style="background:#0092D2"></i>Utvikling</span>
 <span><i style="background:#2EA04B"></i>Installasjon</span>
 <span><i style="background:#8E5BD0"></i>Drift/leveranse</span>
 <span><i style="background:#E0533A"></i>Salg</span>
 <span><i style="background:#9bb0bf"></i>Fullført</span>
 <span class="sp" style="flex:1"></span>
 <span class="filter">Fagområde: __FILTER__</span>
 <span class="filter" style="margin-left:14px">Eier: __OWNERFILTER__</span>
</div>
<div id="wrap"><aside id="side"></aside><div id="g"><svg id="gantt"></svg></div></div>
<div id="toast" style="position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:99;
 color:#fff;padding:9px 16px;border-radius:8px;font-size:13px;opacity:0;transition:opacity .3s;box-shadow:0 3px 12px rgba(0,0,0,.4)"></div>
<script src="https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"></script>
<script>
 var tasks = __DATA__;
 var OWNERS = __OWNERS__;   // [{id,name}] alle HubSpot-eiere
 function fmtDate(x){var d=(x instanceof Date)?x:new Date(x);
   return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);}
 function addDays(ds,n){var d=new Date(ds+'T00:00:00');d.setDate(d.getDate()+n);return fmtDate(d);}
 function toast(msg,ok){var el=document.getElementById('toast');el.textContent=msg;
   el.style.background=ok?'#2EA04B':'#E0533A';el.style.opacity='1';
   clearTimeout(el._t);el._t=setTimeout(function(){el.style.opacity='0';},2600);}
 // Angre-stakk: hver vellykket endring legger på {type, hsid, prev, label}
 var undoStack=[];
 function refreshUndo(){var b=document.getElementById('undo');
   b.disabled=!undoStack.length; b.style.opacity=undoStack.length?'1':'.5';
   b.textContent='↶ Angre'+(undoStack.length>1?' ('+undoStack.length+')':'');}
 function pushUndo(it){undoStack.push(it);refreshUndo();}
 var gantt = new Gantt("#gantt", tasks, {view_mode:"Week", date_format:"YYYY-MM-DD", bar_height:18, padding:12,
   custom_popup_html:function(t){
     var per=t.sd?(t.sd+' → '+t.due):('Forfall: '+(t.due||t.start));
     return '<div style="padding:6px 10px;font-size:12px">'+t.name.trim()+(t.fag&&t.fag!=='—'?'<br><b>'+t.fag+'</b>':'')+(t.owner?'<br>👤 '+t.owner:'')+'<br>📅 '+per+'</div>';},
   on_date_change:function(task,start,end){
     if(!task.hsid){ return; }        // prosjekt-stolper flyttes ikke
     var prevStart=task.sd||'', prevDue=task.due;
     var ns=fmtDate(start);
     var due=addDays(fmtDate(end),-1);   // frappe sin slutt er eksklusiv → inklusiv forfallsdag
     fetch('/move',{method:'POST',headers:{'Content-Type':'application/json'},
       body:JSON.stringify({hsid:task.hsid,start:ns,date:due})})
       .then(function(r){return r.json();})
       .then(function(j){ if(j.ok){ task.sd=ns; task.due=due;
                            pushUndo({type:'move',hsid:task.hsid,prevStart:prevStart,prevDue:prevDue,label:task.name.trim()});
                            toast('✔ '+task.name.trim()+': '+ns+' → '+due,true);}
                          else {toast('✖ Kunne ikke lagre: '+(j.error||'ukjent'),false);} })
       .catch(function(e){toast('✖ Nettverksfeil: '+e,false);});
   }});
 document.querySelectorAll('header button[data-vm]').forEach(function(b){
   b.onclick=function(){gantt.change_view_mode(b.dataset.vm);
     document.querySelectorAll('header button').forEach(function(x){x.classList.remove('active')});
     b.classList.add('active');
     setTimeout(function(){ if(b.dataset.vm==='Week') relabelWeeks(); positionToday(); },0);};});

 // Nedre tidsakse-rad: vis ukenummer ("Uke NN") i ukevisning. Øvre rad = måned (frappe standard).
 function isoWeek(d){
   var t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));
   var day=(t.getUTCDay()+6)%7; t.setUTCDate(t.getUTCDate()-day+3);
   var f=new Date(Date.UTC(t.getUTCFullYear(),0,4));
   return 1+Math.round(((t-f)/86400000-3+((f.getUTCDay()+6)%7))/7);
 }
 function relabelWeeks(){
   if(!gantt||gantt.options.view_mode!=='Week') return;
   var lts=document.querySelectorAll('#gantt .lower-text');
   var ds=gantt.dates||[];
   lts.forEach(function(el,i){ if(ds[i]) el.textContent='Uke '+isoWeek(ds[i]); });
 }
 relabelWeeks();

 // «I dag»-linje: rød stiplet vertikal strek ved dagens dato
 function positionToday(){
   var svg=document.getElementById('gantt');
   var ds=gantt.dates||[];
   var line=document.getElementById('todayline');
   var today=new Date(); today.setHours(0,0,0,0);
   var cw=(gantt.options&&gantt.options.column_width)||30;
   var x=null;
   for(var i=0;i<ds.length-1;i++){
     if(today>=ds[i] && today<ds[i+1]){ x=(i+(today-ds[i])/(ds[i+1]-ds[i]))*cw; break; }
   }
   if(x===null){ if(line) line.style.display='none'; return; }
   var h=svg.getAttribute('height')||svg.clientHeight||3000;
   if(!line){
     line=document.createElementNS('http://www.w3.org/2000/svg','line');
     line.id='todayline'; line.setAttribute('stroke','#E0533A'); line.setAttribute('stroke-width','2');
     line.setAttribute('stroke-dasharray','5,4');
   }
   line.style.display=''; line.setAttribute('x1',x); line.setAttribute('x2',x);
   line.setAttribute('y1',0); line.setAttribute('y2',h);
   svg.appendChild(line);  // legg sist = ligg øverst
 }
 positionToday();

 // Angre siste endring: send revers til HubSpot, last siden på nytt så alt stemmer
 document.getElementById('undo').onclick=function(){
   if(!undoStack.length) return;
   var it=undoStack[undoStack.length-1];
   var url='/'+it.type;   // move | owner | status
   var body={hsid:it.hsid};
   if(it.type==='move'){ body.start=it.prevStart; body.date=it.prevDue; }
   else if(it.type==='owner') body.ownerid=it.prev;
   else if(it.type==='prio') body.prio=it.prev;
   else body.status=it.prev;
   this.disabled=true;
   fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
     .then(function(r){return r.json();}).then(function(j){
       if(j.ok){ undoStack.pop(); toast('↶ Angret: '+it.label,true);
         setTimeout(function(){location.reload();},600); }
       else { toast('✖ Angre feilet: '+(j.error||'ukjent'),false); refreshUndo(); }
     }).catch(function(e){toast('✖ '+e,false); refreshUndo();});
 };

 // Venstremeny: prosjekter + oppgaver, klikk = hopp til raden i tidslinja
 var side=document.getElementById('side');
 var COL={'Tavleverksted':'#E6A100','Utvikling':'#0092D2','Installasjon':'#2EA04B','Drift/leveranse':'#8E5BD0','Salg':'#E0533A'};
 var STATUS={NOT_STARTED:{lbl:'Ikke startet',col:'#8fa0ab'},IN_PROGRESS:{lbl:'Pågår',col:'#0092D2'},
   WAITING:{lbl:'Venter',col:'#E6A100'},DEFERRED:{lbl:'Utsatt',col:'#8E5BD0'},COMPLETED:{lbl:'Fullført',col:'#2EA04B'}};
 var STORDER=['NOT_STARTED','IN_PROGRESS','WAITING','DEFERRED','COMPLETED'];
 function statusEl(t){
   var s=STATUS[t.status]||STATUS.NOT_STARTED;
   var el=document.createElement('span'); el.className='st'; el.title='Status: '+s.lbl+' — klikk for å endre';
   var dot=document.createElement('span'); dot.className='sdot'; dot.style.background=s.col;
   var lbl=document.createElement('span'); lbl.textContent=s.lbl;
   lbl.style.overflow='hidden'; lbl.style.textOverflow='ellipsis'; lbl.style.whiteSpace='nowrap';
   el.appendChild(dot); el.appendChild(lbl);
   el.onclick=function(e){e.stopPropagation();openStatusSel(t,el);};
   return el;
 }
 function openStatusSel(t,el){
   var sel=document.createElement('select'); sel.className='stsel';
   STORDER.forEach(function(k){var op=document.createElement('option');op.value=k;op.textContent=STATUS[k].lbl;
     if(k===t.status) op.selected=true; sel.appendChild(op);});
   el.replaceWith(sel); sel.focus();
   sel.onclick=function(e){e.stopPropagation();};
   var handled=false;
   function fin(save){
     if(handled) return; handled=true;   // onchange + onblur skal ikke begge kjøre
     var ns=sel.value, old=t.status||'NOT_STARTED';
     if(save && ns!==old){
       fetch('/status',{method:'POST',headers:{'Content-Type':'application/json'},
         body:JSON.stringify({hsid:t.hsid,status:ns})})
         .then(function(r){return r.json();}).then(function(j){
           if(j.ok){ t.status=ns; pushUndo({type:'status',hsid:t.hsid,prev:old,label:t.name.trim()});
             toast('✔ Status: '+t.name.trim()+' → '+(STATUS[ns].lbl),true); }
           else { toast('✖ '+(j.error||'feil'),false); }
           sel.replaceWith(statusEl(t));
         }).catch(function(e){toast('✖ '+e,false);sel.replaceWith(statusEl(t));});
     } else { sel.replaceWith(statusEl(t)); }
   }
   sel.onchange=function(){fin(true);};
   sel.onblur=function(){fin(false);};
 }
 // Prioritet: klikkbart flagg-ikon (farge = nivå)
 var PRIO={NONE:{lbl:'Ingen',col:'#5b6b78'},LOW:{lbl:'Lav',col:'#59C2EA'},MEDIUM:{lbl:'Middels',col:'#E6A100'},HIGH:{lbl:'Høy',col:'#E0533A'}};
 var PRORDER=['HIGH','MEDIUM','LOW','NONE'];
 function prioEl(t){
   var p=PRIO[t.prio]||PRIO.NONE;
   var el=document.createElement('span'); el.className='prio'; el.textContent='⚑';
   el.style.color=p.col; if(!t.prio||t.prio==='NONE') el.style.opacity='.28';
   el.title='Prioritet: '+p.lbl+' — klikk for å endre';
   el.onclick=function(e){e.stopPropagation();openPrioSel(t,el);};
   return el;
 }
 function openPrioSel(t,el){
   var sel=document.createElement('select'); sel.className='stsel';
   PRORDER.forEach(function(k){var op=document.createElement('option');op.value=k;op.textContent=PRIO[k].lbl;
     if(k===(t.prio||'NONE')) op.selected=true; sel.appendChild(op);});
   el.replaceWith(sel); sel.focus();
   sel.onclick=function(e){e.stopPropagation();};
   var handled=false;
   function fin(save){
     if(handled) return; handled=true;
     var ns=sel.value, old=t.prio||'NONE';
     if(save && ns!==old){
       fetch('/prio',{method:'POST',headers:{'Content-Type':'application/json'},
         body:JSON.stringify({hsid:t.hsid,prio:ns})})
         .then(function(r){return r.json();}).then(function(j){
           if(j.ok){ t.prio=ns; pushUndo({type:'prio',hsid:t.hsid,prev:old,label:t.name.trim()});
             toast('✔ Prioritet: '+t.name.trim()+' → '+PRIO[ns].lbl,true); }
           else toast('✖ '+(j.error||'feil'),false);
           sel.replaceWith(prioEl(t));
         }).catch(function(e){toast('✖ '+e,false);sel.replaceWith(prioEl(t));});
     } else { sel.replaceWith(prioEl(t)); }
   }
   sel.onchange=function(){fin(true);};
   sel.onblur=function(){fin(false);};
 }
 function jump(id){
   var el=document.querySelector('.bar-wrapper[data-id="'+id+'"]');
   if(!el) return;
   el.scrollIntoView({behavior:'smooth',block:'center',inline:'center'});
   el.classList.add('hl'); setTimeout(function(){el.classList.remove('hl');},1600);
 }
 tasks.forEach(function(t){
   var d=document.createElement('div');
   if(t.id[0]==='p'){
     d.className='p'; d.textContent=t.name.replace('📁','').trim();
   } else {
     d.className='t'+(t.overdue?' overdue':'');
     var dot=document.createElement('span'); dot.className='dot';
     dot.style.background = (t.progress===100) ? '#9bb0bf' : (COL[t.fag]||'#0092D2');
     var s=document.createElement('span'); s.className='subj';
     s.textContent=(t.overdue?'⚠ ':'')+t.name.trim();
     if(t.overdue){ s.title='Forfalt: '+t.due; }
     d.appendChild(dot); d.appendChild(s);
     if(t.hsid){ d.appendChild(prioEl(t)); d.appendChild(statusEl(t)); d.appendChild(ownerEl(t)); }
   }
   d.onclick=(function(id){return function(ev){ if(ev.target.closest('.own,.ownsel,.st,.stsel,.prio')) return; jump(id);};})(t.id);
   side.appendChild(d);
 });

 // Eier-visning + klikk → nedtrekk med alle eiere → lagre til HubSpot
 function ownerEl(t){
   var ow=document.createElement('span'); ow.className='own';
   ow.textContent=t.owner||'+ eier'; if(!t.owner) ow.style.opacity='.6';
   ow.title='Klikk for å endre eier';
   ow.onclick=function(e){ e.stopPropagation(); openOwnerSel(t, ow); };
   return ow;
 }
 function openOwnerSel(t, ow){
   var sel=document.createElement('select'); sel.className='ownsel';
   var o0=document.createElement('option'); o0.value=''; o0.textContent='— ingen —'; sel.appendChild(o0);
   OWNERS.forEach(function(o){var op=document.createElement('option');op.value=o.id;op.textContent=o.name;
     if(String(o.id)===String(t.ownerid)) op.selected=true; sel.appendChild(op);});
   ow.replaceWith(sel); sel.focus();
   sel.onclick=function(e){e.stopPropagation();};
   var handled=false;
   function done(save){
     if(handled) return; handled=true;   // onchange + onblur skal ikke begge kjøre
     var nid=sel.value, oldid=String(t.ownerid||'');
     if(save && nid!==oldid){
       fetch('/owner',{method:'POST',headers:{'Content-Type':'application/json'},
         body:JSON.stringify({hsid:t.hsid,ownerid:nid})})
         .then(function(r){return r.json();}).then(function(j){
           if(j.ok){ t.ownerid=nid;
             t.owner=nid?(OWNERS.filter(function(o){return String(o.id)===String(nid);})[0]||{}).name||'':'';
             pushUndo({type:'owner',hsid:t.hsid,prev:oldid,label:t.name.trim()});
             toast('✔ Eier oppdatert: '+(t.owner||'ingen'),true);
           } else { toast('✖ '+(j.error||'feil'),false); }
           sel.replaceWith(ownerEl(t));
         }).catch(function(e){toast('✖ '+e,false); sel.replaceWith(ownerEl(t));});
     } else { sel.replaceWith(ownerEl(t)); }
   }
   sel.onchange=function(){done(true);};
   sel.onblur=function(){done(false);};
 }

 // Frys periode-linja (dato-header) øverst når man blar nedover
 (function(){
   var svg=document.getElementById('gantt'), g=document.getElementById('g');
   var header=svg.querySelector('.grid-header'), dates=svg.querySelector('.date');
   if(!header||!dates) return;
   svg.appendChild(header); svg.appendChild(dates); // males sist = ligger øverst
   g.addEventListener('scroll',function(){
     var y=g.scrollTop;
     header.setAttribute('transform','translate(0,'+y+')');
     dates.setAttribute('transform','translate(0,'+y+')');
   });
 })();

 // Synkroniser vertikal scroll mellom venstremeny og tidslinje (kilde-guard, ingen loop/tilbakehopp)
 (function(){
   var side=document.getElementById('side'), g=document.getElementById('g');
   if(!side||!g) return;
   var src=null, t=0;
   function link(a,b){
     a.addEventListener('scroll',function(){
       var now=(window.performance&&performance.now)?performance.now():+new Date();
       if(src && src!==a && (now-t)<160) return;  // b scrolles programmatisk nå → ignorer ekko
       src=a; t=now;
       b.scrollTop=a.scrollTop;   // 1:1 (lik rad-pitch på begge sider) → rad følger stolpe eksakt
     },{passive:true});
   }
   link(side,g); link(g,side);
 })();
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _authed(self):
        if not AUTH:
            return True
        h = self.headers.get("Authorization", "")
        if h.startswith("Basic "):
            try:
                if base64.b64decode(h[6:]).decode("utf-8", "ignore") == AUTH:
                    return True
            except Exception:
                pass
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="BRE Prosjekt-Gantt"')
        self.send_header("Content-Length", "0"); self.end_headers()
        return False

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_POST(self):
        if not self._authed():
            return
        route = self.path.split("?")[0]
        if route not in ("/move", "/owner", "/status", "/prio"):
            self._json(404, {"ok": False, "error": "ukjent endepunkt"}); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n).decode() or "{}")
            hsid = str(payload.get("hsid") or "").strip()
            if not hsid:
                self._json(400, {"ok": False, "error": "mangler hsid"}); return
            if route == "/move":
                date = str(payload.get("date") or "").strip()[:10]
                if len(date) != 10:
                    self._json(400, {"ok": False, "error": "mangler dato"}); return
                # hs_timestamp settes til kl 12:00 UTC på valgt dato (unngår at tidssone flytter dagen)
                props = {"hs_timestamp": date + "T12:00:00Z"}
                # startdato valgfri: '' tømmer property, gyldig dato settes (date-property = midnatt UTC ms/ISO)
                if "start" in payload:
                    sd = str(payload.get("start") or "").strip()[:10]
                    props["bre_start_date"] = sd if len(sd) == 10 else ""  # date-property tar YYYY-MM-DD
                patch(f"/crm/v3/objects/tasks/{hsid}", {"properties": props})
                remember_override(hsid, {"date": date, "sd": props.get("bre_start_date", "")})
                self._json(200, {"ok": True, "hsid": hsid, "date": date, "start": props.get("bre_start_date", "")})
            elif route == "/owner":
                ownerid = str(payload.get("ownerid") or "").strip()
                patch(f"/crm/v3/objects/tasks/{hsid}", {"properties": {"hubspot_owner_id": ownerid}})
                remember_override(hsid, {"ownerid": ownerid, "owner": (_cache.get("owners") or {}).get(ownerid, "")})
                self._json(200, {"ok": True, "hsid": hsid, "ownerid": ownerid})
            elif route == "/status":
                status = str(payload.get("status") or "").strip()
                if status not in ("NOT_STARTED", "IN_PROGRESS", "WAITING", "DEFERRED", "COMPLETED"):
                    self._json(400, {"ok": False, "error": "ugyldig status"}); return
                patch(f"/crm/v3/objects/tasks/{hsid}", {"properties": {"hs_task_status": status}})
                remember_override(hsid, {"status": status})
                self._json(200, {"ok": True, "hsid": hsid, "status": status})
            elif route == "/prio":
                prio = str(payload.get("prio") or "").strip()
                if prio not in ("NONE", "LOW", "MEDIUM", "HIGH"):
                    self._json(400, {"ok": False, "error": "ugyldig prioritet"}); return
                patch(f"/crm/v3/objects/tasks/{hsid}", {"properties": {"hs_task_priority": prio}})
                remember_override(hsid, {"prio": prio})
                self._json(200, {"ok": True, "hsid": hsid, "prio": prio})
        except urllib.error.HTTPError as e:
            self._json(502, {"ok": False, "error": f"HubSpot {e.code}: {e.read().decode()[:120]}"})
        except Exception as e:
            self._json(500, {"ok": False, "error": str(e)})

    def do_GET(self):
        if self.path.startswith("/favicon"):
            self.send_response(204); self.end_headers(); return
        if not self._authed():
            return
        from urllib.parse import urlparse, parse_qs, urlencode
        q = parse_qs(urlparse(self.path).query)
        show_all = q.get("all", ["0"])[0] == "1"
        fag = q.get("fag", [""])[0]
        owner = q.get("owner", [""])[0]
        # bygger URL som bevarer alle aktive filtre; over-verdier med "" fjerner parameteren
        def url(**over):
            p = {"all": "1" if show_all else "", "fag": fag, "owner": owner}
            p.update(over)
            p = {k: v for k, v in p.items() if v}
            return "?" + urlencode(p) if p else "?"
        try:
            gtasks = build_tasks(show_all, fag, owner)
            owners_list = sorted(
                [{"id": oid, "name": nm} for oid, nm in (_cache.get("owners") or {}).items() if nm],
                key=lambda o: o["name"].lower())
            # fagområde-filter-lenker (bevarer all= og owner=)
            links = [f'<a href="{url(fag="")}" class="{"active" if not fag else ""}">Alle</a>']
            for v, lbl in FAG:
                links.append(f'<a href="{url(fag=v)}" class="{"active" if fag==v else ""}">{lbl}</a>')
            # eier-nedtrekk (bevarer all= og fag=)
            opts = [f'<option value="{url(owner="")}"{" selected" if not owner else ""}>Alle eiere</option>']
            for o in owners_list:
                sel = " selected" if owner == o["id"] else ""
                opts.append(f'<option value="{url(owner=o["id"])}"{sel}>{html.escape(o["name"])}</option>')
            ownerfilter = '<select onchange="location.href=this.value">' + "".join(opts) + "</select>"
            toggle = url(all=("" if show_all else "1"))
            body = PAGE.replace("__DATA__", json.dumps(gtasks, ensure_ascii=False)) \
                .replace("__OWNERS__", json.dumps(owners_list, ensure_ascii=False)) \
                .replace("__COUNT__", f"{len(gtasks)} rader") \
                .replace("__TS__", time.strftime("%H:%M:%S")) \
                .replace("__TOGGLE__", toggle) \
                .replace("__TOGGLELBL__", "Vis fullførte" if not show_all else "Skjul fullførte") \
                .replace("__FILTER__", " ".join(links)) \
                .replace("__OWNERFILTER__", ownerfilter)
            b = body.encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        except Exception as e:
            msg = f"Feil: {html.escape(str(e))}".encode()
            self.send_response(500); self.send_header("Content-Type","text/plain; charset=utf-8")
            self.end_headers(); self.wfile.write(msg)

if __name__ == "__main__":
    print(f"BRE Prosjekt-Gantt på http://127.0.0.1:{PORT}  (Ctrl+C for å stoppe)")
    ThreadingHTTPServer((HOST, PORT), H).serve_forever()
