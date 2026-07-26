---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-0-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: '`AutoRedemption::fulfillRequest` should never be allowed to revert'
vuln_class: []
---

# `AutoRedemption::fulfillRequest` should never be allowed to revert

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** Given that the Chainlink Functions DON will not retry failed fulfilments, `AutoRedemption::fulfillRequest` should never be allowed to revert; otherwise, `lastRequestId` will not be reset to `bytes32(0)` which means `AutoRedemption::performUpkeep` will never be able to trigger new requests.

Currently, inline comments suggest that there is an intention to revert if the Chainlink Functions DON returns an error; however, this should be avoided for the reason explained above. Similarly, any potential malformed response or reverts caused by external calls should be handled gracefully and fall through to this line:

```solidity
lastRequestId = bytes32(0);
```

**Impact:** Complete DoS of the auto redemption functionality.

**Recommended Mitigation:** * Do __not__ revert if an error is reported.
* Validate the response against its expected length to ensure that the decoding does not revert.
* Handle reverts from all external calls using `try/catch` blocks.
* Short-circuit if `AutoRedemption::calculateUSDsToTargetPrice` returns `0` (since this will cause the swap to [revert](https://github.com/Uniswap/v3-core/blob/main/contracts/UniswapV3Pool.sol#L603)).
* Optionally add an access-controlled admin function to reset `lastRequestId`.

**The Standard DAO:** Fixed by commit [5235524](https://github.com/the-standard/smart-vault/commit/523552498edefe77aa2782d2a887bb1980cf80b9).

**Cyfrin:** Verified. The response length is now validated against its expected length, which will also result in the logic being skipped if an error is reported. `AutoRedemption::runAutoRedemption` will only run if the target `USDs` amount is non-zero and other reverts from external calls are handled using `try/catch` blocks. An admin function to forcibly reset `lastRequestId` has not been added.
