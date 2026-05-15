---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-11
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Overriding fees can't be switched back once set
vuln_class: []
---

# Overriding fees can't be switched back once set

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** A fee is charged when buying a PropertyToken via the TokenBank. The system allows for charging a personalized fee on a per-token basis or a baseFee for all tokens.
If the variable `overrideFees` is set as true, the TokenBank will charge the baseFee that is charged to all tokens instead of charging the configured per-token fee.

The problem is that once the `overrideFees` variable is set to true, it is not possible to set it back to false to allow charging fees on a per-token basis.

```solidity
    function setBaseFee(
        bool updateFee,
        bool overrideFee,
        uint32 newFee
    ) external restricted {
        ...
//@audit => enters only when it is true.
//@audit => So, once set to true, it can't be changed back to false
        if (overrideFee) {
            overrideFees = overrideFee;
            emit FeeOverride(overrideFee);
        }
    }

```

**Impact:** Not possible to charge fees on a per-token basis once it has been configured to charge the baseFee.

**Recommended Mitigation:** Directly update `overrideFees` with the value of the parameter `overrideFee`.
```diff
    function setBaseFee(
        bool updateFee,
        bool overrideFee,
        uint32 newFee
    ) external restricted {
        ...
-       if (overrideFee) {
            overrideFees = overrideFee;
            emit FeeOverride(overrideFee);
-       }
    }
```

**Remora:** Fixed in commit [c38787f](https://github.com/remora-projects/remora-smart-contracts/commit/c38787f4cfd8272868bc939e73ee3d3d50889740).

**Cyfrin:** Verified.
