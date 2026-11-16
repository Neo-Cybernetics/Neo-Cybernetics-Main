"""Experiments 1-2: distributed delay, asymmetric nonlinearity, instantaneous terms.
All runs: tau (mean delay) = 21 years. Quarter lengths are measured with the essay's labels:
High = x>0 rising, Awakening = x>0 falling, Unraveling = x<0 falling, Crisis = x<0 rising."""
import numpy as np

TAU = 21.0

def quarters(t, x, skip_frac=0.6):
    m = t > t[-1]*skip_frac; t = t[m]; x = x[m]
    dx = np.gradient(x, t)
    up = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    if len(up) < 3:
        return None
    amp = np.abs(x).max()
    # last full cycle stats averaged over cycles
    res = []
    for a, b in zip(up[:-1], up[1:]):
        seg = slice(a, b+1); ts = t[seg]; xs = x[seg]; ds = dx[seg]
        hi = np.sum((xs >= 0) & (ds >= 0)); aw = np.sum((xs >= 0) & (ds < 0))
        un = np.sum((xs < 0) & (ds < 0)); cr = np.sum((xs < 0) & (ds >= 0))
        h = ts[1]-ts[0]
        res.append([hi*h, aw*h, un*h, cr*h, ts[-1]-ts[0]])
    r = np.array(res).mean(0)
    return r, amp

def sim_discrete(k, f=np.tanh, a=0.0, years=3000, dt=0.02, x0=0.3, tau=TAU):
    n = int(years/dt); d = int(round(tau/dt))
    x = np.zeros(n); x[:d+1] = x0
    for i in range(d, n-1):
        x[i+1] = x[i] + dt*(-a*x[i] - k*f(x[i-d]))
    return np.arange(n)*dt, x

def sim_gamma(k, nshape, f=np.tanh, years=4000, dt=0.02, x0=0.3, tau=TAU):
    """Gamma(Erlang) kernel with mean tau via linear chain trick."""
    th = tau/nshape; n = int(years/dt)
    y = np.full(nshape, x0); xv = x0; xs = np.zeros(n)
    for i in range(n):
        xs[i] = xv
        dy = np.empty(nshape); dy[0] = (xv-y[0])/th; dy[1:] = (y[:-1]-y[1:])/th
        dxv = -k*f(y[-1])
        y = y + dt*dy; xv = xv + dt*dxv
    return np.arange(n)*dt, xs

def sim_kernel(k, w, dt, f=np.tanh, years=3000, x0=0.3):
    """General kernel w over lags 0..L (w sums to 1, index j = lag j*dt)."""
    L = len(w); n = int(years/dt)
    x = np.zeros(n+L); x[:L] = x0
    wr = w[::-1]
    for i in range(L, n+L-1):
        u = np.dot(wr, x[i-L+1:i+1])  # x(t - s) weighted
        x[i+1] = x[i] + dt*(-k*f(u))
    return np.arange(n+L)*dt, x

def hopf_gamma(n):
    if n == 1: return np.inf, np.nan
    wt = n*np.tan(np.pi/(2*n))       # omega*tau
    ktau = wt/np.cos(np.pi/(2*n))**n
    return ktau, 2*np.pi/wt          # threshold k*tau, period/tau at threshold

def fmt(r):
    if r is None: return "decays (no sustained cycle)"
    q, amp = r
    if amp < 0.02: return "decays (no sustained cycle)"
    return "P=%.1f  H/A/U/C = %.1f/%.1f/%.1f/%.1f  amp=%.2f" % (q[4], q[0], q[1], q[2], q[3], amp)

if __name__ == "__main__":
    print("== 1a. Gamma (Erlang) kernel, mean 21y: linear Hopf threshold and period ==")
    print("n, sd(yr), kτ_Hopf, P/τ at Hopf")
    for n in [1, 2, 3, 4, 6, 8, 12, 16, 32, 64]:
        kt, pr = hopf_gamma(n)
        print(n, round(TAU/np.sqrt(n), 1), round(kt, 3), round(pr, 3) if np.isfinite(pr) else "-")
    print("\n== 1b. Nonlinear runs with gamma kernel, mean 21 ==")
    for n in [1, 2, 4, 8, 16, 64]:
        for kt in [1.8, 2.5, 4.0, 8.0]:
            t, x = sim_gamma(kt/TAU, n, years=3000, dt=0.05)
            print("n=%2d sd=%4.1f kτ=%.1f : %s" % (n, TAU/np.sqrt(n), kt, fmt(quarters(t, x))))
    print("\n== 1c. Uniform (boxcar) kernel, mean 21 ==")
    dt = 0.1
    for half in [0, 5, 10, 15, 20]:
        lags = np.arange(0, 21+half+dt/2, dt)
        w = ((lags >= 21-half-1e-9) & (lags <= 21+half+1e-9)).astype(float); w /= w.sum()
        for kt in [1.8, 4.0]:
            t, x = sim_kernel(kt/TAU, w, dt, years=2500)
            print("width ±%2d kτ=%.1f : %s" % (half, kt, fmt(quarters(t, x))))
    print("\n== 1d. 'Cohort' kernel: formative age ~ U(17,25), age of influence ~ U(40,70) ==")
    rng = np.random.default_rng(0)
    s = rng.uniform(40, 70, 400000) - rng.uniform(17, 25, 400000)
    print("delay mean %.1f sd %.1f range %.0f-%.0f" % (s.mean(), s.std(), s.min(), s.max()))
    lags = np.arange(0, 55, dt); w, _ = np.histogram(s, bins=np.r_[lags, lags[-1]+dt]); w = w/w.sum()
    for kt in [1.8, 3.0, 6.0]:
        t, x = sim_kernel(kt/s.mean(), w, dt, years=3000)
        print("kτ=%.1f (τ=mean %.1f): %s" % (kt, s.mean(), fmt(quarters(t, x))))
    print("\n== 2. Asymmetric nonlinearity (single delay 21) ==")
    for a in [1.0, 1.5, 2.0, 3.0]:
        f = lambda u, a=a: np.where(u > 0, np.tanh(u), a*np.tanh(u))   # rebuilding a times stronger
        for kt in [1.8, 3.0]:
            t, x = sim_discrete(kt/TAU, f=f)
            print("rebuild x%.1f kτ=%.1f: %s  mean x=%.2f" % (a, kt, fmt(quarters(t, x)), x[len(x)//2:].mean()))
    for c in [0.5, 2.0]:
        f = lambda u, c=c: np.where(u > 0, np.tanh(u), np.tanh(c*u))   # different saturation scale
        t, x = sim_discrete(1.8/TAU, f=f)
        print("asym. slope below 0 x%.1f kτ=1.8: %s" % (c, fmt(quarters(t, x))))
    f = lambda u: np.tanh(u) + 0.3*np.tanh(u)**2 * 0 + 0.2   # constant bias (non-zero set-point)
    t, x = sim_discrete(1.8/TAU, f=lambda u: np.tanh(u-0.2)); print("offset set-point 0.2: ", fmt(quarters(t, x)))
    print("\n== 2b. Add an instantaneous term: dx/dt = -a x(t) - k tanh(x(t-τ)) ==")
    for a in [-0.02, 0.0, 0.01, 0.02, 0.05]:
        t, x = sim_discrete(2.5/TAU, a=a)
        print("a=%+.2f/yr kτ=2.5: %s" % (a, fmt(quarters(t, x))))
