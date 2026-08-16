---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-15-cyfrin-story-ip-derivative-agent-v2-1-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md
tags:
- firm:cyfrin
- report:2026-01-15-cyfrin-story-ip-derivative-agent-v2-1
title: '`IPDerivativeAgent` only supports single parent IP, limiting `Multi-Parent
  Derivative` use cases'
vuln_class: []
---

# `IPDerivativeAgent` only supports single parent IP, limiting `Multi-Parent Derivative` use cases

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md)_

---

**Description:** The `IPDerivativeAgent::registerDerivativeViaAgent` is hardcoded to support only a single parent IP by constructing fixed-length(`1`) arrays for `parentIpIds` and `licenseTermsIds`.

```solidity
        // Prepare arrays for LicensingModule call (single parent)
        address[] memory parents = new address[](1);
        parents[0] = parentIpId;
        uint256[] memory licenseTermsIds = new uint256[](1);
        licenseTermsIds[0] = licenseTermsId;
```

However, the underlying `LicensingModule::registerDerivative` explicitly supports registering derivatives with multiple parent IPs.

```solidity
    function registerDerivative(
        address childIpId,
        address[] calldata parentIpIds,
        uint256[] calldata licenseTermsIds,
```

According to the protocol [documentation](https://docs.story.foundation/concepts/licensing-module/license-token#registering-a-derivative), an IP Asset can only register as a derivative once. If it has multiple parents, all parent IPs must be registered atomically in the same call, and once registered, no additional parents can be linked later.
> An IP Asset can only register as a derivative one time. If an IP Asset has multiple parents, it must register both at the same time.
> Once an IP Asset is a derivative, it cannot link any more parents.

Given this constraint, the agent’s single-parent design is not a recoverable limitation. Instead, it permanently prevents registering any multi-parent derivative through `IPDerivativeAgent`, even though such derivatives are explicitly supported at the core protocol level.

As a result, the agent abstraction introduces an implicit and restriction that materially diverges from the capabilities and guarantees of `LicensingModule`.

This single-parent assumption also propagates to:
- Fee estimation via `predictMintingLicenseFee()`, which only accepts a single parent IP, preventing accurate fee prediction for multi-parent derivatives.
- The whitelist mechanism, which is keyed by a single `parentIpId`, making it impossible to express authorization rules for combinations of multiple parent IPs.

**Impact:** This limits the agent’s applicability for cross-parent derivative use cases.

**Recommended Mitigation:**
- If multi-parent derivatives are intended to be supported via the agent, extend `IPDerivativeAgent` to accept arrays of parent IPs and license terms, and update fee prediction and whitelist logic accordingly.

- If single-parent support is an intentional design decision, explicitly document this limitation and clarify that multi-parent derivatives are not supported and must be registered directly through `LicensingModule`.

**Story:** Acknowledged.
