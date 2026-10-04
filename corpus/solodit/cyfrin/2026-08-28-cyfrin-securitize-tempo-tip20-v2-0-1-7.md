---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-7
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`loadPk` reads deployer keys from plaintext sources'
vuln_class: []
---

# `loadPk` reads deployer keys from plaintext sources

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** Deployment and operational scripts `deploy-token.ts, register-investor.ts, mint.ts, deploy-full.ts, register-and-mint.ts` use function `loadPk` to load the deployer private key from `DEPLOYER_PK` and, when it is unset, from an unencrypted `.deployer.key` file. Ignoring the file in version control does not protect it from access on a developer workstation, CI runner, backup, or log collection system.

**Impact:** An attacker who obtains the plaintext key through a secondary environment compromise can sign transactions as the deployer and exercise any authority held by that address. This is not a direct on-chain exploit, but compromises deployment and operational trust boundaries.

**Recommended Mitigation:** Remove support for plaintext key files. Use an encrypted keystore or a managed, hardware-backed, or remote signer so the private key is not exposed to the deployment process. Configure CI to use a least-privileged signing integration, rotate any key previously stored in plaintext, and remove residual copies from developer and CI environments.

**Securitize:** **Cyfrin:**


\clearpage
