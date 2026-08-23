---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_ESS_Wrapper1` exposes no call paths to `WithdrawExpired`, `distributeYield`,
  or `WithdrawFees` — three isWrapper-gated admin functions are permanently unreachable,
  freezing expired LT assets, blocking yield distribution, and stranding'
vuln_class: []
---

# `STBL_ESS_Wrapper1` exposes no call paths to `WithdrawExpired`, `distributeYield`, or `WithdrawFees` — three isWrapper-gated admin functions are permanently unreachable, freezing expired LT assets, blocking yield distribution, and stranding protocol fees

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** Three administrative functions across `STBL_XLayer_Asset_Issuer` and `STBL_XLayer_Asset_Vault` are gated by the `isWrapper` modifier, meaning only the authorized wrapper contract may call them:

- `STBL_XLayer_Asset_Issuer:WithdrawExpired` — reclaims expired lock-time assets to the treasury
- `STBL_XLayer_Asset_Vault:distributeYield` — distributes RWA price-appreciation yield to NFT holders
- `STBL_XLayer_Asset_Vault:WithdrawFees` — sweeps accumulated protocol fees to the treasury

Neither the abstract `STBL_ESS_Wrapper1` nor the concrete `STBL_XLayer_Wrapper` contains any function that calls any of these on the issuer or vault. Any direct call by an external account is blocked by `isWrapper` since no external caller is the wrapper. There is no reachable call path to any of the three functions.

**`WithdrawExpired` permanently blocked — expired LT assets are frozen in the vault.**

`STBL_XLayer_Asset_Issuer.WithdrawExpired` is the only path through which lock-time (`AssetType.LT`) positions can be reclaimed once their lock duration has elapsed. After a lock-time asset expires, the normal `withdraw` path is blocked by the issuer (it reverts on expired assets), and `WithdrawExpired` is unreachable. The expired YLD NFTs remain in the ESS NFT Vault indefinitely. The underlying assets are permanently inaccessible to both the original depositors and the protocol treasury without a contract upgrade. Any `AssetType.LT` deposit whose lock duration has elapsed is affected.

**`distributeYield` permanently blocked — yield from asset appreciation is never distributed to NFT holders.**

`iDistributeYield` calculates the USD price differential between the asset's current oracle price and its recorded deposit baseline, splits the gain into a yield portion and a protocol fee, approves the reward distributor for the yield amount, and calls `distributeReward` to push it to the yield distributor. With this path broken, any appreciation in the underlying RWA asset price never reaches the yield distributor. NFT holders entitled to yield from asset price appreciation receive nothing, regardless of how much value the underlying asset accrues. The yield accumulates silently inside the vault and is permanently inaccessible.

**`WithdrawFees` permanently blocked — all accumulated protocol fees are locked in the vault.**

`iWithdrawFees` aggregates all fee buckets tracked in `VaultData` — deposit fees, withdrawal fees, yield fees, and insurance fees — and transfers the total to the protocol treasury. With this path broken, every fee collected since deployment accumulates in the vault and can never be retrieved by the treasury. The longer the vault operates, the larger the stranded balance grows.

Each function's access gate is identical in structure:

```solidity
// STBL_XLayer_Asset_Issuer.sol:34-37, 114-116
modifier isWrapper() {
    if (msg.sender != wrapper) revert STBL_UnauthorizedCaller();
    _;
}

function WithdrawExpired(uint256 _tokenID) external isWrapper {
    withdrawExpired(_tokenID);
}

// STBL_XLayer_Asset_Vault.sol:94-107
function distributeYield() external isWrapper {
    iDistributeYield();
}

function WithdrawFees() external isWrapper {
    iWithdrawFees();
}
```

**Recommended Mitigation:** Add pass-through functions to `STBL_ESS_Wrapper1` (or the concrete wrapper) for each missing operation, gated by an appropriate access-control check (e.g., `REGISTER_ROLE`):

- A `WithdrawExpired` pass-through that calls the issuer's `WithdrawExpired`; also add `WithdrawExpired` to the `iSTBL_Issuer` interface.
- A `distributeYield` pass-through that iterates over all configured asset vaults and calls `distributeYield` on each via a vault interface.
- A `WithdrawFees` pass-through that similarly calls `WithdrawFees` on each configured vault.

All three should be exposed through their respective interfaces so the wrapper can dispatch them correctly.


**STBL:** Fixed in commit [afc1f16](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/afc1f164f3b3ffcb06e0eff5f84cb9bfa3098173).

**Cyfrin:** Verified. `distributeYield` and `withdrawFees` as external pass-through functions on `STBL_XLayer_Wrapper`, delegating to internal helpers that iterate all configured asset vaults and call the corresponding isWrapper-gated functions on each. `WithdrawExpired`, is not applicable in this deployment because the system exclusively uses PT asset types.
