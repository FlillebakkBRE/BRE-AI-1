#!/usr/bin/env python3
"""Tegner topologi-skissen som PNG (matplotlib). Speiler backup/topologi.svg."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(11.8, 6.5), dpi=130)
ax.set_xlim(0, 1180); ax.set_ylim(650, 0); ax.axis("off")

def box(x, y, w, h, fc, ec, lines, tc, ls="-", bold_first=True):
    ax.add_patch(FancyBboxPatch((x+3, y+3), w-6, h-6,
        boxstyle="round,pad=3,rounding_size=10", fc=fc, ec=ec, lw=2, linestyle=ls))
    cx = x + w/2
    if len(lines) == 1:
        ax.text(cx, y+h/2, lines[0], ha="center", va="center", fontsize=11.5,
                fontweight="bold", color=tc)
    else:
        ax.text(cx, y+h/2-8, lines[0], ha="center", va="center", fontsize=11.5,
                fontweight="bold", color=tc)
        ax.text(cx, y+h/2+9, lines[1], ha="center", va="center", fontsize=9.5, color="#5f6368")

def arrow(x1, y1, x2, y2, color="#5f6368", ls="-", both=False):
    style = "<|-|>" if both else "-|>"
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
        mutation_scale=12, color=color, lw=1.8, linestyle=ls, shrinkA=0, shrinkB=2))

def line(x1, y1, x2, y2, color="#5f6368"):
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.6)

# tittel
ax.text(40, 30, "BRE Digital — AI-assistent (OpenClaw-stack)", fontsize=19, fontweight="bold", color="#202124")
ax.text(40, 54, "Topologi per 5. juli 2026", fontsize=12, color="#5f6368")

# connectors (bak)
arrow(520, 138, 520, 160, both=True)
line(400, 186, 350, 176); line(400, 214, 350, 240)
arrow(250, 274, 197, 330); arrow(256, 274, 475, 330); arrow(262, 274, 753, 330)
ax.text(300, 306, "trigger", fontsize=9, color="#80868b")
for cx in (195, 475, 755):
    arrow(cx, 380, cx, 430); arrow(cx, 478, cx, 528)
arrow(640, 176, 890, 176); arrow(640, 196, 890, 240)
arrow(640, 214, 890, 304, color="#f9a825", ls="--")
arrow(640, 230, 890, 368, color="#9aa0a6", ls="--")

G=("#e6f4ea","#1e8e3e"); T=("#e0f2f1","#00897b"); S=("#f5f5f5","#546e7a"); X=("#e1f5fe","#0277bd")
# noder
box(400,86,240,52,"#e8f0fe","#1a73e8",["Frode  ·  Telegram"],"#174ea6")
box(400,160,240,76,"#ede7f6","#5e35b1",["OpenClaw hovedagent","(Claude Opus)"],"#4527a0")
box(150,150,200,52,"#fff8e1","#f9a825",["Memory","MEMORY.md + notater"],"#8d6e00")
box(150,222,200,52,T[0],T[1],["Cron-planlegger"],"#00695c")
box(890,150,250,52,G[0],G[1],["Brave Search API","web-søk · AKTIV"],"#137333")
box(890,214,250,52,G[0],G[1],["HubSpot MCP","CRM · AKTIV"],"#137333")
box(890,278,250,52,"#fffdf2","#f9a825",["O365 Graph MCP","kalender+kladd · PLANLAGT"],"#8d6e00",ls="--")
box(890,342,250,52,"#f1f3f4","#9aa0a6",["Diakonhjemmet MCP","InfluxDB batteri · PARKERT"],"#80868b",ls="--")
box(70,330,250,50,T[0],T[1],["Morgenbrief","07:00 hverdager"],"#00695c")
box(350,330,250,50,T[0],T[1],["Insider-radar","07:10 hverdager"],"#00695c")
box(630,330,250,50,T[0],T[1],["Ukentlig backup","søndag 03:00"],"#00695c")
box(70,430,250,48,S[0],S[1],["lead-radar/doffin.py"],"#37474f")
box(350,430,250,48,S[0],S[1],["insider-radar/fetch.py"],"#37474f")
box(630,430,250,48,S[0],S[1],["backup/backup.sh"],"#37474f")
box(70,528,250,54,X[0],X[1],["Doffin søke-API","offentlige anbud (IoT)"],"#01579b")
box(350,528,250,54,X[0],X[1],["Oslo Børs Newsweb API","meldepliktig handel"],"#01579b")
box(630,528,250,54,"#fff3e0","#ef6c00",["GitHub (privat) BRE-AI-1","SSH deploy key · off-site"],"#e65100")

# legend
ax.add_patch(FancyBboxPatch((908,432),228,150,boxstyle="round,pad=3,rounding_size=8",fc="#fafafa",ec="#dadce0",lw=1.5))
ax.text(922,452,"Tegnforklaring",fontsize=11,fontweight="bold",color="#202124")
def sw(y,fc,ec,ls,txt):
    ax.add_patch(FancyBboxPatch((922,y),20,13,boxstyle="round,pad=1,rounding_size=3",fc=fc,ec=ec,lw=1.8,linestyle=ls))
    ax.text(950,y+7,txt,fontsize=10.5,va="center",color="#3c4043")
sw(466,"#e6f4ea","#1e8e3e","-","Aktiv")
sw(492,"#fffdf2","#f9a825","--","Planlagt (venter på IT)")
sw(518,"#f1f3f4","#9aa0a6","--","Parkert")
ax.annotate("",xy=(944,552),xytext=(922,552),arrowprops=dict(arrowstyle="-|>",color="#5f6368",lw=2))
ax.text(950,552,"Dataflyt / trigger",fontsize=10.5,va="center",color="#3c4043")

ax.text(40,614,"Flyt: Cron trigger -> agenten kjorer skript -> henter data fra API -> ferdig brief til Frode paa Telegram.",fontsize=10,color="#5f6368")
ax.text(40,631,"Backup: lokal git -> GitHub (kun kode + redigert config + memory, ingen hemmeligheter). Ukentlig auto-push.",fontsize=10,color="#5f6368")

plt.subplots_adjust(left=0,right=1,top=1,bottom=0)
fig.savefig("/Users/breai1/.openclaw/workspace/backup/topologi.png", dpi=130, facecolor="white", bbox_inches="tight", pad_inches=0.15)
print("PNG lagret")
