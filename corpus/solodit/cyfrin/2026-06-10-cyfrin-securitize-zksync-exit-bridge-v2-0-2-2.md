---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: Redundant SLOAD of `dsToken` in `SecuritizeBridge::bridgeDSTokensToAddress`
vuln_class: []
---

# Redundant SLOAD of `dsToken` in `SecuritizeBridge::bridgeDSTokensToAddress`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `SecuritizeBridge::bridgeDSTokensToAddress` re-reads `dsToken` from storage for the event argument `address(dsToken)`, but the internal `_bridgeDSTokensInternal` it just called already cached `dsToken` into the local `_dsToken` (line 427). This issues a fresh SLOAD on the user-facing hot path.

```solidity
contracts/bridge/SecuritizeBridge.sol
300:        string memory investorId = _bridgeDSTokensInternal(_targetChain, _value, _destinationAddress);
301:        emit DSTokenBridgeSend(_targetChain, address(dsToken), _addressToBytes32(_msgSender()), _destinationAddress, investorId, _value);
427:        IDSToken _dsToken = dsToken;
```

**Recommended Mitigation:** Change `_bridgeDSTokensInternal` to `returns (string memory investorId, address dsTokenAddr)`, set `dsTokenAddr = address(_dsToken)` inside it, and update the emit at line 301 to use the returned `dsTokenAddr` instead of `address(dsToken)`.

**Securitize:** Acknowledged.

\clearpage
