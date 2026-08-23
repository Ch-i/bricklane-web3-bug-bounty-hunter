---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`TokenP::burnStablecoin` breaks accounting'
vuln_class: []
---

# `TokenP::burnStablecoin` breaks accounting

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** Anybody can burn their USDP:
```solidity
    /// @dev This function can typically be called if there is a settlement mechanism to burn stablecoins
    function burnStablecoin(uint256 amount) external {
        _burn(msg.sender, amount);
    }
```
However it's not reflected in Parallel accounting. Associated collateral will be locked in protocol. There are already restricted alternatives that are used by protocol:
```solidity
    function burnSelf(uint256 amount, address burner) external restricted {
        _burn(burner, amount);
    }

    function burnFrom(uint256 amount, address burner, address sender) external restricted {
        if (burner != sender) {
            _spendAllowance(burner, sender, amount);
        }
        _burn(burner, amount);
    }
```

So in current implementation there is no need to have this function.

**Recommended Mitigation:** Remove function `TokenP::burnStablecoin`.

**Parallel:** Acknowledged
