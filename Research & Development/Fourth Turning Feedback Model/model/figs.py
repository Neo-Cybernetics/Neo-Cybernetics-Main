import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from model import sim, period
INK="#1f1f1f"; RED="#b3261e"; GREY="#8a8a8a"; BG="#faf8f3"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,
 "xtick.color":INK,"ytick.color":INK,"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,
 "axes.spines.top":False,"axes.spines.right":False})
out="figures/"
import os; os.makedirs(out,exist_ok=True)

# Fig 2: limit cycle with turnings shaded
tau=21; k=1.8/tau
t,x=sim(tau,k,years=900,x0=0.3)
m=(t>500)&(t<500+260); tt=t[m]-500; xx=x[m]
dx=np.gradient(xx,tt)
cols={"High":"#e8e2d0","Awakening":"#f3d9c9","Unraveling":"#e9c4bd","Crisis":"#d9d9d9"}
lab=np.where((xx>=0)&(dx>=0),"High",np.where((xx>=0)&(dx<0),"Awakening",np.where((xx<0)&(dx<0),"Unraveling","Crisis")))
fig,ax=plt.subplots(figsize=(10,4.2))
start=0
for i in range(1,len(tt)+1):
    if i==len(tt) or lab[i]!=lab[start]:
        ax.axvspan(tt[start],tt[i-1],color=cols[lab[start]],lw=0)
        mid=(tt[start]+tt[i-1])/2
        if tt[i-1]-tt[start]>12: ax.text(mid,1.32,lab[start],ha="center",va="bottom",fontsize=8.5,color=INK)
        start=i
ax.plot(tt,xx,color=RED,lw=2.2)
ax.axhline(0,color=GREY,lw=0.8)
ax.set_ylim(-1.5,1.55); ax.set_xlim(0,260)
ax.set_xlabel("Years"); ax.set_ylabel("Institutional cohesion\n(deviation from average)")
ax.set_title("A one-generation delay produces a four-phase cycle of about 84 years",loc="left",fontsize=12)
fig.text(0.01,0.01,"Model: dx/dt = -k·tanh(x(t-τ)), τ = 21 years, kτ = 1.8. Phases named by quadrant (level above or below average, rising or falling).",fontsize=8,color=GREY)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig(out+"fig2-four-turnings-cycle.png",dpi=200); plt.close()

# Fig 3: period vs delay
taus=np.arange(8,32,1.0); P1=[];P2=[]
for tv in taus:
    t,x=sim(tv,1.8/tv,years=60*tv,x0=0.3); P1.append(period(t,x))
    t,x=sim(tv,1.2/tv,years=12*tv,x0=0.5); P2.append(period(t,x,skip=0.0))
fig,ax=plt.subplots(figsize=(8,4.6))
ax.plot(taus,P1,color=RED,lw=2.2,label="Self-sustaining cycle (kτ = 1.8)")
ax.plot(taus,P2,color=INK,lw=1.6,ls="--",label="Damped cycle (kτ = 1.2)")
ax.axhline(50,color=GREY,lw=0.8,ls=":")
ax.text(22.3,52,"50-year cycles in Turchin's and Sterman's models\n(produced by different mechanisms)",fontsize=8.5,color=GREY)
ax.axvline(21,color=GREY,lw=0.8,ls=":"); ax.plot([21],[84],"o",color=RED,ms=6)
ax.annotate("~84 years:\nStrauss-Howe saeculum",(21,84),xytext=(21.8,62),fontsize=8.5,color=INK)
ax.set_xlabel("Delay τ in the loop (years)"); ax.set_ylabel("Cycle length (years)")
ax.set_title("Cycle length is set by the delay, roughly four times over",loc="left",fontsize=12)
ax.legend(frameon=False,fontsize=9,loc="upper left")
fig.tight_layout(); fig.savefig(out+"fig3-period-vs-delay.png",dpi=200); plt.close()
print("P at 12.5?", [ (tv,p) for tv,p in zip(taus,P1) if tv in (12,13,21)], [(tv,p) for tv,p in zip(taus,P2) if tv in (12,13,21)])

# Fig 4: damped + noise, two runs
def smooth(x,n): return np.convolve(x,np.ones(n)/n,mode="same")
fig,axs=plt.subplots(2,1,figsize=(10,4.8),sharex=True)
for ax,seed in zip(axs,[3,11]):
    t,x=sim(21,1.4/21,years=900,sigma=0.06,x0=0.0,seed=seed)
    m=t>300; tt=t[m]-300; xs=smooth(x[m],200); tt,xs=tt[100:-100],xs[100:-100]
    ax.plot(tt,xs,color=INK,lw=1.4); ax.axhline(0,color=GREY,lw=0.8)
    ax.set_ylabel("Cohesion",fontsize=9)
axs[-1].set_xlabel("Years")
axs[0].set_title("A stable loop pushed by random shocks: rough cycles with no fixed timetable",loc="left",fontsize=12)
fig.text(0.01,0.01,"Same model with damping (kτ = 1.4, τ = 21 years) plus small random shocks; 10-year smoothing. Two runs, different random seeds.",fontsize=8,color=GREY)
fig.tight_layout(rect=(0,0.04,1,1)); fig.savefig(out+"fig4-noise-driven-quasi-cycles.png",dpi=200); plt.close()
# stats over a long run
t,x=sim(21,1.4/21,years=20000,sigma=0.06,x0=0.0,seed=5)
xs=smooth(x,200); up=np.where((xs[:-1]<0)&(xs[1:]>=0))[0]; g=np.diff(t[up]); g=g[g>15]
print("n",len(g),"median",np.median(g),"p10",np.percentile(g,10),"p90",np.percentile(g,90))
