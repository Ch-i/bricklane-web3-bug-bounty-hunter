---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Use assembly call to send native tokens when return data is not needed
vuln_class: []
---

# Use assembly call to send native tokens when return data is not needed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Solidity's `(bool ok,) = payable(addr).call{value: amount}("")` always copies return data into memory even when discarded. This wastes gas on the memory allocation and copy, and also exposes the caller to a "return-bomb" DoS where the callee returns a huge payload to grief the caller's gas. Using assembly `call` with zero-length return buffer avoids both issues.

```solidity
contracts/governance/ArmadaRedemption.sol
177:                (bool success,) = msg.sender.call{value: ethPayout}("");

contracts/governance/ArmadaTreasuryGov.sol
489:        (bool success,) = recipient.call{value: amount}("");
```

`ArmadaRedemption::redeem:177` is the higher-impact site - `msg.sender` is arbitrary, so a redeemer contract can return a maximally-sized payload to grief gas. `ArmadaTreasuryGov::transferETHTo:489` is gated to `windDownContract` and recipients are wind-down sweep destinations, so the return-bomb vector is bounded; the gas savings still apply.

**Recommended Mitigation:** Replace each site with an assembly `call` that skips return data entirely:

```diff
-        (bool success,) = msg.sender.call{value: ethPayout}("");
+        bool success;
+        assembly {
+            success := call(gas(), caller(), ethPayout, 0, 0, 0, 0)
+        }
```

```diff
-        (bool success,) = recipient.call{value: amount}("");
+        bool success;
+        assembly {
+            success := call(gas(), recipient, amount, 0, 0, 0, 0)
+        }
```

The last two zeros (`retOffset`, `retSize`) skip return data entirely.

**Armada:** Fixed in commits [7fe0547](https://github.com/ship-armada/armada-poc/commit/7fe05472d9f2c932cf26a5784ef2a9b78fbbe2af), [d62e42c](https://github.com/ship-armada/armada-poc/commit/d62e42c82141719d199e9285eab48dddefacd165).

**Cyfrin:** Verified.
