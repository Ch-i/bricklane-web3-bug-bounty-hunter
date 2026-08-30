---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Unused constants
vuln_class: []
---

# Unused constants

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** In `Constants.sol` there are a some unused constants, consider removing thses:
* [#L21: `SIGNER_ROLE`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L21)
* [#L38: `VESTING_PERIOD`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L38)
* [#L41 `MAX_COOLDOWN_PERIOD`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L41)
* [#L44: `MIN_COOLDOWN_PERIOD`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L44)
* [#L47 `ETH_SIGNED_MESSAGE_PREFIX`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L47)
* [#L50`REWARD_HASH`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L50)
* [#L56-L59 `DEPOSIT`, `WITHDRAW`, `DEPOSIT_L2`, `WITHDRAW_L2`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/libs/Constants.sol#L56-L59)

**YieldFi:** Fixed in commit [`125ec4a`](https://github.com/YieldFiLabs/contracts/commit/125ec4a944c436e587d7380b8c4bf6232d3264aa)

**Cyfrin:** Verified.
