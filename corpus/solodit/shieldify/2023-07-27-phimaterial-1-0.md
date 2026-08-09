---
affected_contracts: []
derives_from: []
id: solodit-shieldify-2023-07-27-phimaterial-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-07-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
tags:
- firm:shieldify
- report:2023-07-27-phimaterial
title: '[M-01] Signature Does Not Contain a Deadline, Making It Reusable'
vuln_class: []
---

# [M-01] Signature Does Not Contain a Deadline, Making It Reusable

_Section severity (from Solodit section header): Medium_  
_Audit firm: Shieldify_  
_Source report: [2023-07-27-PHIMaterial.md](https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md)_

---

**Severity**

Medium Risk

**Description**

The `PhiDaily.sol` contract has the `claimMaterialObject` function that allow a user to claim a material object directly. These then call the private `_processClaim()` function to check that the coupon has been signed by the admin signer.
The `digest` variable in `_processClaim()` accepts an `eventId`, `logicId` and `msgSender()`, but it does not accept any variable that defines a timeframe in which this signature is valid and does not check if such variable has passed a certain amount of time. Without such a variable and a corresponding check for it, the issued signature essentially becomes timeless and reusable again. This is also applicabe in the other functions that call the `_processClaim()` function, namely - `batchClaimMaterialObject`, `claimMaterialObjectByRelayer` and `batchClaimMaterialObjectByRelayer` .This can negatively impact the business logic of the protocol, as one material object can be claimed more than once.

**Location of Affected Code**

File: [`src/PhiDaily.sol#L248-L258`](https://github.com/PHI-LABS-INC/PHIMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/PhiDaily.sol#L248-L258)

```solidity
// Function to claim a material object.
function claimMaterialObject(
    uint32 eventid,
    uint16 logicid,
    Coupon memory coupon
)
    external
    onlyIfAlreadyClaimed(eventid, logicid)
    nonReentrant
{

function _processClaim(uint32 eventid, uint16 logicid, Coupon memory coupon) private {
    // Check that the coupon sent was signed by the admin signer
    bytes32 digest = keccak256(abi.encode(eventid, logicid, _msgSender()));
```

**Recommendation**

Consider adding a deadline check in the `claimMaterialObject()` function and an `expiresIn`/`deadline` variable either as an argument that is passed to the `claimMaterialObject()` function or in the `Coupon` struct. The `claimMaterialObject()` function should also contain a check if the `expiresIn` / `deadline` variable is valid:

`Example:`

```diff
    function claimMaterialObject(
        uint32 eventid,
        uint16 logicid,
++      uint256 expiresIn
        Coupon memory coupon
    )
        external
        onlyIfAlreadyClaimed(eventid, logicid)
        nonReentrant
    {
++     if (expiresIn <= block.timestamp){
++        revert SignatureExpired()
++     }
        _processClaim(eventid, logicid, coupon, expiresIn);
    }

    function _processClaim(uint32 eventid, uint16 logicid, Coupon memory coupon, expiresIn) private {
    // Check that the coupon sent was signed by the admin signer
++   bytes32 digest = keccak256(abi.encode(eventid, logicid, _msgSender(), expiresIn));
```

**Team Response**

Acknowledged and fixed by setting expiration period `expiresIn` to `Coupon` and added/modified tests for it.
