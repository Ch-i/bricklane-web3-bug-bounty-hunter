---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Lack of Governance action to update registered emitters
vuln_class: []
---

# Lack of Governance action to update registered emitters

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

**Description:** The Wormhole CCTP integration contract currently exposes a function [`Governance::registerEmitterAndDomain`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Governance.sol#L48-L84) to register an emitter address and its corresponding CCTP domain on the given foreign chain; however, no such function currently exists to update this state. Any mistake made when registering the emitter and CCTP domain is irreversible unless an upgrade is performed on the entirety of the integration contract itself. Deployment of protocol upgrades comes with its own risks and should not be performed as a necessary fix for trivial human errors. Having a separate governance action to update the emitter address, foreign chain identifier, and CCTP domain is a preferable pre-emptive measure against any potential human errors.

```solidity
function registerEmitterAndDomain(bytes memory encodedVaa) public {
    /* snip: parsing of Governance VAA payload */

    // Set the registeredEmitters state variable.
    registeredEmitters[foreignChain] = foreignAddress;

    // update the chainId to domain (and domain to chainId) mappings
    getChainToDomain()[foreignChain] = cctpDomain;
    getDomainToChain()[cctpDomain] = foreignChain;
}
```

**Impact:** In the event an emitter is registered with an incorrect foreign chain identifier or CCTP domain, then a protocol upgrade will be required to mitigate this issue. As such, the risks associated with the deployment of protocol upgrades and the potential time-sensitive nature of this issue designate a low severity issue.

**Proof of Concept:**
1. A Governance VAA erroneously registers an emitter with the incorrect foreign chain identifier.
2. A Governance upgrade is now required to re-initialize this state so that the correct foreign chain identifier can be associated with the given emitter address.

**Recommended Mitigation:** The addition of a `Governance::updateEmitterAndDomain` function is recommended to allow Governance to more easily respond to any issues with the registered emitter state.

**Wormhole Foundation:** Allowing existing emitters to be updated comes with similar impacts of admin mistakes. But allowing updates is indeed easier than coordinating a whole contract upgrade. However we won’t change this since we can’t easily enforce that governance messages to perform these updates are played in sequence.

**Cyfrin:** Acknowledged.

\clearpage
