"""Experiment 4: UK coding vs S-H dates, permutation / shift nulls; indicator check."""
import os as _os, sys; _here = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, _os.path.join(_here, '..', 'uk-case-study'))
import csv, numpy as np
from coding import OURS, SH

YEARS = np.arange(1900, 2026)
CYC = ["High", "Awakening", "Unraveling", "Crisis"]
def norm(s): return "Crisis" if s.startswith("Crisis") else s

def yearly(rows):
    lab = {}
    for r in rows:
        s, e, st = r[0], r[1], norm(r[2])
        for y in range(s, e):
            lab[y] = st
    lab.setdefault(2025, lab.get(2024))
    return np.array([lab.get(y, "Unclear") for y in YEARS])

uk = yearly(OURS)
# Extended S-H timeline (US), 1435 onwards, with projected turnings after 2008 at 21y
SHFULL = [(1435,"Unraveling"),(1459,"Crisis"),(1487,"High"),(1517,"Awakening"),(1542,"Unraveling"),(1569,"Crisis"),
 (1594,"High"),(1621,"Awakening"),(1649,"Unraveling"),(1675,"Crisis"),(1704,"High"),(1727,"Awakening"),(1746,"Unraveling"),
 (1773,"Crisis"),(1794,"High"),(1822,"Awakening"),(1844,"Unraveling"),(1860,"Crisis"),(1865,"High"),(1886,"Awakening"),
 (1908,"Unraveling"),(1929,"Crisis"),(1946,"High"),(1964,"Awakening"),(1984,"Unraveling"),(2008,"Crisis"),(2030,"High"),
 (2051,"Awakening"),(2072,"Unraveling"),(2093,"Crisis"),(2114,"High")]
def sh_at(y):
    lab = None
    for s, st in SHFULL:
        if s <= y: lab = st
    return lab

def agree(a, b, mask=None):
    m = np.ones(len(a), bool) if mask is None else mask
    return np.mean(a[m] == b[m])

sh = np.array([sh_at(y) for y in YEARS])
post = YEARS >= 1929; pre = ~post
obs = agree(uk, sh); obs_post = agree(uk, sh, post); obs_pre = agree(uk, sh, pre)
print("Observed year-level agreement 1900-2025: %.3f (post-1929 %.3f, pre-1929 %.3f)" % (obs, obs_post, obs_pre))
print("UK 'Unclear' years: %d of %d" % (np.sum(uk == "Unclear"), len(uk)))

# Null A: shift S-H timeline by s years (s = -40..40)
print("\nNull A: agreement when the S-H timeline is shifted by s years")
res = []
for s in range(-42, 43):
    shs = np.array([sh_at(y - s) for y in YEARS]); res.append((s, agree(uk, shs), agree(uk, shs, post)))
res = np.array(res)
for s in [-30, -20, -15, -10, -7, -5, -3, 0, 3, 5, 7, 10, 15, 20, 30]:
    r = res[res[:, 0] == s][0]; print("  shift %+3d: all %.3f  post-1929 %.3f" % (s, r[1], r[2]))
best = res[np.argmax(res[:, 1])]; print("  best shift (all years): %+d -> %.3f" % (best[0], best[1]))
best2 = res[np.argmax(res[:, 2])]; print("  best shift (post-1929): %+d -> %.3f" % (best2[0], best2[2]))

# Null B: random S-H-like timelines: cyclic H-A-U-C, turning lengths drawn from S-H's own turning lengths, random phase
rng = np.random.default_rng(1)
starts = [s for s, _ in SHFULL[:26]]; lens = np.diff(starts + [2030])[:25]  # empirical turning lengths 1435-2008
def rand_timeline(lenpool):
    st = rng.integers(4); y = 1900 - rng.uniform(0, 30); lab = {}
    while y < 2026:
        L = rng.choice(lenpool);
        for yy in range(int(np.ceil(y)), int(np.ceil(y+L))): lab[yy] = CYC[st]
        y += L; st = (st+1) % 4
    return np.array([lab.get(yy, CYC[st]) for yy in YEARS])
for name, pool in [("S-H empirical turning lengths", lens), ("fixed 21y", np.array([21])), ("uniform 15-28y", np.arange(15, 29))]:
    sims = np.array([[agree(uk, tl := rand_timeline(pool)), agree(uk, tl, post)] for _ in range(20000)])
    print("\nNull B (%s): mean agreement %.3f; P(null >= obs all)=%.4f; P(null >= obs post-1929)=%.4f; 95th pct all %.3f" % (
        name, sims[:, 0].mean(), np.mean(sims[:, 0] >= obs), np.mean(sims[:, 1] >= obs_post), np.percentile(sims[:, 0], 95)))

# Null C: 'shock-following' timeline built only from dated shocks, no generational clock:
# Crisis during total war / national emergency govt; High for 19 years after; Awakening next 10; Unraveling until next shock.
def shock_timeline(shocks):
    lab = {}
    for i, (s, e) in enumerate(shocks):
        nxt = shocks[i+1][0] if i+1 < len(shocks) else 2026
        for y in range(s, e): lab[y] = "Crisis"
        for y in range(e, nxt):
            d = y - e
            lab[y] = "High" if d < 19 else ("Awakening" if d < 29 else "Unraveling")
    return np.array([lab.get(y, "Awakening") for y in YEARS])
shock = shock_timeline([(1914, 1922), (1931, 1946), (2008, 2026)])
print("\nNull C: mechanical shock-following timeline (crisis = war/emergency years; then 19y High, 10y Awakening, Unraveling):")
print("  agreement with UK coding: all %.3f post-1929 %.3f   | agreement with S-H: all %.3f" % (agree(uk, shock), agree(uk, shock, post), agree(sh, shock)))

# Indicators by coded stage
E = list(csv.DictReader(open(_os.path.join(_here, '..', 'uk-case-study', 'uk_elections.csv'))))
S = {int(r['year']): float(r['days_lost_thousands']) for r in csv.DictReader(open(_os.path.join(_here, '..', 'uk-case-study', 'uk_strikes_ons_bbfw.csv'))) if r['days_lost_thousands']}
print("\nIndicators by UK-coded stage (median strike days lost, thousands; two-party share range):")
for st in CYC + ["Unclear"]:
    ys = YEARS[uk == st]
    sd = [S[y] for y in ys if y in S]
    tp = [float(r['top_two']) for r in E if int(float(r['year'])) in set(ys)]
    print("  %-10s n_years=%3d strikes median %7.0f  two-party %s" % (st, len(ys), np.median(sd) if sd else np.nan, (min(tp), max(tp)) if tp else "-"))
print("\nYears with two-party share >= 85 that are NOT coded High:", [r['year'] for r in E if float(r['top_two']) >= 85 and uk[YEARS == int(float(r['year']))][0] != "High"])
