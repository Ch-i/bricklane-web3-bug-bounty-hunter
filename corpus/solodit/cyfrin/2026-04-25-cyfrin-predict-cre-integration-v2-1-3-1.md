---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Emit before state change or use input value to avoid storage re-read
vuln_class: []
---

# Emit before state change or use input value to avoid storage re-read

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Several setters in `ChainlinkReceiverBase` cache a previous storage value into a local purely for an event, or re-read storage after writing it:

```solidity
ChainlinkReceiverBase.sol
138:        address previousAuthor = s_expectedAuthor;
139:        s_expectedAuthor = _author;
140:        emit ExpectedAuthorUpdated(previousAuthor, _author);

170:        s_expectedWorkflowName = bytes10(first10);
171:        emit ExpectedWorkflowNameUpdated(previousName, s_expectedWorkflowName);  // re-reads storage!

249:        address previousForwarder = s_forwarderAddress;
250:        s_forwarderAddress = _forwarder;
251:        emit ForwarderAddressUpdated(previousForwarder, _forwarder);
```

Line 171 re-reads `s_expectedWorkflowName` (warm SLOAD ~100 gas) immediately after writing — use the local instead.

**Impact:** Minor gas waste per admin setter call.

**Recommended Mitigation:**
```solidity
function setExpectedAuthor(address _author) external onlyRole(DEFAULT_ADMIN_ROLE) {
    emit ExpectedAuthorUpdated(s_expectedAuthor, _author);
    s_expectedAuthor = _author;
}

bytes10 newName = bytes10(first10);
emit ExpectedWorkflowNameUpdated(s_expectedWorkflowName, newName);
s_expectedWorkflowName = newName;
```

**Predict.fun:** In commit [a0aa366](https://github.com/PredictDotFun/prediction-market/commit/a0aa3660fef0f8f08806db61d48a0a4ec8fd1cca) `s_expectedAuthor` and `s_expectedWorkflowName` were refactored into a mapping and now set in `setIsWorkflowAuthorAndNameValid`.

**Cyfrin:** After the mentioned workflow author & name refactoring, the only remaining optimization relevant to this issue is in [_setForwarderAddress](https://github.com/PredictDotFun/prediction-market/blob/feat/chainlink-adapter/contracts/Adapters/Chainlink/ChainlinkReceiverBase.sol#L210-L212) where `previousForwarder` can be optimized away by emitting the event first:
```diff
    function _setForwarderAddress(address _forwarder) private {
        if (_forwarder == address(0)) {
            revert InvalidForwarderAddress();
        }
-       address previousForwarder = forwarderAddress;
+       emit ForwarderAddressUpdated(forwarderAddress, _forwarder);
        forwarderAddress = _forwarder;
-       emit ForwarderAddressUpdated(previousForwarder, _forwarder);
    }
```
