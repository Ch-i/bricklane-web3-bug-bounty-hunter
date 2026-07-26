---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: 'Pre-deploy placeholders and deploy-script gaps: unset roles, placeholder addresses
  and stale timestamps'
vuln_class: []
---

# Pre-deploy placeholders and deploy-script gaps: unset roles, placeholder addresses and stale timestamps

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of pre-deployment configuration gaps - placeholder values, unfilled TODOs, and missing role grants in deploy scripts. Each sub-item is a distinct instance. All are non-exploitable (pre-deploy or role-gated) but each represents a runbook step that must happen before mainnet or the protocol misbehaves.

---

**1. Mainnet deploy branch grants `EXTENDER_ROLE` to `address(0)` - TODO placeholder**

`ChainlinkUpDownAdapterDeployment.s.sol:48` passes `extender: 0x0000000000000000000000000000000000000000` for the BSC mainnet branch, with an inline `// TODO: operator address` comment. If the script runs as-is on mainnet, `EXTENDER_ROLE` is granted to `address(0)`, meaning no real address holds the role until an admin grants it post-deploy.

**Impact:** `extend()` is uncallable on mainnet until an admin manually grants `EXTENDER_ROLE` to a real operator address. Recoverable misconfiguration, not a vulnerability.

**Recommended:** Fill in the real operator address in the mainnet branch before running the deploy script. Add defensive requires at the top of `run()`:

```solidity
require(params.extender != address(0), "extender address not set");
require(params.initializer != address(0), "initializer address not set");
require(params.msig != address(0), "msig address not set");
```

---

**2. `config.production.json` ships with zero `adapterAddress` - pre-deploy placeholder**

`cre/data-stream-resolution/close-rounds/config.production.json` line 4 sets `"adapterAddress": "0x0000000000000000000000000000000000000000"`. Pre-deployment placeholder to be updated once the adapter is deployed to BSC mainnet.

**Impact:** If the config reaches CRE production with the zero address in place, the CRE workflow silently no-ops on every cron tick rather than loudly failing. The CRE workflow itself does not validate `adapterAddress != 0x0` before submitting reports, so the misconfiguration is not caught on the CRE side either - tracked as a separate Low finding in this repo.

**Recommended:** Add "update `adapterAddress` in `config.production.json`" as a named step in the production deployment runbook. Consider a commit-time CI check that rejects config files containing the zero address.

---

**3. Init script hardcodes past `startTime` - pre-deploy placeholder needs explicit update step**

`ChainlinkUpDownAdapterInitializeRoundSeries.s.sol:38` hardcodes `uint32 startTime = 1776198600` (Tue Apr 14 2026 20:30 UTC). If the script runs meaningfully after this timestamp, every pre-created round has an `endTimestamp` in the past - outcomes are deterministically known from the Chainlink Data Streams historical API before any CRE run. No inline `// TODO` comment flags this to operators (unlike the `extender` placeholder in the deploy script).

**Impact:** If run verbatim without updating `startTime`, on-chain state ends up with pre-created rounds whose outcomes are publicly knowable before the CRE settles them. The related contract-level defensive-depth gap (missing sanity bound in `_initialize`, tracked as a separate Informational finding) would catch this even if operator discipline fails.

**Recommended:** Add an inline comment + runtime assertion:

```solidity
// TODO: update startTime to a recent timestamp (within the last interval) before running
uint32 public constant startTime = 1776198600;
// ...
require(
    block.timestamp - startTime < uint256(5 minutes),
    "startTime stale; update before running"
);
```

Alternatively, derive `startTime` at script runtime:

```solidity
uint32 startTime = uint32(block.timestamp) / interval * interval - interval;
```

---

**4. `PAUSER_ROLE` and `EMERGENCY_CLOSE_ROUND_ROLE` never granted in deploy script**

`ChainlinkAdapter::togglePaused` and `ChainlinkUpDownAdapter::emergencyCloseRounds` have no role-holder post-deploy. Legitimate emergency recovery (DS API outage, expired reports, stuck rounds) cannot happen until admin remembers to self-grant.

**Impact:** Delayed emergency recovery.

**Recommended:** Grant `PAUSER_ROLE` and `EMERGENCY_CLOSE_ROUND_ROLE` explicitly to the msig inside `ChainlinkUpDownAdapterDeployment.s.sol`. Emit an alert if any role is granted from a non-deploy-script tx post-deploy.

---

**Predict.fun:** Fixed in commit [333d76a](https://github.com/PredictDotFun/prediction-market/pull/71/changes/333d76a6970ed0c0fa424bb66866002bb9a2d323).

**Cyfrin:** Verified.
