---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Configuring compose option will prevent users from receiving TGLD on the destination
  chain
vuln_class: []
---

# Configuring compose option will prevent users from receiving TGLD on the destination chain

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** Users are able to send their TGLD by calling `send` function of TempleGold contract.
Since `SendParam` struct is passed from users, they can add any field including compose data into the message.
However on the destination chain, in `_lzReceive` function, it blocks messages with compose options in it:
```Solidity
if (_message.isComposed()) { revert CannotCompose(); }
```

This means that users who call `send` with compose option, they will not receive TGLD tokens on the destination chain.

**Impact:** Token transfer does not work based on the parameter and causes loss of funds for users.

**Recommended Mitigation:**
1. In `send` function, if the `_sendParam` includes compose option, it should revert.
2. Even better, `send` function only inputs mandatory fields from users like the amount to send, and it constructs `SendParam` in it rather than receiving it as a whole from the user.

**TempleDAO:** Fixed in [PR 1029](https://github.com/TempleDAO/temple/pull/1029)

**Cyfrin:** Verified
