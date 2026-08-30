---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Cooldown Withdrawals Do Not Support ERC4626 Allowance-Based Owner Flow
vuln_class: []
---

# Cooldown Withdrawals Do Not Support ERC4626 Allowance-Based Owner Flow

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** `ERC-4626` specifies that withdraw and redeem [MUST support](https://eips.ethereum.org/EIPS/eip-4626) a flow where shares are burned from an owner address when `msg.sender` has sufficient ERC-20 allowance over the owner’s shares. In this implementation, the standard `withdraw` and `redeem` functions correctly implement this requirement when `cooldownDuration == 0`. However, when cooldown mode is enabled, these functions are explicitly disabled and users must instead use `cooldownAssets` or `cooldownShares`.

The cooldown withdrawal functions do not provide an owner parameter and always burn shares from `msg.sender`, making allowance-based withdrawals impossible during cooldown mode. As a result, while the contract technically implements the ERC-4626 requirement in normal operation, this behavior is not preserved under cooldown conditions.

**Recommended Mitigation:** Either extend the cooldown withdrawal logic to support an explicit owner parameter with allowance checks, or clearly document that cooldown mode intentionally restricts withdrawals to be initiated only by the share owner.

**Boundary:**
Acknowledged. The owner parameter is omitted to prevent a griefing attack vector.
