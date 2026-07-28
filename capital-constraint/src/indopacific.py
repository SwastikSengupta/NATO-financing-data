"""
Extend the financing-constraint measure to the Indo-Pacific.

Same method as the NATO panel: interest payments as a share of government
revenue is the observed debt-service burden, which proxies the cost of raising
new sovereign capital. Applied here to the question of which states face a
binding CAPITAL constraint on infrastructure build-out, as distinct from a
project-pipeline constraint. Those need different instruments.
"""
import json, time, urllib.request
WB="https://api.worldbank.org/v2"; UA={"User-Agent":"indopac-financing/1.0"}
C={"IND":"India","BGD":"Bangladesh","LKA":"Sri Lanka","NPL":"Nepal","PAK":"Pakistan",
   "IDN":"Indonesia","VNM":"Vietnam","PHL":"Philippines","THA":"Thailand",
   "MYS":"Malaysia","KHM":"Cambodia","LAO":"Laos","MMR":"Myanmar","SGP":"Singapore",
   "JPN":"Japan","KOR":"Korea, Rep.","AUS":"Australia","NZL":"New Zealand",
   "PNG":"Papua New Guinea","FJI":"Fiji","MNG":"Mongolia","GBR":"United Kingdom"}
IND={"gdp_usd":"NY.GDP.MKTP.CD","gdp_pc":"NY.GDP.PCAP.CD",
     "int_pct_revenue":"GC.XPN.INTP.RV.ZS","elec_access":"EG.ELC.ACCS.ZS",
     "pop":"SP.POP.TOTL"}
def fetch(ind,years="2018:2025"):
    url=f"{WB}/country/{';'.join(C)}/indicator/{ind}?format=json&date={years}&per_page=2000"
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=60) as r:
                return json.load(r)[1] or []
        except Exception: time.sleep(3)
    return []
def latest(rows):
    b={}
    for r in rows:
        i,v,y=r.get("countryiso3code"),r.get("value"),r.get("date")
        if not i or v is None: continue
        y=int(y)
        if i not in b or y>b[i][1]: b[i]=(float(v),y)
    return b
panel={i:{"country":n,"iso3":i} for i,n in C.items()}
for k,code in IND.items():
    g=latest(fetch(code))
    for i,(v,y) in g.items():
        if i in panel: panel[i][k]=v; panel[i][k+"_year"]=y
    print(f"  {k:16s} coverage {len(g)}/{len(C)}")
    time.sleep(0.4)
for i,p in panel.items():
    if p.get("elec_access") is not None:
        p["elec_gap_pct"]=max(0.0,100.0-p["elec_access"])
        if p.get("pop"): p["people_without_elec_m"]=p["elec_gap_pct"]/100*p["pop"]/1e6
json.dump(panel,open("results/indopacific_panel.json","w"),indent=1)
rows=[p for p in panel.values() if p.get("int_pct_revenue") is not None]
print(f"\nusable: {len(rows)}/{len(C)}")
import statistics as st
med=st.median(r["int_pct_revenue"] for r in rows)
print(f"median interest burden: {med:.2f}% of revenue\n")
print(f"{'country':18s} {'int%rev':>8} {'elec acc%':>10} {'GDPpc $':>10}")
for r in sorted(rows,key=lambda r:-r["int_pct_revenue"]):
    print(f"{r['country']:18s} {r['int_pct_revenue']:8.2f} "
          f"{r.get('elec_access',float('nan')):10.1f} {r.get('gdp_pc',0):10,.0f}")
constrained=[r for r in rows if r["int_pct_revenue"]>med]
print(f"\nabove median (capital-constrained): {len(constrained)}")
json.dump({"median":med,"n":len(rows),
  "constrained":[{k:r.get(k) for k in ("country","int_pct_revenue","elec_access","gdp_pc")} for r in sorted(constrained,key=lambda r:-r["int_pct_revenue"])]},
  open("results/indopacific_findings.json","w"),indent=1)
print("wrote results/indopacific_findings.json")
