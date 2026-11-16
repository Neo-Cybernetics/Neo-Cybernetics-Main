"""Experiment 3: robustness of the section 5.3 statistic; Slutsky-Yule nulls; distinguishability with ~7 cycles."""
import os as _os, sys; _here = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, _os.path.join(_here, '..', 'model'))
import numpy as np
from model import sim

DT = 0.05
def smooth(x, n):
    if n <= 1: return x
    return np.convolve(x, np.ones(n)/n, mode="valid")

def gaps(x, win_yrs=10, filt=15, merge=False):
    xs = smooth(x, int(round(win_yrs/DT)))
    t = np.arange(len(xs))*DT
    up = np.where((xs[:-1] < 0) & (xs[1:] >= 0))[0]
    if merge:
        # hysteresis: count an upswing only if it follows a down-crossing below -h after the last upswing
        h = 0.25*np.std(xs); ups = []; armed = True
        for i in range(1, len(xs)):
            if xs[i] < -h: armed = True
            if armed and xs[i-1] < 0 <= xs[i]:
                ups.append(i); armed = False
        up = np.array(ups)
    g = np.diff(t[up])
    return g[g > filt] if filt else g

def stats(g):
    return "n=%4d median=%6.1f P10=%6.1f P90=%6.1f" % (len(g), np.median(g), np.percentile(g, 10), np.percentile(g, 90))

def ou(T, years=20000, sigma=0.06, seed=5):
    rng = np.random.default_rng(seed); n = int(years/DT); x = np.zeros(n)
    for i in range(n-1):
        x[i+1] = x[i] - DT*x[i]/T + sigma*np.sqrt(DT)*rng.standard_normal()
    return x

if __name__ == "__main__":
    t, x = sim(21, 1.4/21, years=20000, sigma=0.06, x0=0.0, seed=5)
    print("== 3a. Essay statistic (kτ=1.4, seed 5) vs smoothing window and gap filter ==")
    for w in [0.05, 2, 5, 10, 20]:
        for f in [0, 5, 15, 25]:
            print("smooth %5.2fy filter >%2dy: %s" % (w, f, stats(gaps(x, w, f))))
        print("smooth %5.2fy hysteresis merge: %s" % (w, stats(gaps(x, w, 0, merge=True))))
    print("\n== 3b. Same statistic on processes with NO delayed loop and NO oscillatory mode ==")
    for T in [10, 20, 40, 80]:
        xo = ou(T)
        print("OU red noise, T=%3dy, 10y smooth, >15 filter: %s" % (T, stats(gaps(xo, 10, 15))))
        print("                         hysteresis merge: %s" % stats(gaps(xo, 10, 0, merge=True)))
    for kt in [0.2, 0.35]:
        t, xx = sim(21, kt/21, years=20000, sigma=0.06, x0=0.0, seed=5)
        print("delayed loop kτ=%.2f (non-oscillatory, <1/e), >15: %s" % (kt, stats(gaps(xx, 10, 15))))
    print("\n== 3c. Spectral peak of the essay's noisy model ==")
    from scipy.signal import welch
    for kt in [1.0, 1.4, 1.55]:
        t, xx = sim(21, kt/21, years=40000, sigma=0.06, x0=0.0, seed=2)
        xx = xx[::20]  # yearly
        f, p = welch(xx, fs=1.0, nperseg=4096)
        i = np.argmax(p[1:])+1; half = p[i]/2
        lo = f[:i][p[:i] < half]; hi = f[i:][p[i:] < half]
        fl = lo[-1] if len(lo) else np.nan; fh = hi[0] if len(hi) else np.nan
        print("kτ=%.2f peak period %.1fy, half-power band %.0f-%.0fy, Q=%.1f" % (kt, 1/f[i], 1/fh, 1/fl, f[i]/(fh-fl)))
    print("\n== 3d. Can ~590 years (7 cycles) tell a noisy limit cycle from a noise-driven damped loop? ==")
    # Compare coefficient of variation of upswing gaps in 590-yr windows.
    def cv_windows(kt, sigma, nwin=400):
        t, xx = sim(21, kt/21, years=590*nwin+300, sigma=sigma, x0=0.0, seed=7)
        xx = xx[int(300/DT):]; L = int(590/DT); cvs = []
        for j in range(nwin):
            g = gaps(xx[j*L:(j+1)*L], 10, 15, merge=True)
            if len(g) >= 3: cvs.append(np.std(g)/np.mean(g))
        return np.array(cvs)
    A = cv_windows(1.4, 0.06); B = cv_windows(1.8, 0.10)
    print("damped+noise  CV: median %.2f IQR %.2f-%.2f" % (np.median(A), *np.percentile(A, [25, 75])))
    print("limit cyc+noise CV: median %.2f IQR %.2f-%.2f" % (np.median(B), *np.percentile(B, [25, 75])))
    best = max(((np.mean(A > c) + np.mean(B <= c))/2, c) for c in np.linspace(0, 1, 201))
    print("best single-threshold classification accuracy %.2f at CV=%.2f" % best)
    sh = np.array([1487, 1594, 1704, 1794, 1865, 1946]); g = np.diff(sh)
    print("Strauss-Howe saeculum gaps (High starts):", g, "CV=%.2f" % (g.std()/g.mean()))
    print("  fraction of damped windows with CV >= that: %.2f; of limit-cycle windows: %.2f" % (np.mean(A >= g.std()/g.mean()), np.mean(B >= g.std()/g.mean())))
