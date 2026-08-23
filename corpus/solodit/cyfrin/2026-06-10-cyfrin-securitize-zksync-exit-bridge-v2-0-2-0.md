---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: Use assembly `call` for ETH transfers that discard return data
vuln_class: []
---

# Use assembly `call` for ETH transfers that discard return data

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `(bool ok, ) = addr.call{value: amount}("")` copies the callee's entire return payload into memory even though it is discarded, wasting gas and exposing the caller to a return-bomb DoS. Use assembly `call` with zero output size instead.

```solidity
contracts/bridge/ZKSyncSecuritizeBridge.sol
99:        (bool sent, ) = _to.call{value: amount}("");

contracts/bridge/SecuritizeBridge.sol
406:        (bool sent, ) = _to.call{value: amount}("");
491:            (bool ok,) = payable(_msgSender()).call{value: extra}("");

contracts/bridge/USDCBridgeV2.sol
250:        (bool sent, ) = _to.call{value: amount}("");
```

**Recommended Mitigation:**
```solidity
bool sent;
assembly {
    sent := call(gas(), _to, amount, 0, 0, 0, 0)
}
if (!sent) revert ETHTransferError();
```

Apply analogously to the refund at `SecuritizeBridge.sol:491`.

**Securitize:** Acknowledged.
