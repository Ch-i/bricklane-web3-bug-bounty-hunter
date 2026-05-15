---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-13
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Follow function declaration solidity style guide in `BaseContract`
vuln_class: []
---

# Follow function declaration solidity style guide in `BaseContract`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Functions `pause` and `unpause` defines the visibility `public` after the modifier `onlyOwner`. As per the [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html#function-declaration), the order expects modifiers to be placed after visibility declarations.
```solidity
function pause() onlyOwner external {
        _pause();
    }

    function unpause() onlyOwner external {
        _unpause();
    }
```

**Recommended Mitigation:** Update the code in the following way:
```solidity
function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }
```

**Securitize:** Fixed in commit [61fb6a6](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/61fb6a6e4cb0830d152aa3a436a718fb0e0795ae).

**Cyfrin:** Verified.
