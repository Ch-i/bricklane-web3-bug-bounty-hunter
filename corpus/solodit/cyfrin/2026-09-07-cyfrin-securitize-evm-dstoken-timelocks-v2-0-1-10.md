---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-10
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: Gate `DSToken::executeOverCapMint` on the token pause to give the transfer
  agent an instant block on scheduled exceptional mints
vuln_class: []
---

# Gate `DSToken::executeOverCapMint` on the token pause to give the transfer agent an instant block on scheduled exceptional mints

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** The exceptional-mint path has an asymmetry in who can act and how fast. `DSToken::executeOverCapMint` is `onlyIssuerOrAbove` and the operation id is public through `OverCapMintScheduled`, so any ISSUER can execute any scheduled mint. `DSToken::cancelOverCapMint` is `onlyMaster`, and after handover master authority is the master `TimelockController`, so a cancel is itself a scheduled operation that matures after the master `minDelay`.

Between schedule and execute the only instant privileged action is a TRANSFER_AGENT `pause`, and execute does not check it: issuance has always ignored `paused` (the flag is enforced only in `ComplianceService::preTransferCheck, preInternalTransferCheck`), which is reasonable for within-cap mints such as bridge settlement but leaves the exceptional path with no instant stop. `timelocks.md` section 6 lists execution while paused as a case to assess.

**Impact:** Once an exceptional mint is scheduled, stopping it depends entirely on the cancel arriving before `readyAt`, which ties the safety of the path to the relative values of `overCapDelay` and the master delay plus detection and human response time. A pause gives no protection today, so a transfer agent who spots a suspicious `OverCapMintScheduled` has no way to hold the mint while the cancel is queued.

**Recommended Mitigation:** Add `whenNotPaused` to `executeOverCapMint` only; leave `scheduleOverCapIssuance` and within-cap issuance as they are:

```solidity
function executeOverCapMint(bytes32 _operationId) external override onlyIssuerOrAbove whenNotPaused {
```

A pause then holds the mint until MASTER, the same authority that cancels, lifts it. Note in the runbook that a pause freezes the exceptional-mint queue and that an operation whose grace period lapses during a long pause must be rescheduled. The gate needs a non-zero `overCapDelay` to be useful, since with zero delay schedule and execute land in one block.

**Securitize:** Fixed in commit [9595027](https://github.com/securitize-io/dstoken/commit/9595027e0113dd8525c762a99352809f79628845).

**Cyfrin:** Verified. The finding is resolved by relaxing `cancelOverCapMint` access control so an instant canceller exists after handover, and the trade-off of the relaxed permissions is documented in the code and the runbook.
