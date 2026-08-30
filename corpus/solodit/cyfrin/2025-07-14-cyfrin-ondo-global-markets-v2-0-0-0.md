---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: '`guardian` missing `PAUSER_ROLE` grant in `onUSD` deployment'
vuln_class: []
---

# `guardian` missing `PAUSER_ROLE` grant in `onUSD` deployment

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** Deployment of the `onUSD` token is handled via the `onUSDFactory`, which sets up the token as an upgradeable proxy using the transparent proxy pattern (EIP-1967).

As documented in the contract comments, the `guardian` address is expected to be granted both the `DEFAULT_ADMIN_ROLE` and `PAUSER_ROLE`:

[globalMarkets/onUSDFactory.sol#L33-36](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSDFactory.sol#L33-L36)

```solidity
/**
...
 *         Following the above mentioned deployment, the address of the onUSD_Factory contract will:
 *         i) Grant the `DEFAULT_ADMIN_ROLE` & PAUSER_ROLE to the `guardian` address <<----------------
 *         ii) Revoke the `MINTER_ROLE`, `PAUSER_ROLE` & `DEFAULT_ADMIN_ROLE` from address(this).
 *         iii) Transfer ownership of the ProxyAdmin to that of the `guardian` address.
 */
```

However, in the actual deployment logic, only the `DEFAULT_ADMIN_ROLE` is granted to the `guardian`. The `PAUSER_ROLE` is omitted:

[globalMarkets/onUSDFactory.sol#L88](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/onUSDFactory.sol#L88)

```solidity
  function deployonUSD( ... ) external onlyGuardian returns (address, address, address) {
    ...

    // @audit `PAUSER_ROLE` not granted to guardian
>>  onusdProxied.grantRole(DEFAULT_ADMIN_ROLE, guardian);

    onusdProxied.revokeRole(MINTER_ROLE, address(this));
    onusdProxied.revokeRole(PAUSER_ROLE, address(this));
    onusdProxied.revokeRole(DEFAULT_ADMIN_ROLE, address(this));

    onusdProxyAdmin.transferOwnership(guardian);
    assert(onusdProxyAdmin.owner() == guardian);
    initialized = true;
    emit onUSDDeployed( ... );

    return ( ... );
  }
```

As a result, deployment completes without the `guardian` address having the `PAUSER_ROLE` in the `onUSD` token contract, contrary to the intended and documented behavior.


**Impact:** The `guardian` will not have the `PAUSER_ROLE` in the deployed `onUSD` token contract. This prevents them from pausing the token immediately after deployment, potentially limiting their ability to respond to emergencies or enforce compliance controls. However, since the guardian retains the `DEFAULT_ADMIN_ROLE`, they can manually grant themselves the `PAUSER_ROLE` later. Still, this deviates from the intended one-step initialization flow and introduces the risk of operational oversight.

**Recommended Mitigation:** Grant the `PAUSER_ROLE` to the `guardian` address immediately after assigning the `DEFAULT_ADMIN_ROLE`, to match both the contract’s intended behavior and its documentation:

```diff
  onusdProxied.initialize(name, ticker, complianceView);

  onusdProxied.grantRole(DEFAULT_ADMIN_ROLE, guardian);
+ onusdProxied.grantRole(PAUSER_ROLE, guardian);

  onusdProxied.revokeRole(MINTER_ROLE, address(this));
  onusdProxied.revokeRole(PAUSER_ROLE, address(this));
```

**Ondo:** Fixed in commit [`b13a651`](https://github.com/ondoprotocol/rwa-internal/pull/472/commits/b13a651ae927e972a5c1478080fbe37e85409071).  It's the comment that is incorrect here - we only want to grant the default admin role, as it is temporarily used by the deployment EOA to configure the contract properly. Once configured, the default admin is renounced. If the pauser was also granted to the EOA on deployment it would just require another call to renounce

**Cyfrin:** Verified. Comment removed.
