---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-4-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Branchless optimization
vuln_class: []
---

# Branchless optimization

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

The `sqrt` function in `MathLib` and [related comment](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/libraries/LibMath.sol#L129-L136) should be updated to reflect changes in Solmate's `FixedPointMathLib` which now includes the [branchless optimization](https://github.com/transmissions11/solmate/blob/1b3adf677e7e383cc684b5d5bd441da86bf4bf1c/src/utils/FixedPointMathLib.sol#L220-L225) `z := sub(z, lt(div(x, z), z))`.

**Beanstalk:** Fixed in commit [46b24ac](https://github.com/BeanstalkFarms/Basin/commit/46b24aca0c65793604e3c24a07debfe163c5322a).

**Cyfrin:** Acknowledged.

\clearpage
