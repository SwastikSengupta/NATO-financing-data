import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":9,"axes.grid":True,"grid.alpha":.3,
                     "figure.dpi":200,"savefig.bbox":"tight"})
RED,BLUE,GREY="#c0392b","#2471a3","#7f8c8d"
p=json.load(open("results/nato_panel.json")); f=json.load(open("results/findings.json"))
rows=[v for v in p.values() if "gap_5.0_usd_bn" in v and v.get("int_pct_revenue") is not None]
de=f["germany_int_pct_rev"]; med=f["median_int"]

# Fig 1 -- the addressable market map
fig,ax=plt.subplots(figsize=(5.4,3.8))
x=[r["int_pct_revenue"] for r in rows]; y=[r["gap_5.0_usd_bn"] for r in rows]
core=[r["int_pct_revenue"]>med and r["gap_5.0_usd_bn"]>0 for r in rows]
ax.scatter([xi for xi,c in zip(x,core) if c],[yi for yi,c in zip(y,core) if c],
           c=RED,s=48,zorder=3,label="core addressable market")
ax.scatter([xi for xi,c in zip(x,core) if not c],[yi for yi,c in zip(y,core) if not c],
           c=BLUE,s=40,zorder=3,label="outside core")
ax.axvline(de,ls="--",c="k",lw=1); ax.axvline(med,ls=":",c=GREY,lw=1)
ax.text(de+0.3,max(y)*0.93,"Germany\n2.48%",fontsize=6.5)
ax.text(med+0.3,max(y)*0.70,"NATO median\n4.21%",fontsize=6.5,color=GREY)
for r in rows:
    if r["gap_5.0_usd_bn"]>25 or r["int_pct_revenue"]>10:
        ax.annotate(r["country"],(r["int_pct_revenue"],r["gap_5.0_usd_bn"]),
                    fontsize=6,xytext=(4,3),textcoords="offset points")
ax.set_xlabel("interest payments (% of government revenue)")
ax.set_ylabel("gap to 5% GDP defence target ($bn)")
ax.set_title("Who needs the bank: financing stress against spending gap",fontsize=9)
ax.legend(fontsize=7)
plt.savefig("figures/fig1_addressable_market.png"); plt.close()

# Fig 2 -- gap by country
fig,ax=plt.subplots(figsize=(4.6,4.4))
s=sorted([r for r in rows if r["gap_5.0_usd_bn"]>0.5],key=lambda r:r["gap_5.0_usd_bn"])
cols=[RED if r["int_pct_revenue"]>med else BLUE for r in s]
ax.barh(range(len(s)),[r["gap_5.0_usd_bn"] for r in s],color=cols,alpha=.85)
ax.set_yticks(range(len(s))); ax.set_yticklabels([r["country"] for r in s],fontsize=6.5)
ax.set_xlabel("gap to 5% GDP target ($bn)")
ax.set_title("red = above-median debt-service burden",fontsize=8)
plt.savefig("figures/fig2_gap_by_country.png"); plt.close()

# Fig 3 -- the 70% verification
fig,ax=plt.subplots(figsize=(4.8,2.8))
v=sorted([r["int_pct_revenue"] for r in rows])
ax.bar(range(len(v)),v,color=[RED if x>de else BLUE for x in v],alpha=.85)
ax.axhline(de,ls="--",c="k",lw=1.2)
ax.text(0.5,de+0.6,f"Germany benchmark {de:.2f}%",fontsize=7)
ax.set_xlabel("NATO members, sorted"); ax.set_ylabel("interest payments (% revenue)")
ax.set_title(f"{f['pct_above_germany']:.1f}% of members exceed the German benchmark",fontsize=9)
plt.savefig("figures/fig3_verification.png"); plt.close()
print("3 figures written")

# Fig 4 -- Indo-Pacific capital-cost dispersion
import json as _j
ip=_j.load(open("results/indopacific_panel.json"))
rows=[v for v in ip.values() if v.get("int_pct_revenue") is not None]
rows.sort(key=lambda r:r["int_pct_revenue"])
fig,ax=plt.subplots(figsize=(5.0,3.6))
names=[r["country"] for r in rows]; vals=[r["int_pct_revenue"] for r in rows]
cols=[RED if v>8.94 else BLUE for v in vals]
ax.barh(range(len(rows)),vals,color=cols,alpha=.85)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(names,fontsize=7)
ax.axvline(8.94,ls=":",c=GREY,lw=1)
for i,r in enumerate(rows):
    if r["country"] in ("India","United Kingdom"):
        ax.annotate("GGI founding partner",(r["int_pct_revenue"],i),fontsize=6,
                    xytext=(6,-2),textcoords="offset points",color="k")
ax.set_xlabel("interest payments (% of government revenue)")
ax.set_title("Indo-Pacific: capital cost spans 0.5% to 80% of revenue",fontsize=9)
plt.savefig("figures/fig4_indopacific.png"); plt.close()
print("fig4 written")
