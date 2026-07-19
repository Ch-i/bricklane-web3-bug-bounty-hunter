---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Refactor to avoid two calls to `AddressFilter::addressIsFiltered`
vuln_class: []
---

# Refactor to avoid two calls to `AddressFilter::addressIsFiltered`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** The intention is that the address filter will be enabled and hence every call to `ForcedTransactionGateway::submitForcedTransaction` will make two external calls to `AddressFilter::addressIsFiltered`:
```solidity
    if (useAddressFilter) {
      require(!ADDRESS_FILTER.addressIsFiltered(signer), AddressIsFiltered());
      require(!ADDRESS_FILTER.addressIsFiltered(_forcedTransaction.to), AddressIsFiltered());
    }
```

The most common case will likely be that `signer == _forcedTransaction.to` which also results in duplicate identical storage reads. This can be refactored more efficiently by:

1) Creating a function `AddressFilter::addressesAreFiltered` which takes two inputs:
```solidity
function addressesAreFiltered(address _addr1, address _addr2) external view returns (bool) {
    if (_addr1 == _addr2) {
        return filteredAddresses[_addr1];
    }
    return filteredAddresses[_addr1] || filteredAddresses[_addr2];
}
```

2) Calling this function once in `ForcedTransactionGateway::submitForcedTransaction`:
```solidity
    if (useAddressFilter)
        require(!ADDRESS_FILTER.addressesAreFiltered(signer, _forcedTransaction.to), AddressIsFiltered());
```

This solution results in only 1 external and optimizes away the duplicate identical storage read that would occur in the most common case where `signer == _forcedTransaction.to`.

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-8d8766008f6ce77c606b66562a607209e5227fa45ae395a762f75d474ef17670L161-R161) by only making the second call if `signer != _forcedTransaction.to`.

**Cyfrin:** Verified.

\clearpage
