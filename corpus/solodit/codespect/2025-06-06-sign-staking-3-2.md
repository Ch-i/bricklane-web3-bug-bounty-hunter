---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-3-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[I-03] Lack of guardrails on key protocol parameter values'
vuln_class: []
---

# [I-03] Lack of guardrails on key protocol parameter values

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Original severity:** Best Practices

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol#L158)

**Description:**

The protocol allows for setting various parameters defining the staking assets, unstaking rules and interest calculations. The following struct defines the controllable parameters:

```solidity
struct SignStakingStorage {
    IERC20 signToken;
    IERC721 nftContract;
    uint256 standardAPY;
    uint256 boostedAPY;
    uint256 cooldownPeriod;
    /// [...]
}
```

They can be set by a collection of `set` functions guarded by `onlyOwner` modifier. However the protocol lacks safeguards against setting of incorrect values that will damage user experience or endanger the reserve which is used for interest payments. Specifically:

- `setSignToken(...)` and `setNFTContract(...)` could change the token and NFT once users are already staked and hence block unstaking functions;
- `setStandardAPY(...)` and `setBoostedAPY(...)` can be set too high and hence contribute to faster than expected reserve depletion;
- `setCooldownPeriod(...)` could set the cooldown period to unreasonably large value and prevent users from unstaking;

**Impact:** Hampered user experience or reserve depletion.

**Recommendation:** Set limits on the APR values. Block changing of token and NFT addresses after first user stake. Limit maximum value of the cooldown period.

**Status:** Acknowledged

**Update from TokenTable:** Acknowledged
