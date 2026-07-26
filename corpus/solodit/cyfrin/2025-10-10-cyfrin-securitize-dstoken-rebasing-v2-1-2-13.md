---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-13
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`MulticallProxy::_callTarget` doesn''t check if `target` has code'
vuln_class: []
---

# `MulticallProxy::_callTarget` doesn't check if `target` has code

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `IssuerMulticall::multicall` allows permissioned users to perform multiple calls against arbitrary targets, calling `MulticallProxy::_callTarget` for each target.

`MulticallProxy::_callTarget` doesn't check whether each `target` has code:
```solidity
function _callTarget(address target, bytes memory data, uint256 i) internal returns (bytes memory) {
    // @audit returns true if `target` has no code
    (bool success, bytes memory returndata) = target.call(data);
    if (!success) {
        if (returndata.length > 0) {
            // Assumes revert reason is encoded as string
            revert MulticallFailed(i, _getRevertReason(returndata));
        } else {
            revert MulticallFailed(i, "Call failed without revert reason");
        }
    }
    return returndata;
}
```

**Impact:** When using `call` on an address with no code, `call` returns `true`. This can mislead the caller to think that the multi-call succeeded when in fact it didn't if one of the targets within the multi-call has no code.

**Recommended Mitigation:** Verify `target` has code:
```diff
    function _callTarget(address target, bytes memory data, uint256 i) internal returns (bytes memory) {
+        require(target.code.length > 0, "Target is not a contract");
```

**Securitize:** The affected contracts were deleted as they were obsolete.

**Cyfrin:** Verified.
