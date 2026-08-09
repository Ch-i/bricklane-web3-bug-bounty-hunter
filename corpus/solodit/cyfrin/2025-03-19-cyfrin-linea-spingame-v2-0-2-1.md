---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Native token transfers lack explicit balance check
vuln_class: []
---

# Native token transfers lack explicit balance check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** One possible prize type is native tokens, represented by `tokenAddress = address(0)`. A user who wins native tokens can claim them in [`Spin::_transferPrize`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L347-L352):

```solidity
if (prize.tokenAddress == address(0)) {
    (bool success, ) = _winner.call{value: prize.amount}("");
    if (!success) {
        revert NativeTokenTransferFailed();
    }
} else {
```

For ERC20 prizes ([handled here](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L353-L362)) and ERC721 prizes ([handled here](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L369-L371)), the contract explicitly checks whether it has a sufficient balance or ownership of the token before proceeding with the transfer.

While the current implementation would still revert if the contract lacks the required native token balance, consider adding an explicit balance check for native tokens as it would provide consistency across all prize types and ensure uniform error messages, improving usability and debugging.

**Linea:** Fixed in commit [`7675766`](https://github.com/Consensys/linea-hub/commit/7675766ba45bd87888897ac130a587a45e47e96b)

**Cyfrin:** Verified.
