---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`ROUSG::unwrap` can unnecessarily return slightly less `OUSG` tokens than
  users originally wrapped'
vuln_class: []
---

# `ROUSG::unwrap` can unnecessarily return slightly less `OUSG` tokens than users originally wrapped

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** One invariant of the `ROUSG` token is:

> when unwrapping users should receive the same amount of OUSG input tokens they provided when they wrapped, irrespective of price

However this can often not be the case as `ROUSG::unwrap` can unnecessarily return slightly less `OUSG` tokens than users originally wrapped.

**Impact:** Users will unnecessarily receive slightly less tokens than they originally wrapped, breaking an invariant of the `ROUSG` contract.

**Proof of Concept:** Run this stand-alone stateless fuzz test which shows the problem:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "forge-std/Test.sol";

// run from base project directory with:
// forge test --match-contract ROUSGWrapUnwrapBrokenInvariantTest -vvv

contract ROUSGWrapUnwrapBrokenInvariantTest is Test {

    uint256 public constant OUSG_TO_ROUSG_SHARES_MULTIPLIER = 10_000;

    function _getROUSGByShares(uint256 _shares, uint256 ousgPrice) internal pure returns (uint256 rOUSGAmount) {
        rOUSGAmount = (_shares * ousgPrice) / (1e18 * OUSG_TO_ROUSG_SHARES_MULTIPLIER);
    }

    function getSharesByROUSG(uint256 _rOUSGAmount, uint256 ousgPrice)
    internal pure returns (uint256 shares) {
        shares = (_rOUSGAmount * 1e18 * OUSG_TO_ROUSG_SHARES_MULTIPLIER) / ousgPrice;
    }

    function _wrap(uint256 _OUSGAmount) internal pure returns (uint256 shares) {
        require(_OUSGAmount > 0, "rOUSG: can't wrap zero OUSG tokens");

        shares = _OUSGAmount * OUSG_TO_ROUSG_SHARES_MULTIPLIER;
    }

    function _unwrap(uint256 _rOUSGAmount, uint256 ousgPrice) internal pure returns(uint256 tokens) {
        require(_rOUSGAmount > 0, "rOUSG: can't unwrap zero rOUSG tokens");

        uint256 ousgSharesAmount = getSharesByROUSG(_rOUSGAmount, ousgPrice);

        vm.assume(ousgSharesAmount >= OUSG_TO_ROUSG_SHARES_MULTIPLIER);

        tokens = ousgSharesAmount / OUSG_TO_ROUSG_SHARES_MULTIPLIER;
    }

    function test_WrapUnwrapReturnsInputTokens(uint256 initialOUSGAmount, uint256 ousgPrice) external {
        // bound inputs
        initialOUSGAmount  = bound(initialOUSGAmount, 100000e18, type(uint128).max);
        ousgPrice          = bound(ousgPrice, 105e18, 106e18);

        // wrap OUSG into rOUSG
        uint256 rousgShares = _wrap(initialOUSGAmount);

        // get the token amount of rOUSG equivalent to the received shares
        uint256 rousgAmount = _getROUSGByShares(rousgShares, ousgPrice);

        // use the token amount to unwrap rOUSG back into OUSG
        uint256 finalOUSGAmount = _unwrap(rousgAmount, ousgPrice);

        // verify amounts match; this fails as user is slighty short-changed
        assertEq(initialOUSGAmount, finalOUSGAmount);
    }
}
```

**Recommended Mitigation:** When calling `ROUSG::unwrap`, `burn` and `OUSGInstantManager::redeemRebasingOUSG`, instead of passing in the `ROUSG` token amount the callers should pass in the share amount which can be retrieved via `ROUSG::sharesOf`. The output token calculation can then be performed as `shares / OUSG_TO_ROUSG_SHARES_MULTIPLIER` which will always return the correct amount of tokens.

The existing functions do not necessarily need to be removed but additional functions should be created to allow users to input the share amounts. The following function has been tested via an invariant fuzz testing suite and appears to always return the correct amount:
```solidity
  // @audit this function allow unwrapping by shares instead of tokens
  // to prevent users being slightly short-changed such that users will
  // always receive the same input amount of OUSG tokens
  function unwrapShares(uint256 _shares) external whenNotPaused {
    uint256 ousgTokens = _shares / OUSG_TO_ROUSG_SHARES_MULTIPLIER;

    require(ousgTokens > 0, "rOUSG: no tokens to send, unwrap more shares");

    uint256 rousgBurned = getROUSGByShares(_shares);

    _burnShares(msg.sender, _shares);
    ousg.transfer(msg.sender, ousgTokens);

    emit Transfer(msg.sender, address(0), rousgBurned);
    emit TransferShares(msg.sender, address(0), _shares);
  }
```

Proof that this mitigation works, using a modified version of the PoC stateless fuzz test:

First ensure that `foundry.toml` has the fuzz setting increased for example:
```
[fuzz]
runs = 1000000
```

Then run this stand-alone stateless fuzz test which verifies the solution:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "forge-std/Test.sol";

// run from base project directory with:
// forge test --match-contract ROUSGWrapUnwrapFixedInvariantTest -vvv

contract ROUSGWrapUnwrapFixedInvariantTest is Test {

    uint256 public constant OUSG_TO_ROUSG_SHARES_MULTIPLIER = 10_000;

    function _wrap(uint256 _OUSGAmount) internal pure returns (uint256 shares) {
        require(_OUSGAmount > 0, "rOUSG: can't wrap zero OUSG tokens");

        shares = _OUSGAmount * OUSG_TO_ROUSG_SHARES_MULTIPLIER;
    }

    function _unwrapShares(uint256 shares) internal pure returns(uint256 tokens) {
        tokens = shares / OUSG_TO_ROUSG_SHARES_MULTIPLIER;
    }

    function test_WrapUnwrapReturnsInputTokens(uint256 initialOUSGAmount, uint256 ousgPrice) external {
        // bound inputs
        initialOUSGAmount  = bound(initialOUSGAmount, 100000e18, type(uint128).max);
        ousgPrice          = bound(ousgPrice, 105e18, 106e18);

        // wrap OUSG into rOUSG
        uint256 rousgShares = _wrap(initialOUSGAmount);

        // use the token amount to unwrap rOUSG back into OUSG
        uint256 finalOUSGAmount = _unwrapShares(rousgShares);

        assertEq(initialOUSGAmount, finalOUSGAmount);
    }
}
```

**Ondo:**
Fixed in commits [df0e491](https://github.com/ondoprotocol/rwa-internal/commit/df0e491fb081f4b7cd0d7329f8763e644ea77c18), [2aa437a](https://github.com/ondoprotocol/rwa-internal/commit/2aa437aa78435fc4533c3a9d223460da34e71647). We decided on not making any changes to `OUSGInstantManager` due to the amount of code changes necessary.

**Cyfrin:** Verified.
