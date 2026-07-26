---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Logic of `FiveFiftyRule::checkCanTransfer` and `FiveFiftyRule::canTransfer`
  can subtle differ
vuln_class: []
---

# Logic of `FiveFiftyRule::checkCanTransfer` and `FiveFiftyRule::canTransfer` can subtle differ

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** There are subtle differences in the `checkCanTransfer` and `canTransfer` functions on the `FiveFiftyRule` contract that could make the result of the execution on both of them differ.
The most notable difference is shown on the snippet below:
1. On `canTransfer`, it considers the `gid` on the conditional
2. On `checkCanTransfer`, it doesn't consider the `gid` on the conditional

```solidity
//FiveFiftyRule.sol//
    function canTransfer(address from, address to, uint256 amount) external returns (bool) {
        ...

        // to side changes
        if (to != address(0)) {
            ...
            } else if (gId == 0 && iTo.numCatalyst != 0 &&
                !_updateEntityAllowance(false, to, amount)
            ) revert();

            ...
        }

        ...
    }

function checkCanTransfer(
    address to,
    uint256 amount
) external view returns (bool _output) {
    ...
    } else if (iData.numCatalyst != 0 &&
        !_checkEntityAllowance(to, amount)
    ) return false;

    ...
}

```

**Recommended Mitigation:** Consider making them have the same logic by factoring out common logic into internal functions.

**Remora:** Acknowledged.

**Cyfrin:** Verified.
