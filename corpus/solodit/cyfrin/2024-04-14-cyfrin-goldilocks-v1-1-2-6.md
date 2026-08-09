---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Rounding loss of 1 wei
vuln_class: []
---

# Rounding loss of 1 wei

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** In `Goldivault`, sum of 2 amounts might be less than `amount` due to the rounding loss.

```solidity
File: Goldivault.sol
159:     if(remainingTime > 0) {
160:       SafeTransferLib.safeTransfer(depositToken, msg.sender, amount * (1000 - _fee) / 1000);
161:       SafeTransferLib.safeTransfer(depositToken, multisig, amount * _fee / 1000); //@audit rounding loss
162:       emit OwnershipTokenRedemption(msg.sender, amount * (1000 - _fee) / 1000);
163:     }

File: Goldilend.sol
430:     poolSize += userLoan.interest * (1000 - (multisigShare + apdaoShare)) / 1000;
431:     _updateInterestClaims(interest); //@audit rounding loss
...
694:   function _updateInterestClaims(uint256 interest) internal {
695:     multisigClaims += interest * multisigShare / 1000;
696:     apdaoClaims += interest * apdaoShare / 1000;
697:   }
```

**Client:** Fixed in [PR #17](https://github.com/0xgeeb/goldilocks-core/pull/17)

**Cyfrin:** Verified.
