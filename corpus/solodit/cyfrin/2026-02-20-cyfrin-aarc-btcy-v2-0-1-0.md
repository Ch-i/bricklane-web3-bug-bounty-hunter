---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Use Foundry's encrypted secure private key storage instead of plaintext environment
  variables
vuln_class: []
---

# Use Foundry's encrypted secure private key storage instead of plaintext environment variables

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** The deployment scripts expect private keys to be available plaintext in environment variables. Instead consider [using](https://updraft.aarc-xyz.io/courses/foundry/foundry-simple-storage/never-use-a-env-file) Foundry's encrypted secure private key storage.

**Aarc:** Fixed in commit [cc91182](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/cc91182f7146a1b49262851f7df67904bd859b33).

**Cyfrin:** Verified.
