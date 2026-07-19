---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Some functions of `Goldilend` will revert forever.
vuln_class: []
---

# Some functions of `Goldilend` will revert forever.

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** `Goldilend.multisigInterestClaim()/apdaoInterestClaim()/sunsetProtocol()` will revert forever because they doesn't withdraw `ibgt` from `ibgtVault` before the transfer.

```solidity
  function multisigInterestClaim() external {
    if(msg.sender != multisig) revert NotMultisig();
    uint256 interestClaim = multisigClaims;
    multisigClaims = 0;
    SafeTransferLib.safeTransfer(ibgt, multisig, interestClaim);
  }

  /// @inheritdoc IGoldilend
  function apdaoInterestClaim() external {
    if(msg.sender != apdao) revert NotAPDAO();
    uint256 interestClaim = apdaoClaims;
    apdaoClaims = 0;
    SafeTransferLib.safeTransfer(ibgt, apdao, interestClaim);
  }

...

  function sunsetProtocol() external {
    if(msg.sender != timelock) revert NotTimelock();
    SafeTransferLib.safeTransfer(ibgt, multisig, poolSize - outstandingDebt);
  }
```

As `ibgtVault` has all `ibgt` of `Goldilend`, they should withdraw from `ibgtVault` first.

**Impact:** `Goldilend.multisigInterestClaim()/apdaoInterestClaim()/sunsetProtocol()` will revert forever.

**Recommended Mitigation:** 3 functions should be changed like the below.

```diffclea
  function multisigInterestClaim() external {
    if(msg.sender != multisig) revert NotMultisig();
    uint256 interestClaim = multisigClaims;
    multisigClaims = 0;
+  iBGTVault(ibgtVault).withdraw(interestClaim);
    SafeTransferLib.safeTransfer(ibgt, multisig, interestClaim);
  }

  /// @inheritdoc IGoldilend
  function apdaoInterestClaim() external {
    if(msg.sender != apdao) revert NotAPDAO();
    uint256 interestClaim = apdaoClaims;
    apdaoClaims = 0;
+  iBGTVault(ibgtVault).withdraw(interestClaim);
    SafeTransferLib.safeTransfer(ibgt, apdao, interestClaim);
  }

...

  function sunsetProtocol() external {
    if(msg.sender != timelock) revert NotTimelock();
+  iBGTVault(ibgtVault).withdraw(poolSize - outstandingDebt);
    SafeTransferLib.safeTransfer(ibgt, multisig, poolSize - outstandingDebt);
  }
```

**Client:** Fixed in [PR #9](https://github.com/0xgeeb/goldilocks-core/pull/9) and [PR #12](https://github.com/0xgeeb/goldilocks-core/pull/12)

**Cyfrin:** Verified.
