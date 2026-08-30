---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::fallback` `else` branch is unreachable'
vuln_class: []
---

# `OnChainLab::fallback` `else` branch is unreachable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `OnChainLab::fallback` checks `config.callerPolicy == CallerPolicy.ENTRYPOINT_ONLY` and falls through to `else { revert InvalidCallerPolicy(); }`. `CallerPolicy` only has `ENTRYPOINT_ONLY` (the storage default for `callerPolicy` is the zero-byte enum value, which is `ENTRYPOINT_ONLY`). The `else` branch is therefore unreachable in practice. `_installSelector` already enforces `callerPolicy == ENTRYPOINT_ONLY` (`SelectorManager.sol:63-65`), so no other value can ever be installed; the runtime check is redundant. Either expand the enum (intended) or remove the dead branch.

```solidity
src/OnChainLab.sol
201:        if (config.callerPolicy == CallerPolicy.ENTRYPOINT_ONLY) {
202:            if (msg.sender != address(ENTRYPOINT)) {
203:                revert InvalidCaller();
204:            }
205:        } else {
206:            revert InvalidCallerPolicy();
207:        }

src/core/SelectorManager.sol
63:        if (callerPolicy != CallerPolicy.ENTRYPOINT_ONLY) {
64:            revert InvalidCallerPolicy();
65:        }
```

**Recommended Mitigation:** Replace the `if/else` with a direct check while only `ENTRYPOINT_ONLY` is supported:

```solidity
// Until additional policies are introduced, only ENTRYPOINT_ONLY is reachable.
if (config.callerPolicy != CallerPolicy.ENTRYPOINT_ONLY) revert InvalidCallerPolicy();
if (msg.sender != address(ENTRYPOINT)) revert InvalidCaller();
```

When new policies are added, expand both `_installSelector` (`src/core/SelectorManager.sol:63-65`) and this dispatch in lockstep.

**Molecule:** Acknowledged.
