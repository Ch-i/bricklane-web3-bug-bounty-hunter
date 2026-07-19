---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Auto redemption logic can be abused by an attacker due to insufficient access
  control
vuln_class: []
---

# Auto redemption logic can be abused by an attacker due to insufficient access control

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** `AutoRedemption::performUpkeep` is exposed for use by the Chainlink Automation DON when upkeep is required:

```solidity
function performUpkeep(bytes calldata performData) external {
    if (lastRequestId == bytes32(0)) {
        triggerRequest();
    }
}
```

However, there is an absence of access control that allows the function to be called by an address. Since `lastRequestId` is reset to `bytes32(0)` at the end of `AutoRedemption::fulfillRequest` execution, this means that upkeep can be repeatedly performed after the previous one has succeeded, regardless the trigger condition.

If `AutoRedemption::fulfillRequest` reverts, the `lastRequestId` state will not be reset which completely blocks all future auto redemptions due to the conditional in `AutoRedemption::performUpkeep` shown above. Combined with the use of `ERC20::balanceOf` within both `SmartVaultV4Legacy::autoRedemption` and `SmartVaultV4::autoRedemption` to determine the amount `USDs` repaid, an attacker can force this DoS condition by sending a small amount of `USDs` directly to the target vault:

```solidity
uint256 _usdsBalance = USDs.balanceOf(address(this));
minted -= _usdsBalance;
```

This causes the vault balance to be inflated above the expected maximum `minted` amount and execution to revert due to underflow. Since the Chainlink Functions DON will not retry failed fulfilment, there will be no way to reset the state and recover core functionality without complete redeployment.

**Impact:** An attacker can repeatedly trigger auto redemption regardless of the trigger condition and without relying on price oracle manipulation. This could amount to a loss of funds to the protocol since the Chainlink subscription will be billed on every fraudulent fulfilment attempt. Alternatively, an attacker could completely block functionality of the auto redemption mechanism if fulfilment is made to revert.

**Recommended Mitigation:** * Re-check the trigger condition within `AutoRedemption::performUpkeep` and also consider adding [access control](https://docs.chain.link/chainlink-automation/guides/forwarder).
* Calculate the amount of `USDs` repaid as the balance diff rather than using the vault balance directly.

**The Standard DAO:** Fixed by commit [5ec532e](https://github.com/the-standard/smart-vault/commit/5ec532e5f3813a865102501dbb91cf13a0813930).

**Cyfrin:** The trigger condition is re-checked and a TWAP has been implemented, however:
* It is recommended to use a substantially large interval (at least 900 seconds, if not 1800 seconds) to protect against manipulation. Note: Uniswap V3 pool oracles are not multi-block MEV resistant.
* The `USDs` repayment amount calculation has not been modified to use balance diffs instead of direct `balanceOf()`.

**The Standard DAO:** Fixed by commit [a8cdc77](https://github.com/the-standard/smart-vault/commit/a8cdc77d1fac9817128e1f3c1c8a1ab57f715513), using the amount out of the swap rather than balance checks.

**Cyfrin:** Verified. The TWAP interval has been increased and the redeemed amount has been modified to use the value output from the swap.
