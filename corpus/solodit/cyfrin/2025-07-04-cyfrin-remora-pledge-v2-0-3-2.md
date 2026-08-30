---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use constants instead of magic numbers
vuln_class: []
---

# Use constants instead of magic numbers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Use constants instead of magic numbers; 1000000, 1e6 and 10 ** 6 are all identical and should declared in a constant that is imported into the various files.
```solidity
TokenBank.sol
111:        if (newFee > 1000000) revert InvalidValuePassed();
252:        uint64 feeValue = (stablecoinValue * curData.saleFee) / 1e6;

PledgeManager.sol
151:        require(newPenalty <= 1000000);
157:        require(newFee <= 1000000);
180:        uint256 fee = (stablecoinAmount * pledgeFee) / 1e6;
283:            refundAmount -= (refundAmount * earlySellPenalty) / 1e6;

RWAToken/DividendManager.sol
230:        require(newFee <= 1e6);
416:        payoutAmount -= (payoutAmount * fee) / (10 ** 6);

RWAToken/RemoraToken.sol
306:            require(newBurnFee <= 1e6);
398:        if (burnFee != 0) burnPayout -= (burnPayout * burnFee) / 1e6;
```

**Remora:** Fixed in commit [aaaab45](https://github.com/remora-projects/remora-smart-contracts/commit/aaaab4558bd370173de2d6f11697ecfd5f097072).

**Cyfrin:** Verified.
