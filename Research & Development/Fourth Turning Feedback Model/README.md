# Fourth Turning Feedback Model

Code and data for the essay [Can Generations Make History Cycle? A Feedback Model of Strauss-Howe Theory](https://neo-cybernetics.org/articles/fourth-turning-feedback-model) on Neo-Cybernetics.

The essay writes Strauss-Howe generational theory as a balancing feedback loop with a generational delay, tests what that loop does when its assumptions change, and compares the theory's dates with a coding of UK history since 1900. Everything here is meant to be rerun and challenged.

## Contents

| Folder | What it holds |
|---|---|
| `model/` | The delayed-feedback model (`model.py`) and the scripts that draw the essay's model figures |
| `uk-case-study/` | The coding rules (`protocol.md`), the stage coding (`coding.py`), the UK data and the case-study figure |
| `review-experiments/` | The tests from a deliberately hostile review of the model, run with an AI agent, with their recorded outputs (`out_*.txt`) |

## The model

```
dx/dt = −k · tanh( x(t − τ) )
```

`x` is institutional cohesion as a deviation from its long-run average, `τ` the generational delay (21 years in the essay's base case) and `k` the strength of the reaction. It is integrated with Euler steps of 0.05 years.

## Running it

Python 3 with the packages in `requirements.txt`:

```
pip install -r requirements.txt
(cd model && python figs.py)                 # Figures 5, 6 and 8 into model/figures/
(cd model && python fig-spread-delay.py)     # Figure 7, overlapping cohorts
(cd uk-case-study && python fig5.py)         # Figure 9, the UK case study
(cd review-experiments && python exp_uk.py)  # each exp_*.py prints the results in its out_*.txt
```

All the scripts are deterministic (fixed random seeds), and the review experiments reproduce their recorded outputs exactly.

## Data

- `uk_elections.csv`: vote share of the two largest parties and turnout at each UK general election from 1900. The National Government bloc is counted as one party in 1931 and 1935.
- `uk_strikes_ons_bbfw.csv`: working days lost to labour disputes, Office for National Statistics series BBFW, annual from 1891. Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Known limits

The UK stages were coded by one coder who already knew the Strauss-Howe dates. Coding by people who have not seen them is one of the tests the essay asks for, and contributions are welcome. The essay's section 7 lists five predictions that existing data could check.

## Licence

The code is under the repository's MIT Licence. The ONS data stays under the Open Government Licence.
