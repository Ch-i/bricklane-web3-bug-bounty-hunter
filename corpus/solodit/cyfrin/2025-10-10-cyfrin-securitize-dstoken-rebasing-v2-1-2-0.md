---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Protocol will leak value to users due to rounding in `RebasingLibrary`
vuln_class: []
---

# Protocol will leak value to users due to rounding in `RebasingLibrary`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Protocols should always round against users in favor of the protocol. `RebasingLibrary` uses "rounding to nearest" method which leaks value to users:
```solidity
// In convertTokensToShares
return (_tokens * DECIMALS_FACTOR + _rebasingMultiplier / 2) / _rebasingMultiplier;
                                 // ^^^^^^^^^^^^^^^^^^^^
                                 // This rounds to nearest

// In convertSharesToTokens
return (_shares * _rebasingMultiplier + DECIMALS_FACTOR / 2) / DECIMALS_FACTOR;
                                     // ^^^^^^^^^^^^^^^^^^^^
                                     // This also rounds to nearest
```

**Impact:** The rounding helps users in both directions:
* When depositing: Users might get 1 extra share
* When withdrawing: Users might get 1 extra token

Over thousands of transactions, these wei-level losses accumulate.

**Proof of Concept:** First [add Foundry integration](https://getfoundry.sh/config/hardhat/#adding-foundry-to-a-hardhat-project). Then add new PoC contract to `test/RebasingRoundingTest.t.sol`:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import "forge-std/Test.sol";
import "../contracts/rebasing/RebasingLibrary.sol";

contract RebasingRoundingTest is Test {
    using RebasingLibrary for *;

    function testRoundingInconsistency() public {
        // Setup: multiplier = 1.5e18 (1.5x rebasing)
        uint256 multiplier = 1.5e18;
        uint8 decimals = 18;

        // Test 1: Convert 1 token to shares and back
        uint256 initialTokens = 1e18;

        // Convert tokens to shares
        uint256 shares = RebasingLibrary.convertTokensToShares(
            initialTokens,
            multiplier,
            decimals
        );

        // Convert shares back to tokens
        uint256 finalTokens = RebasingLibrary.convertSharesToTokens(
            shares,
            multiplier,
            decimals
        );

        console.log("Initial tokens:", initialTokens);
        console.log("Shares received:", shares);
        console.log("Final tokens:", finalTokens);

        // This should fail if there's inconsistency
        assertEq(initialTokens, finalTokens, "Rounding inconsistency detected");
    }

    function testAccumulatedRoundingErrors() public {
        uint256 multiplier = 1.7e18; // Non-round multiplier
        uint8 decimals = 18;

        uint256 totalSharesIssued;
        uint256 totalTokensIn;

        // Simulate 1000 small deposits
        for(uint i = 0; i < 1000; i++) {
            // Each user deposits a small odd amount
            uint256 tokens = 1e15 + i; // 0.001 tokens + i wei

            uint256 shares = RebasingLibrary.convertTokensToShares(
                tokens,
                multiplier,
                decimals
            );

            totalTokensIn += tokens;
            totalSharesIssued += shares;
        }

        // Now convert total shares back to tokens
        uint256 totalTokensOut = RebasingLibrary.convertSharesToTokens(
            totalSharesIssued,
            multiplier,
            decimals
        );

        console.log("Total tokens in:", totalTokensIn);
        console.log("Total tokens out:", totalTokensOut);
        console.log("Difference:", totalTokensOut > totalTokensIn ?
            totalTokensOut - totalTokensIn : totalTokensIn - totalTokensOut);

        // Check if protocol lost tokens
        if(totalTokensOut > totalTokensIn) {
            console.log("Protocol LOST tokens due to rounding!");
        }
    }
}
```

Run with: `forge test --match-contract RebasingRoundingTest -vv`

**Recommended Mitigation:** Rounding should always favor the protocol; normally rounding in favor is rounding down when for example issuing tokens to users but rounding up when users are charged fees etc. But consider:

* `convertTokensToShares` is used during issuance (`TokenLibrary::issueTokensCustom`) where rounding down is in favor of the protocol to give the user slightly less shares
* `convertTokensToShares` is also used during burning (`TokenLibrary::burn`) where rounding down is actually in favor of the user to burn slightly less of their shares

So this is tricky; what newer protocols are doing now:

* in functions such as `convertTokensToShares` that are used throughout the code, they add an [input rounding parameter](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L13-L18)
* all callers to `convertTokensToShares` must specify an explicit rounding direction via the additional input parameter
* all callers to `convertTokensToShares` should have a comment above the call explaining the logic for why the specified rounding direction is correct

This forces developers to carefully consider the rounding direction in the context of every call which is a good practice to follow and can help eliminate rounding bugs.

I'd do the same for `convertSharesToTokens`; make every caller specify the rounding direction and put a comment before every call explaining why the rounding direction is correct in that context.

**Securitize:** Acknowledged; the current implementation doesn't appear exploitable. In practice due to the decimals it very often won't even occur, and trying to fix it creates other potential problems. We'll leave it as is for now but have added some explanatory comments and additional tests in commit [8b74550](https://github.com/securitize-io/dstoken/commit/8b7455093963caefacc8694ee87d0725c83451c6).
