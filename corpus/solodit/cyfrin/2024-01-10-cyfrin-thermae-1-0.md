---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Checking `bool` return of ERC20 `approve` and `transfer` breaks protocol for
  mainnet USDT and similar tokens which don't return true
vuln_class: []
---

# Checking `bool` return of ERC20 `approve` and `transfer` breaks protocol for mainnet USDT and similar tokens which don't return true

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Checking `bool` return of ERC20 `approve` and `transfer` breaks protocol for mainnet USDT and similar tokens which [don't return true](https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7#code) even though the calls were successful.

**Impact:** Protocol won't work with mainnet USDT and similar tokens.

**Proof of Concept:** Portico.sol L58, 61, 205, 320, 395, 399.

**Recommended Mitigation:** Use [SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) or [SafeTransferLib](https://github.com/transmissions11/solmate/blob/main/src/utils/SafeTransferLib.sol).

**Wormhole:**
Fixed in commits 3f08be9 & 55f93e2.

**Cyfrin:** Verified.
