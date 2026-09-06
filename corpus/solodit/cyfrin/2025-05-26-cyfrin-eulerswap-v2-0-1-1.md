---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Lack of events emitted on state changes
vuln_class: []
---

# Lack of events emitted on state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** Both [`ProtocolFee::setProtocolFee`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/utils/ProtocolFee.sol#L14-L19) and [`ProtocolFee::setProtocolFeeRecipient`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/utils/ProtocolFee.sol#L21-L23) changes state for the `EulerSwapFactory` however no events are emitted.

Consider emitting events from these functions for better off-chain tracking and transparency.

**Euler:** Fixed in commit [`05a9148`](https://github.com/euler-xyz/euler-swap/pull/97/commits/05a91488dcaf27633c26699e98694d99b73d20ea)

**Cyfrin:** Verified.
