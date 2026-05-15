---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Initializer Can Be Front-Run to Gain Control of the Program
vuln_class: []
---

# Initializer Can Be Front-Run to Gain Control of the Program

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** The `initialize` function from the `xbelo` program, and the `initialize_farm` function from the `clmm_lp_farm` program can be called by anyone after deployment. Considering these functions sets the admins for programs and initializes critical values, malicious executions of these can gave away the control of the program to the caller.

**Recommended Mitigation:** Make sure the deployment and initialization of the program occur in the same transaction, or add the admin address in the `Farm` seeds.

**Doryoku:**
Fixed in [41676f1](https://github.com/Warlands-Nft/xbelo/commit/41676f1ad0572f9b08fcd53c1d0a4a39b4fb9685) and [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.
