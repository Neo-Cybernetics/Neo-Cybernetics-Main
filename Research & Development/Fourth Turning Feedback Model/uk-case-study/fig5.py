import csv, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from coding import OURS, SH
INK="#1f1f1f"; RED="#b3261e"; GREY="#8a8a8a"; BG="#faf8f3"
C={"High":"#e8e2d0","Awakening":"#f3d9c9","Unraveling":"#e9c4bd","Crisis":"#cfcfcf","Crisis (partial)":"#dedede","Unclear":"#ffffff"}
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":INK,"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False})
E=list(csv.DictReader(open("uk_elections.csv"))); S=[r for r in csv.DictReader(open("uk_strikes_ons_bbfw.csv")) if r["days_lost_thousands"] and int(r["year"])>=1900]
fig=plt.figure(figsize=(11,7.2)); gs=fig.add_gridspec(4,1,height_ratios=[3,1.6,0.55,0.55],hspace=0.35)
a=fig.add_subplot(gs[0]); b=fig.add_subplot(gs[1],sharex=a); c=fig.add_subplot(gs[2],sharex=a); d=fig.add_subplot(gs[3],sharex=a)
for ax in (a,b):
    for s,e,st,_ in OURS: ax.axvspan(s,e,color=C[st],lw=0)
yrs=[float(r["year"]) for r in E]
a.plot(yrs,[float(r["top_two"]) for r in E],"-o",color=RED,ms=3.5,lw=2,label="Vote share of the two largest parties (%)")
a.plot(yrs,[float(r["turnout"]) for r in E],"-o",color=INK,ms=3,lw=1.3,label="Turnout (%)")
a.set_ylim(50,100); a.legend(frameon=False,loc="upper right",fontsize=9)
a.set_title("United Kingdom, 1900 to 2026: indicators and stages marked by our rules",loc="left",fontsize=12)
b.bar([int(r["year"]) for r in S],[float(r["days_lost_thousands"])/1000 for r in S],color=INK,width=0.9)
b.set_yscale("log"); b.set_ylabel("Strike days lost\n(millions, log)",fontsize=8.5)
b.set_ylim(0.1,250); b.text(2020.5,0.4,"no data\n2020-21",fontsize=6.5,color=GREY,ha="center")
for ax,rows,lab in ((c,[(s,e,st) for s,e,st,_ in OURS],"Our UK coding"),(d,SH,"Strauss-Howe (US dates)")):
    for s,e,st in rows:
        ax.axvspan(s,e,color=C[st],ec="#999",lw=0.6)
        ax.text((s+e)/2,0.5,st.replace(" (partial)","*"),ha="center",va="center",fontsize=8 if e-s>=8 else 6.5)
    ax.set_yticks([]); ax.set_ylabel(lab,rotation=0,ha="right",va="center",fontsize=9); ax.spines["left"].set_visible(False)
d.set_xlim(1900,2026); d.set_xlabel("Year")
for ax in (a,b,c): plt.setp(ax.get_xticklabels(),visible=False)
fig.text(0.01,0.005,"Sources: UK general election results (Wikipedia summary tables); strike days ONS series BBFW (released 20 Oct 2026). *Crisis markers present, rebuilding not yet.",fontsize=7.5,color=GREY)
fig.savefig("fig5-uk-case-study.png",dpi=200,bbox_inches="tight")
