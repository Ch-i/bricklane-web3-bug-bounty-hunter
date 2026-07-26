---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Optimize setters by emitting event before state updates
vuln_class: []
---

# Optimize setters by emitting event before state updates

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** Functions `SherpaUSD::setKeeper`, `SherpaUSD::setOperator`, `SherpaUSD::setAutoTransfer` and `SherpaVault::setDepositsEnabled`, `SherpaVault::setStableWrapper` create an unnecessary memory variable to store old values used for event emissions. However, this is not required if the event is emitted first.

For example, function setKeeper can be optimized in the following manner:

```solidity
function setKeeper(address _keeper) external onlyOwner {
    if (_keeper == address(0)) revert AddressMustBeNonZero();
    emit KeeperSet(keeper, _keeper);
    keeper = _keeper;
}
```

**Recommended Mitigation:** Consider removing the memory variables by emitting events first.

**Sherpa:** Fixed in commit [`7e34a6b`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/7e34a6b064b63d8f7a3f2c66c49e10adab0198b7)

**Cyfrin:** Verified.

\clearpage
