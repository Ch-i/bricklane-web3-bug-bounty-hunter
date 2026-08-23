---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-0-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Auto redemption functionality broken by incorrect address passed to `SmartVaultV4::autoRedemption`
vuln_class: []
---

# Auto redemption functionality broken by incorrect address passed to `SmartVaultV4::autoRedemption`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** `SmartVaultV4::autoRedemption` has the following signature:

```solidity
function autoRedemption(
    address _swapRouterAddress,
    address _quoterAddress,
    address _collateralToken,
    bytes memory _swapPath,
    uint256 _USDCTargetAmount,
    address _hypervisor
)
```

However the invocation in `AutoRedemption::fulfillRequest` incorrectly passes the vault address in place of the swap router address:

```solidity
IRedeemable(_smartVault).autoRedemption(
    _smartVault, quoter, _token, _collateralToUSDCPath, _USDsTargetAmount, _hypervisor
);
```

**Impact:** Auto redemption functionality will become completely broken when attempting to repay the debt of a non-legacy vault.

**Recommended Mitigation:** Pass the correct swap router address stored in the `SmartVaultManagerV6` contract.

**The Standard DAO:** Fixed by commit [4400e25](https://github.com/the-standard/smart-vault/commit/4400e25c87880b7ab1b5d19fbe520e4db5b70122).

**Cyfrin:** Verified. The correct `swapRouter` address is now passed.

\clearpage
