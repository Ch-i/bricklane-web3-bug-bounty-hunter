---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Avoid initializing variables to default values
vuln_class: []
---

# Avoid initializing variables to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** There are a number of instances throughout the in-scope contracts where variables are unnecessarily intiialized to default values. For example, consider the following `grep` commands that show the most common scenarios in which this occurs:

```bash
grep -E 'uint.+ *= *0;' -R --include="*.sol" --exclude-dir=lib .
grep -E 'bool.+ *= *false;' -R --include="*.sol" --exclude-dir=lib .
```

**Recommended Mitigation:** Avoid initializing variables to default values to save gas.

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.
