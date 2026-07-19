---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Inline small `private` functions only called once
vuln_class: []
---

# Inline small `private` functions only called once

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `StandardToken::_updateName`  and `_updateSymbol` are very small `private` functions that are only ever called once by `updateNameAndSymbol`.

Hence it is more gas efficient to inline them; here is an implementation that also caches the identical storage reads so `name` and `symbol` are only read once from storage:
```solidity
function updateNameAndSymbol(string calldata _name, string calldata _symbol) external onlyMaster {
    require(!CommonUtils.isEmptyString(_name), "Name cannot be empty");
    require(!CommonUtils.isEmptyString(_symbol), "Symbol cannot be empty");

    string memory nameCache = name;
    if (!CommonUtils.isEqualString(_name, nameCache)) {
        emit NameUpdated(nameCache, _name);
        name = _name;
    }

    string memory symbolCache = symbol;
    if (!CommonUtils.isEqualString(_symbol, symbolCache)) {
        emit SymbolUpdated(symbolCache, _symbol);
        symbol = _symbol;
    }
}
```

**Securitize:** Acknowledged.
