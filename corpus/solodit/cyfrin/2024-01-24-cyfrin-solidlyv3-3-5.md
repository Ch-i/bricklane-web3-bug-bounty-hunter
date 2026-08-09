---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Optimize away two memory variables in `RewardsDistributor::generateLeaves`
vuln_class: []
---

# Optimize away two memory variables in `RewardsDistributor::generateLeaves`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Optimize away two memory variables in `RewardsDistributor::generateLeaves` by using a named return variable and removing the temporary `leaf` variable:

```solidity
function _generateLeaves(
    address[] calldata earners,
    EarnedRewardType[] calldata types,
    address[] calldata pools,
    address[] calldata tokens,
    uint256[] calldata amounts
) private pure returns (bytes32[] memory leaves) {
    uint256 numLeaves = earners.length;
    // @audit using named return variable
    leaves            = new bytes32[](numLeaves);

    // @audit using cached array length in loop
    for (uint256 i; i < numLeaves; ) {
        // @audit assign straight to return variable
        leaves[i] = keccak256(
            bytes.concat(
                keccak256(
                    abi.encode(
                        earners[i],
                        types[i],
                        pools[i],
                        tokens[i],
                        amounts[i]
                    )
                )
            )
        );
        unchecked {
            ++i;
        }
    }
    return leaves;
}
```

**Solidly:**
Acknowledged.

\clearpage
