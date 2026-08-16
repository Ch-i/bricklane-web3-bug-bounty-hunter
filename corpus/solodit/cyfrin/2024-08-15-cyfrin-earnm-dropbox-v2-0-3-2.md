---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Refactor duplicate fee sending code into one private function
vuln_class: []
---

# Refactor duplicate fee sending code into one private function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::claimDropBoxes` and `revealDropBoxes`  are two `payable` external functions which both implement duplicate fee sending code; refactor this into 1 private function:
```solidity
  function _sendFee(uint256 amount) private {
    bool sent;
    address feesReceiver = feesReceiverAddress;
    // Use low level call to send fee to the fee receiver address
    assembly {
      sent := call(gas(), feesReceiver, amount, 0, 0, 0, 0)
    }
    if (!sent) revert Unauthorized();
  }
```

Then simply call it from both external functions:
```solidity
_sendFee(msg.value);
```

**Mode:**
Fixed in commit [327c12b](https://github.com/Earnft/dropbox-smart-contracts/commit/327c12b4b9351fb87df9f0b4706e6ac662cb59cc).

**Cyfrin:** Verified.
