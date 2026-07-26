---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_XLayer_Asset_Oracle::fetchPrice` reverts on every price while `PRICE_THRESHOLD`
  is left at its default `0`'
vuln_class: []
---

# `STBL_XLayer_Asset_Oracle::fetchPrice` reverts on every price while `PRICE_THRESHOLD` is left at its default `0`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_XLayer_Asset_Oracle::fetchPrice` rejects a price as stale when `time + PRICE_THRESHOLD <= block.timestamp`:

```solidity
function fetchPrice() external view returns (uint256) {
    if (!Enabled) revert STBL_Asset_OracleDisabled();
    (uint256 price, uint256 time) = oracle.getPriceData();
    if (time + PRICE_THRESHOLD <= block.timestamp)
        revert STBL_Asset_OracleStalePrice(price, time);
    return price;
}
```

`PRICE_THRESHOLD` is a plain `uint256` storage variable with no value assigned in the constructor, so it defaults to `0`. With `PRICE_THRESHOLD == 0` the staleness condition collapses to `time <= block.timestamp`, which holds for any price whose `time` is the current block or earlier. A price would pass only if `time > block.timestamp`, which is not reachable. Every call to `fetchPrice` therefore reverts with `STBL_Asset_OracleStalePrice` until an admin calls `setPriceThreshold` with a non-zero value.

`fetchPrice` is reached through `STBL_XLayer_Asset_Issuer::deriveAssetValue`, which `STBL_ESS_Wrapper1::iCalculateRatios` calls inside `ess_deposit`. While the threshold is `0`, every deposit reverts.

No deploy automation sets the threshold. The Hardhat deploy tasks (`stbl-contracts-evm-ess-common/scripts/tasks/deploy/`) deploy and wire only the Token, Wrapper, and NFT Vault, and resolve asset oracle addresses from the external `stbl-contracts-evm-asset-type1` deployment. No script deploys `STBL_XLayer_Asset_Oracle` or calls `setPriceThreshold`, and the constructor sets no default, so a deployer that uses this oracle must call `setPriceThreshold` manually before any deposit can succeed.

The condition is fully recoverable. The admin holds `DEFAULT_ADMIN_ROLE` and can call `setPriceThreshold` at any time to set a sane staleness window. The fault would also surface immediately on the first deposit attempt after deployment. This is a missing-default / deployment-configuration issue, not a permanent or unrecoverable defect.

**Impact:** If the oracle is deployed and the threshold setter is not called, all `ess_deposit` calls revert until the admin sets `PRICE_THRESHOLD`. No funds are lost and the condition is corrected by a single admin transaction. Low.

**Recommended Mitigation:** Initialize `PRICE_THRESHOLD` to a sensible default in the constructor, or revert in `fetchPrice` when `PRICE_THRESHOLD == 0` so the misconfiguration produces an explicit error instead of an unconditional stale-price revert:

```solidity
constructor(address _oracleAddr) AccessControl() {
    _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
    oracle = IRWAOracle(_oracleAddr);
    Enabled = true;
    PRICE_THRESHOLD = 1 hours; // sane default
}
```

**STBL:** Fixed in commit [47dec45](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/47dec45bb6dda51a195d1a1bdf685d29a82f5fc3).

**Cyfrin:** Verified. `STBL_XLayer_Asset_Oracle` constructor now accepts a `_priceThreshold` parameter and assigns it to `PRICE_THRESHOLD` at deployment, eliminating the silent 0 default
