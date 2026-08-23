---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: A given CCTP domain can be registered for multiple foreign chains due to insufficient
  validation in `Governance::registerEmitterAndDomain`
vuln_class: []
---

# A given CCTP domain can be registered for multiple foreign chains due to insufficient validation in `Governance::registerEmitterAndDomain`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

**Description:** [`Governance::registerEmitterAndDomain`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Governance.sol#L48-L84) is a Governance action that is used to register the emitter address and corresponding CCTP domain for a given foreign chain. Validation is currently performed to ensure that the registered CCTP domain of the foreign chain is not equal to that of the local chain; however, there is no such check to ensure that the given CCTP domain has not already been registered for a different foreign chain. In this case, where the CCTP domain of an existing foreign chain is mistakenly used in the registration of a new foreign chain, the [`getDomainToChain`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Governance.sol#L83) mapping of an existing CCTP domain will be overwritten to the most recently registered foreign chain. Given the validation that prevents foreign chains from being registered again, without a method for updating an already registered emitter, it will not be possible to correct this corruption of state.

```solidity
function registerEmitterAndDomain(bytes memory encodedVaa) public {
    /* snip: parsing of Governance VAA payload */

    // For now, ensure that we cannot register the same foreign chain again.
    require(registeredEmitters[foreignChain] == 0, "chain already registered");

    /* snip: additional parsing of Governance VAA payload */

    // Set the registeredEmitters state variable.
    registeredEmitters[foreignChain] = foreignAddress;

    // update the chainId to domain (and domain to chainId) mappings
    getChainToDomain()[foreignChain] = cctpDomain;
    getDomainToChain()[cctpDomain] = foreignChain;
}
```

**Impact:** The impact of this issue in the current scope is limited since the corrupted state is only ever queried in a public view function; however, if it is important for third-party integrators, then this has the potential to cause downstream issues.

**Proof of Concept:**
1. CCTP Domain A is registered for foreign chain identifier X.
2. CCTP Domain A is again registered, this time for foreign chain identifier Y.
3. The `getDomainToChain` mapping for CCTP Domain A now points to foreign chain identifier Y, while the `getChainToDomain` mapping for both X and Y now points to CCTP domain A.

**Recommended Mitigation:** Consider adding the following validation when registering a CCTP domain for a foreign chain:

```diff
+ require (getDomainToChain()[cctpDomain] == 0, "CCTP domain already registered for a different foreign chain");
```

**Wormhole Foundation:** We are comfortable that governance messages are sufficiently validated before being signed by the guardians and submitted on-chain.

**Cyfrin:** Acknowledged.
