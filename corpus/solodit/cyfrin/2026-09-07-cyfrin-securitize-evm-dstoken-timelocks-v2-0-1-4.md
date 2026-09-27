---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-4
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
title: '`BulkOperator` holds `ROLE_ISSUER` but is registered under no service id,
  so handover and verification cannot see it and its `owner` retains instant upgrade
  authority'
vuln_class: []
---

# `BulkOperator` holds `ROLE_ISSUER` but is registered under no service id, so handover and verification cannot see it and its `owner` retains instant upgrade authority

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `ServiceConsumer::onlyMaster` authorizes `owner` or `ROLE_MASTER` as independent principals, and `BaseDSContract::_authorizeUpgrade` is gated on it, so `owner` alone can replace the implementation behind any `BaseDSContract` proxy.

`BulkOperator` is a `BaseDSContract` deployed by the standard `deploy-all` flow and granted `ROLE_ISSUER` by `set-roles.ts`. Services are wired onto it by `set-services.ts`, but it is never registered on the token: there is no `dsToken.setDSService` call for it anywhere, and no service-id constant for it in `IDSServiceConsumer.sol` or the TypeScript registry.

`setup-governance` enumerates ownable targets by calling `dsToken.getDSService(serviceId)` over `OWNED_SERVICE_IDS`. With no id, `BulkOperator` is unreachable by that loop, and `verify-governance` iterates the same map.

**Impact:** After a fully successful handover that `verify-governance` reports as passing, the pre-handover key still owns a live proxy holding `ROLE_ISSUER`. Upgrading it does not change its address, so that key can install arbitrary code and exercise the proxy's issuance identity with no delay: `DSToken::burn` accepts an arbitrary holder and is authorized for `ROLE_ISSUER`, consumes no allowance, and passes through no timelock.

Distinct from issue 1, which concerns deprecated service ids omitted from `OWNED_SERVICE_IDS`. `BulkOperator` has no id in either registry, so a fix that adds the three deprecated ids will not cover it.

**Recommended Mitigation:** Assign `BulkOperator` a service id and register it on the token, or drive handover from an explicit deployment manifest rather than from the token's service registry. Add a post-handover assertion that no `BaseDSContract` in the deployment retains a non-timelock `owner`.

**Securitize:** Fixed in commit [eadeeab](https://github.com/securitize-io/dstoken/commit/eadeeab517275b746abc65e46f46649a1728da8b) by defining `BULK_OPERATOR` id then in commit [7c42b11](https://github.com/securitize-io/dstoken/commit/7c42b1190596e8632fc05742b157547236c3ecbf) `tasks/set-services.ts` now registers it via `dsToken.setDSService` so it can be found in the future by `setup-governance`.

**Cyfrin:** Verified; ideally it should also be set for existing deployments where it is currently being used.
