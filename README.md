# Who Faces the Capital Constraint?

Debt-service burden as a screen for multilateral financing need, applied to
allied defence and to Indo-Pacific grid infrastructure.

**Every input is observed World Bank data. Nothing is assumed, nothing simulated.
Reproduces in under three minutes, no API key.**

## Findings

**The DSRB's headline claim holds.** They state that *"around 70 percent of NATO
countries face higher borrowing costs than AAA-rated nations like Germany."*
Germany sits at **2.48%** of revenue in interest payments; **21 of 30** members
exceed it. **70.0%**, on a proxy the Bank does not cite.

**The gap was created by the Hague target.** $54bn against the old 2% benchmark.
**$1,345bn** against 5%. No member currently meets 5%. Fifteen members carrying
both above-median burden and a shortfall hold **78.6%** of it.

**The Indo-Pacific dispersion is an order of magnitude wider.** Singapore 0.47%,
Sri Lanka 79.9% — roughly **170:1**, against NATO's 8:1.

**The two states that founded the Green Grids Initiative differ by 4x.**
India **34.0%** of revenue to interest; United Kingdom **8.3%**.

**Access is not the binding constraint.** India 99.9% electrified, Bangladesh
99.5%, Malaysia 100%. What binds is capital, not connection. Papua New Guinea is
the exception: 43.3% access *and* 14.2% burden, so both bind.

## Run it

```bash
pip install -r requirements.txt
python src/build_panel.py      # NATO panel
python src/indopacific.py      # Indo-Pacific panel
python src/figures.py          # four figures
```

## Data

World Bank Open Data API, retrieved 27 July 2026, series updated 13 July 2026.
`NY.GDP.MKTP.CD`, `MS.MIL.XPND.GD.ZS` (SIPRI), `GC.XPN.INTP.RV.ZS`,
`EG.ELC.ACCS.ZS`, `SP.POP.TOTL`.

## What this does not claim

The measure is realised debt-service burden, not marginal borrowing cost — it
embeds the existing stock and maturity profile. The US result is most affected by
this and is flagged rather than resolved. The gap is a static identity at current
GDP, not a forecast. Sri Lanka's figure reflects default conditions. Nothing here
evaluates whether either institution would work.

## License

MIT. World Bank data under its own terms.
