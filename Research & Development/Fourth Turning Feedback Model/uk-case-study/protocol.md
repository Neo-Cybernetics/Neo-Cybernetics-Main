# UK turnings case study: coding protocol

Written before the stages were marked. The Strauss-Howe dates are compared only after the UK coding is fixed in `coding.py`.

## Indicators

1. **Party-system cohesion:** vote share of the two largest parties at each general election, 1900 to 2024 (Liberal factions combined in 1918 and 1922).
2. **Civic participation:** general election turnout.
3. **Open conflict:** working days lost to strikes, ONS series BBFW, annual from 1891 (uk_strikes_ons_bbfw.csv).
4. **Trust:** British Social Attitudes, share who "almost never" trust governments of any party to put the nation first (23% in 2020, 45% in 2024; earlier years to be added).
5. **Dated events:** wars, emergency powers, coalition or national governments, major new institutions, major value-changing legislation, mass movements.

## Rules for each stage

- **Crisis:** an existential threat or system breakdown (total war, national emergency, emergency powers) together with a coalition or national government, followed by the building of new institutions. Supporting marker added during coding: constitutional upheaval (referendums that change borders or treaties).
- **High:** no emergency; two-party share of 85% or more; low strike activity relative to the decades either side; new institutions being consolidated with cross-party agreement.
- **Awakening:** no emergency; party system still holding (two-party share around 85% or more); rising conflict and organised movements challenging authority and social values; major liberalising legislation.
- **Unraveling:** no emergency; party system fragmenting (two-party share falling below about 80%) or turnout falling; trust falling; open conflict low or subsiding; market or individual choice replacing collective provision.
- **Unclear:** the indicators point in different directions.

## Dated events used (UK)

| Years | Event | Marker |
|---|---|---|
| 1906–14 | Liberal welfare reforms; People's Budget 1909; Parliament Act 1911 | Value challenge, institutions reformed |
| 1910–14 | "Great Unrest": 40.9m strike days in 1912; suffragette campaign; Irish Home Rule crisis | Rising conflict, movements |
| 1914–18 | First World War; coalition from 1915; conscription 1916 | Total war, coalition |
| 1918 | Representation of the People Act | Institution building |
| 1919–21 | 35.0m strike days in 1919; Emergency Powers Act 1920; Irish War of Independence; Irish Free State 1922 | Emergency powers, breakdown |
| 1926 | General Strike; 162m strike days | Emergency |
| 1931 | Financial crisis; National Government; Britain leaves gold standard | Emergency, national government |
| 1939–45 | Second World War; coalition from 1940; Beveridge Report 1942 | Total war, coalition |
| 1945–51 | NHS 1948; nationalisations; welfare state | Institution building, consolidation |
| 1951–64 | Two-party share 93–97%; post-war consensus | High |
| 1964–70 | Abortion Act and Sexual Offences Act 1967; 1968 protests | Liberalising legislation, movements |
| 1972–79 | Miners' strikes 1972 and 1974; three-day week; IMF loan 1976; Winter of Discontent, 29.5m strike days in 1979 | Conflict, emergency powers, fragmentation |
| 1979–90 | Thatcher governments; privatisation; miners' strike 1984–85 then collapse of strike activity | Market replaces collective provision |
| 1997–2007 | Devolution 1998–99; turnout falls to 59% in 2001 | Fragmentation, falling turnout |
| 2008–10 | Financial crash; first coalition government since 1945 | Emergency, coalition |
| 2014–20 | Scottish referendum 2014; Brexit referendum 2016; exit 2020 | Constitutional upheaval |
| 2020–21 | Covid-19 emergency powers | Emergency powers |
| 2024 | Two-party share 57%, lowest in the series; 45% "almost never" trust government | Fragmentation, low trust |

## Revisions

After an independent review (11 Nov 2026): 1922–31 recoded from Crisis to Unclear, because government was single-party after Lloyd George's coalition ended in October 1922. The 2008–26 Crisis is marked partial: the 2010 coalition came from a hung parliament during the fiscal crisis, not a wartime-style emergency.

## Known weakness

The coder (us) already knew the Strauss-Howe dates. A cleaner test would have several people code the stages without seeing them. Readers could be invited to do this.
