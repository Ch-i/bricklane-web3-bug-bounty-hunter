---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[I-02] Future token’s getClaimInfo function can return inaccurate information
  about token’s cancel status'
vuln_class: []
---

# [I-02] Future token’s getClaimInfo function can return inaccurate information about token’s cancel status

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTFutureTokenV2.sol](https://github.com/EthSign/tokentable-v2-evm/blob/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TTFutureTokenV2.sol)

**Description:**

The `getClaimInfo(...)` function is supposed to return 3 different variables for the `tokenId` provided:

1. The amount of tokens claimable as of now;
2. The amount of tokens claimed as of now;
3. The cancellability of the token’s unlocker;

However, the cancellability of the unlocker is not enough to determine if a token is cancelled, as the token could get cancelled first and then by calling the `disableCancel(...)` function it will show that it’s not cancellable, which is contradictory to the state of the `tokenId`.

**Status:** Fixed

**Update from TokenTable:** Replaced this function in [15637996d75331063f50ecbc2a5b660f33268f4b](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/15637996d75331063f50ecbc2a5b660f33268f4b)
