---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`SwellLib.BOT` can delete active validators when bot methods are paused'
vuln_class: []
---

# `SwellLib.BOT` can delete active validators when bot methods are paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Almost all of the functions callable by `SwellLib.BOT` contain the following check to prevent bot functions from working when bot methods are paused:

```solidity
if (AccessControlManager.botMethodsPaused()) {
  revert SwellLib.BotMethodsPaused();
}
```

The one exception is [`NodeOperatorRegistry::deleteActiveValidators`](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/NodeOperatorRegistry.sol#L417-L423) which is callable by `SwellLib.BOT` even when bot methods are paused. Consider:
* adding a similar check to this function such that `SwellLib.BOT` is not able to call it when bot methods are paused
* alternatively add an explicit comment to this function stating that it should be callable by `SwellLib.BOT` even when bot methods are paused.

One possible implementation for the first solution:
```solidity
bool isBot = AccessControlManager.hasRole(SwellLib.BOT, msg.sender);

// prevent bot from calling this function when bot methods are paused
if(isBot && AccessControlManager.botMethodsPaused()) {
  revert SwellLib.BotMethodsPaused();
}

// function only callable by admin & bot
if (!AccessControlManager.hasRole(SwellLib.PLATFORM_ADMIN, msg.sender) && !isBot) {
  revert OnlyPlatformAdminOrBotCanDeleteActiveValidators();
}
```

**Swell:** Fixed in commit [1a105b7](https://github.com/SwellNetwork/v3-contracts-lst/commit/1a105b76899780e30b1fb88abdede11c0c0586ba).

**Cyfrin:**
Verified.
