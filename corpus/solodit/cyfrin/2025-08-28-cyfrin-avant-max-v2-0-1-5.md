---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Enable whitelist in `RequestsManager::constructor`
vuln_class: []
---

# Enable whitelist in `RequestsManager::constructor`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** Currently `RequestsManager::constructor` has the whitelist enablement commented out:
```solidity
  constructor(
    address _issueTokenAddress,
    address _treasuryAddress,
    address _providersWhitelistAddress,
    address[] memory _allowedTokenAddresses
  ) AccessControlDefaultAdminRules(1 days, msg.sender) {
    // *snip : irrelevant stuff* //

    // @audit commented out, starts in permissionless state
    // isWhitelistEnabled = true;
  }
```

It is more defensive to enable the whitelist in the constructor to start in a restricted state, rather than starting in a permissionless state.

**Avant:**
Acknowledged: The whitelisting feature was not on Avant's short-term roadmap, hence the comment. We agree that starting with it adds marginal defense, but since minting and redeeming are two-step request/complete processes that we control, we accepted the tradeoff.
