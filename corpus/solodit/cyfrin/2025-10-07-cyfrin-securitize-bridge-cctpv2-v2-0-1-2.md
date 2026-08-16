---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Don't use `transfer` to send ETH
vuln_class: []
---

# Don't use `transfer` to send ETH

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Using `transfer` to send ETH hasn't been recommended since the Istanbul hard fork in December 2019 which increased the gas cost of some operations; `transfer` hard-codes gas to 2300 which can cause receiving functions to revert hence is not future-proof.

The [recommended way to send eth](https://www.securitize-io.io/glossary/sending-ether-transfer-send-call-solidity-code-example) is to use `call` and Solady has an optimized way of doing this in [SafeTransferLib::safeTransferETH](https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L95-L103).

`transfer` also may not work as expected on L2s, for example there was this [incident](https://thedefiant.io/news/defi/zksync-rescues-gemholic) which resulted in 921 ETH being stuck on zksync Era due to the smart contract using transfer to send eth, though eventually zksync developed a [solution](https://www.theblock.co/post/225364/zksync-unfreeze-millions-stuck) to rescue the stuck eth.

Affected code in `USDCBridgeV2::withdrawETH`:
```solidity
bridge/USDCBridgeV2.sol
202:        _to.transfer(amount);
```

**Securitize:** Fixed in commit [2b18646](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/2b18646e6344fcebe4f32107cd56812877ddadea).

**Cyfrin:** Verified.
