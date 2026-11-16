import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from model import sim
INK="#1f1f1f"; RED="#b3261e"; GREY="#8a8a8a"; BG="#faf8f3"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10.5,"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False})
tau=21; t,x=sim(tau,1.8/tau,years=900,x0=0.3)
# find an upward zero crossing after 500
i0=np.where((t>500)&(np.r_[False,(x[:-1]<0)&(x[1:]>=0)]))[0][0]; t0=t[i0]
m=(t>=t0-25)&(t<=t0+95); tt=t[m]-t0; xx=x[m]
d=int(tau/0.05); xd=x[np.where(m)[0]-d]
fig,ax=plt.subplots(figsize=(10,5.0))
ax.plot(tt,xd,color=GREY,lw=1.6,ls="--",label="What today's adults grew up with (cohesion 21 years earlier)")
ax.plot(tt,xx,color=RED,lw=2.4,label="Cohesion today")
ax.axhline(0,color=GREY,lw=0.8)
notes=[(0,"Year 0\ncrosses average,\nstill rising"),(21,"Year 21\npeak: the memory\nturns positive"),(42,"Year 42\nfalls through\naverage"),(63,"Year 63\nlow point: the memory\nturns negative"),(84,"Year 84\nback to the start")]
for yr,txt in notes:
    ax.axvline(yr,color=INK,lw=0.6,ls=":")
    ax.text(yr,1.08,txt,ha="center",va="bottom",fontsize=8.5,color=INK)
ax.set_xlim(-5,92); ax.set_ylim(-1.0,1.55); ax.set_xticks([0,21,42,63,84])
ax.set_xlabel("Years"); ax.set_ylabel("Cohesion\n(above or below average)")
ax.legend(frameon=False,fontsize=9,loc="upper center",bbox_to_anchor=(0.5,-0.18),ncol=2)
fig.tight_layout(); import os; os.makedirs("figures",exist_ok=True); fig.savefig("figures/fig-explainer-one-cycle.png",dpi=200)
