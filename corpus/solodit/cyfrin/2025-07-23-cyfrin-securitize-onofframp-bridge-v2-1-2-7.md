---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Refund address in `bridgeDSTokens` function should be configurable
vuln_class: []
---

# Refund address in `bridgeDSTokens` function should be configurable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** In the `SecuritizeBridge::bridgeDSTokens` function, `msg.sender` is assigned as the refund address.
```solidity
        // Send Relayer message
        wormholeRelayer.sendPayloadToEvm{value: msg.value} (
            targetChain,
            targetAddress,
            abi.encode(
                investorDetail.investorId,
                value,
                msg.sender,
                investorDetail.country,
                investorDetail.attributeValues,
                investorDetail.attributeExpirations
            ), // payload
            0, // no receiver value needed since we"re just passing a message
            gasLimit,
            whChainId,
            msg.sender //@audit refund address, any leftover gas will be sent to this address
        );
```
Wormhole will refund the leftover gas to `refundAddress`. However, if the `msg.sender` is a smart contract that does not implement a function to withdraw the native gas token, any potential refund sent to it will become permanently inaccessible. This could result in locked funds that cannot be recovered by the original user.

**Recommended Mitigation:** Add a parameter to explicitly specify a refund address instead of defaulting to `msg.sender`. This allows the user or calling contract to define a fallback or externally owned account (EOA) for receiving refunds.

```solidity
function bridgeDSTokens(..., address refundAddress) external {
    require(refundAddress != address(0), "Invalid refund address");
    ...
}
```

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.
