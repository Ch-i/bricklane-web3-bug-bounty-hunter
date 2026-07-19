---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Distributor::rescueERC20` uses string error messages inconsistent with project
  style and ignores `transfer` return value'
vuln_class: []
---

# `Distributor::rescueERC20` uses string error messages inconsistent with project style and ignores `transfer` return value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Every other validation in the project uses custom errors, but `rescueERC20` uses string revert reasons. Also `IERC20(token).transfer(to, amount)` ignores the return value and does not use `SafeERC20`, unlike the rest of the contract.

```solidity
issuance/src/vault/Distributor.sol
147:        require(token != address(0), "TokenRescuer: token is zero address");
148:        require(to != address(0), "TokenRescuer: recipient is zero address");
150:        IERC20(token).transfer(to, amount);
```

**Recommended Mitigation:**
```solidity
require(token != address(0), AddressCantBeZero());
require(to != address(0), AddressCantBeZero());
IERC20(token).safeTransfer(to, amount);
```

Also emit an event for the rescue so it is observable off-chain.

**Syntetika:** Fixed in commit [`4a233ae`](https://github.com/SyntetikaLabs/monorepo/commit/4a233ae401374bb17acae5782b70a97ba4bc21af)

**Cyfrin:** Verified.
