import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
INK="#1f1f1f"; RED="#b3261e"; GREY="#8a8a8a"; BG="#faf8f3"
fig,ax=plt.subplots(figsize=(10,6.2)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0,10); ax.set_ylim(0,6.2); ax.axis("off")
def box(x,y,txt,c=INK):
    ax.add_patch(FancyBboxPatch((x-1.25,y-0.38),2.5,0.76,boxstyle="round,pad=0.04,rounding_size=0.12",fc="white",ec=c,lw=1.4))
    ax.text(x,y,txt,ha="center",va="center",fontsize=9.5,color=INK)
def arr(p,q,sign,c=INK,rad=0.25,lab=None,lp=None):
    a=FancyArrowPatch(p,q,connectionstyle=f"arc3,rad={rad}",arrowstyle="-|>",mutation_scale=14,color=c,lw=1.5)
    ax.add_patch(a)
    mx=(p[0]+q[0])/2; my=(p[1]+q[1])/2
    if lp: mx,my=lp
    ax.text(mx,my,sign,fontsize=12,color=c,ha="center",va="center",fontweight="bold")
    if lab: ax.text(mx,my-0.32,lab,fontsize=8.5,color=c,ha="center",va="center",style="italic")
A=(2.2,4.9); B=(7.8,4.9); C=(7.8,2.4); D=(2.2,2.4)
box(*A,"Institutional cohesion\n(order, trust, conformity)")
box(*B,"Order the young grow up\ntaking for granted")
box(*C,"Appetite for change when that\ngeneration reaches power")
box(*D,"Push to loosen order\n(when negative: rebuild)")
arr((3.5,5.05),(6.5,5.05),"+",rad=-0.15,lp=(5,5.55))
arr((8.0,4.45),(8.0,2.85),"+",rad=-0.25,lab="delay: about one\nlife phase (~20 years)",lp=(9.1,3.75))
arr((6.5,2.25),(3.5,2.25),"+",rad=-0.15,lp=(5,2.75))
arr((2.0,2.85),(2.0,4.45),"−",rad=-0.25,lp=(0.95,3.65))
ax.text(5,3.65,"B",fontsize=22,color=INK,ha="center",va="center",fontweight="bold")
ax.text(5,3.2,"balancing loop\nwith a delay",fontsize=9,color=INK,ha="center",va="center")
# reflexive loop
E=(5.2,0.55)
ax.add_patch(FancyBboxPatch((E[0]-1.6,E[1]-0.32),3.2,0.64,boxstyle="round,pad=0.04,rounding_size=0.12",fc="white",ec=RED,lw=1.4))
ax.text(*E,"Belief that a Crisis is due",ha="center",va="center",fontsize=9.5,color=RED)
arr((5.6,0.9),(3.3,2.0),"+",c=RED,rad=0.3,lp=(5.45,1.25))

arr((1.6,1.98),(3.6,0.45),"+",c=RED,rad=0.35,lp=(1.75,0.9))
ax.text(8.6,0.6,"R: a reinforcing loop.\nThe forecast feeds back\ninto the system it describes",fontsize=8.5,color=RED,ha="center",va="center")
ax.text(0.1,6.0,"The loop Strauss and Howe imply, drawn as a causal loop diagram",fontsize=12,color=INK)
import os; os.makedirs("figures",exist_ok=True); fig.savefig("figures/fig1-causal-loop.png",dpi=200,bbox_inches="tight"); 
