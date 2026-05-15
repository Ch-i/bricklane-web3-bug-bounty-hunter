---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-22
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use `uint128` for `revealFee` and `claimFee` for more efficient storage packing
vuln_class: []
---

# Use `uint128` for `revealFee` and `claimFee` for more efficient storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Currently `revealFee` and `claimFee` use `uint256` and are set to `1 ether` with a max value of `1000 ether`. Hence they each take up 1 storage slot but this is not that efficient since:
```solidity
1 ether           = 1000000000000000000
1000 ether        = 1000000000000000000000
type(uint128.max) = 340282366920938463463374607431768211455
```

Therefore use `uint128` for `revealFee` and `claimFee`:
```solidity
// storage
  uint128 public revealFee = 1 ether;
  uint128 public claimFee = 1 ether;
  uint128 internal constant MAX_MINT_FEE = 1000 ether;
  uint128 internal constant MAX_CLAIM_FEE = 1000 ether;

// function updates
function setRevealFee(uint128 _mintFee) external onlyOwner {
  function setClaimFee(uint128 _claimFee) external onlyOwner {
```

Also update events in `DropBoxFractalProtocol`:
```solidity
  event RevealFeeUpdated(uint128 revealFee);
  event ClaimFeeUpdated(uint128 claimFee);
```

**Mode:**
Fixed in commit [fb20301](https://github.com/Earnft/dropbox-smart-contracts/commit/fb20301f77c9ae0c7c2333a13a11ca4b02d88366).

**Cyfrin:** Verified.
