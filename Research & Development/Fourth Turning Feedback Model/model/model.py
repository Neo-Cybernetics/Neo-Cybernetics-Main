import numpy as np
def sim(tau, k, years=600, dt=0.05, sigma=0.0, x0=0.5, seed=1):
    rng=np.random.default_rng(seed)
    n=int(years/dt); d=int(round(tau/dt))
    x=np.zeros(n); x[:d+1]=x0
    for i in range(d, n-1):
        x[i+1]=x[i]+dt*(-k*np.tanh(x[i-d]))+sigma*np.sqrt(dt)*rng.standard_normal()
    t=np.arange(n)*dt
    return t,x
def period(t,x,skip=0.5):
    m=t>t[-1]*skip; tt=t[m]; xx=x[m]
    up=np.where((xx[:-1]<0)&(xx[1:]>=0))[0]
    if len(up)<2: return np.nan
    return np.mean(np.diff(tt[up]))
if __name__=="__main__":
    for g in [1.0,1.4,1.6,1.8,2.0,2.5]:
        t,x=sim(21,g/21,years=1500)
        print(g, round(period(t,x),1), round(np.abs(x[-4000:]).max(),2))
