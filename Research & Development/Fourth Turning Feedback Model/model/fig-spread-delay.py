# Gamma (Erlang) distributed delay with mean tau: Hopf threshold and period at onset.
# lambda = -k (1 + lambda*tau/n)^(-n); at onset omega*tau = n*tan(pi/2n), k*tau = omega*tau*sec(pi/2n)^n
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK="#1f1f1f"; RED="#b3261e"; GREY="#8a8a8a"; BG="#faf8f3"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10.5,"figure.facecolor":BG,"axes.facecolor":BG,"savefig.facecolor":BG,"axes.spines.top":False,"axes.spines.right":False})
tau=21; ns=np.arange(2,201)
a=np.pi/(2*ns); wt=ns*np.tan(a); kt=wt/np.cos(a)**ns; P=2*np.pi/wt*tau; sd=tau/np.sqrt(ns)
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.4))
a1.plot(sd,kt,color=RED,lw=2.2); a1.axhline(np.pi/2,color=GREY,ls=":",lw=1); a1.axhline(1.8,color=INK,ls="--",lw=1)
a1.text(15.7,1.61,"single sharp delay: kτ = 1.57",fontsize=8.5,color=GREY,ha="right"); a1.text(0.3,1.835,"our main run: kτ = 1.8",fontsize=8.5,color=INK)
a1.set_xlim(0,16); a1.set_ylim(1.4,4.2); a1.set_xlabel("Spread of the delay (standard deviation, years)"); a1.set_ylabel("Reaction strength kτ needed\nfor a self-sustaining cycle")
a1.set_title("Spreading the delay makes cycles harder to sustain",loc="left",fontsize=11)
xc=float(np.interp(1.8,kt[::-1],sd[::-1])); a1.plot([xc],[1.8],"o",color=INK,ms=4,zorder=5)
a1.annotate("main run stops cycling\nabove about 7 years of spread",(xc,1.8),xytext=(0.5,3.3),fontsize=8.5,arrowprops=dict(arrowstyle="-",color=INK,lw=0.8,shrinkA=2,shrinkB=4))
a2.plot(sd,P,color=RED,lw=2.2); a2.axhline(84,color=GREY,ls=":",lw=1); a2.text(0.3,85,"84 years",fontsize=8.5,color=GREY)
a2.set_xlim(0,16); a2.set_ylim(60,90); a2.set_xlabel("Spread of the delay (standard deviation, years)"); a2.set_ylabel("Cycle length at onset (years)")
a2.set_title("…and shortens the cycle",loc="left",fontsize=11)
fig.text(0.01,0.01,"Mean delay fixed at 21 years; delays spread as a gamma distribution (later delays more spread out than earlier ones). Exact linear results.",fontsize=8,color=GREY)
fig.tight_layout(rect=(0,0.04,1,1)); import os; os.makedirs("figures",exist_ok=True); fig.savefig("figures/fig-spread-delay.png",dpi=200)
for n in (2,4,8,16): i=n-2; print(n,round(sd[i],1),round(kt[i],2),round(P[i],1))
