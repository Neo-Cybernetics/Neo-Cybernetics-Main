import numpy as np
TAU=21.0
def run(kt, beta, TB=5.0, years=3000, dt=0.02, onset=None):
    k=kt/TAU; n=int(years/dt); d=int(TAU/dt); x=np.zeros(n); B=np.zeros(n); x[:d+1]=0.3
    for i in range(d,n-1):
        on = 1.0 if onset is None or i*dt>onset else 0.0
        # belief in a coming crisis grows when cohesion is low (and falling) and decays otherwise
        B[i+1]=B[i]+dt*(np.maximum(-x[i],0)-B[i])/TB
        x[i+1]=x[i]+dt*(-k*np.tanh(x[i-d]) - on*beta*k*B[i])
    t=np.arange(n)*dt; return t,x
def q(t,x):
    m=t>t[-1]*0.6; t=t[m]; x=x[m]; dx=np.gradient(x,t); up=np.where((x[:-1]<0)&(x[1:]>=0))[0]
    if len(up)<3 or np.abs(x).max()<0.02: return "no sustained cycle / runaway"
    r=[]
    for a,b in zip(up[:-1],up[1:]):
        xs=x[a:b]; ds=dx[a:b]; h=t[1]-t[0]
        r.append([np.sum(c)*h for c in [(xs>=0)&(ds>=0),(xs>=0)&(ds<0),(xs<0)&(ds<0),(xs<0)&(ds>=0)]]+[t[b]-t[a]])
    r=np.mean(r,0); return "P=%.1f H/A/U/C=%.1f/%.1f/%.1f/%.1f min x=%.2f mean x=%.2f"%(r[4],*r[:4],x.min(),x.mean())
for kt in [1.4,1.8]:
    for beta in [0,0.5,1.0,2.0]:
        print("kτ=%.1f beta=%.1f:"%(kt,beta), q(*run(kt,beta)))
