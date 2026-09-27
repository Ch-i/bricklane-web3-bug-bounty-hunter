---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-3
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
title: '`IDSServiceConsumer::DEPRECATED_ISSUER_MULTICALL, DEPRECATED_TA_MULTICALL`
  are both zero while the deployment utilities define them as 8194 and 8195, leaving
  two incompatible service-id registries'
vuln_class: []
---

# `IDSServiceConsumer::DEPRECATED_ISSUER_MULTICALL, DEPRECATED_TA_MULTICALL` are both zero while the deployment utilities define them as 8194 and 8195, leaving two incompatible service-id registries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** The service-id registry exists in two places that disagree. In Solidity both deprecated multicall ids are zero:

```solidity
uint256 public constant DEPRECATED_ISSUER_MULTICALL = 0;
uint256 public constant DEPRECATED_TA_MULTICALL = 0;
```

while the TypeScript registry used by the deployment utilities assigns them distinct non-zero values:

```typescript
DEPRECATED_ISSUER_MULTICALL: 8194,
DEPRECATED_TA_MULTICALL: 8195,
```

Neither constant is referenced anywhere else in either language, so nothing currently resolves them and no live token has a non-zero entry at id `0`, `8194` or `8195`. The defect is latent rather than active, but it is a defect in both directions.

Contract code written against the Solidity constants would address slot `0` for both services, so the two would collide with each other, the second write silently replacing the first. Off-chain tooling written against the TypeScript registry would read and write ids `8194` and `8195`, which no contract consults. Two components can therefore be correct with respect to their own source of truth and still not interoperate.

`ServiceConsumer::setDSService` offers no backstop. It writes `services[_serviceId]` for any `uint256`, with no rejection of `0` and no check that the id is one the registry defines, so a write to the collapsed id succeeds and emits `DSServiceSet` exactly as a legitimate registration would:

```solidity
function setDSService(uint256 _serviceId, address _address) public override onlyMaster returns (bool) {
    services[_serviceId] = _address;
    emit DSServiceSet(_serviceId, _address);
    return true;
}
```

**Recommended Mitigation:**
1. Pick one source of truth for service ids and generate the other from it, so the two registries cannot drift; alternatively delete both unused constants outright, since neither is referenced and the ids they describe hold no value on any live token
2. Reject `_serviceId == 0` in `setDSService` unless zero is a deliberately reserved and documented id, so a write to the collapsed id fails loudly instead of appearing to succeed
3. Add a test asserting exact equality for every service id exposed in both languages, which turns any future divergence into a build failure rather than a deployment-time surprise

**Securitize:** Fixed in commit [eadeeab](https://github.com/securitize-io/dstoken/commit/eadeeab517275b746abc65e46f46649a1728da8b) to align the constants then added a test to verify parity in commit [2d9d650](https://github.com/securitize-io/dstoken/commit/2d9d6500d9557af6d663bb82efff8932ef252cd2).

**Cyfrin:** Verified.
