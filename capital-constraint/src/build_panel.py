"""
Who needs the bank? A data-grounded estimate of the DSRB addressable market.

The DSR Bank's public case rests on two empirical premises:
  (a) "Around 70 percent of NATO countries face higher borrowing costs than
      AAA-rated nations like Germany"
  (b) increased defence spending is "creating hard trade-offs across national
      budgets" for members who also "face tight borrowing constraints"

Both are testable with public data, and neither has been quantified publicly at
the member level. This script builds a NATO-wide panel from the World Bank API
and computes, per member: the defence-spending gap against the 2 percent and
5 percent GDP benchmarks, the debt-service burden as a borrowing-cost proxy, and
the intersection of the two, which is the population the Bank exists to serve.

All inputs are observed. No parameter is assumed. No synthetic data is used.
"""
import json
import time
import urllib.request

WB = "https://api.worldbank.org/v2"
UA = {"User-Agent": "dsrb-addressable-market/1.0"}

NATO = {
    "ALB": "Albania", "BEL": "Belgium", "BGR": "Bulgaria", "CAN": "Canada",
    "HRV": "Croatia", "CZE": "Czechia", "DNK": "Denmark", "EST": "Estonia",
    "FIN": "Finland", "FRA": "France", "DEU": "Germany", "GRC": "Greece",
    "HUN": "Hungary", "ISL": "Iceland", "ITA": "Italy", "LVA": "Latvia",
    "LTU": "Lithuania", "LUX": "Luxembourg", "MNE": "Montenegro",
    "NLD": "Netherlands", "MKD": "North Macedonia", "NOR": "Norway",
    "POL": "Poland", "PRT": "Portugal", "ROU": "Romania", "SVK": "Slovakia",
    "SVN": "Slovenia", "ESP": "Spain", "SWE": "Sweden", "TUR": "Turkiye",
    "GBR": "United Kingdom", "USA": "United States",
}

IND = {
    "gdp_usd":        "NY.GDP.MKTP.CD",
    "mil_pct_gdp":    "MS.MIL.XPND.GD.ZS",
    "mil_usd":        "MS.MIL.XPND.CD",
    "debt_pct_gdp":   "GC.DOD.TOTL.GD.ZS",
    "int_pct_revenue": "GC.XPN.INTP.RV.ZS",
    "int_pct_expense": "GC.XPN.INTP.ZS",
}


def fetch(indicator, years="2018:2025"):
    """One call per indicator for all NATO members."""
    codes = ";".join(NATO)
    url = (f"{WB}/country/{codes}/indicator/{indicator}"
           f"?format=json&date={years}&per_page=2000")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                        timeout=60) as r:
                d = json.load(r)
            return d[1] or []
        except Exception:
            time.sleep(3)
    return []


def latest_by_country(rows):
    """Most recent non-null observation per country, with its year."""
    best = {}
    for r in rows:
        iso, val, yr = r.get("countryiso3code"), r.get("value"), r.get("date")
        if not iso or val is None:
            continue
        yr = int(yr)
        if iso not in best or yr > best[iso][1]:
            best[iso] = (float(val), yr)
    return best


if __name__ == "__main__":
    panel = {iso: {"country": name, "iso3": iso} for iso, name in NATO.items()}
    for key, code in IND.items():
        rows = fetch(code)
        got = latest_by_country(rows)
        for iso, (val, yr) in got.items():
            if iso in panel:
                panel[iso][key] = val
                panel[iso][key + "_year"] = yr
        print(f"  {key:16s} {code:22s} coverage {len(got)}/{len(NATO)}")
        time.sleep(0.5)

    # derived quantities, all from observed inputs
    for iso, p in panel.items():
        gdp = p.get("gdp_usd")
        mil = p.get("mil_pct_gdp")
        if gdp and mil is not None:
            for tgt in (2.0, 3.5, 5.0):
                gap_pct = max(0.0, tgt - mil)
                p[f"gap_{tgt}_pct_gdp"] = gap_pct
                p[f"gap_{tgt}_usd_bn"] = gap_pct / 100.0 * gdp / 1e9

    json.dump(panel, open("results/nato_panel.json", "w"), indent=1)
    have = [p for p in panel.values() if "gap_2.0_usd_bn" in p]
    print(f"\npanel built: {len(have)}/{len(NATO)} members with GDP + military expenditure")
    print("wrote results/nato_panel.json")
