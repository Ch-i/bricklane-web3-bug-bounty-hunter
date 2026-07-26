---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Emit event `SyncPriceFromOracle` when price is synced
vuln_class: []
---

# Emit event `SyncPriceFromOracle` when price is synced

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Event `SyncPriceFromOracle` is emitted with `latestPrice` as 0 even when the price has not been synced, which can lead to inaccurate offchain event tracking.

```solidity
// Get the latest price from the oracle with safety checks.
        (latestPrice,) = SafeOracle.safeOraclePrice(oracleAddress);

        // Effect: update the last synced price and timestamp if the latest price is greater than zero.
        if (latestPrice > 0) {
            _vaults[vaultId].lastSyncedPrice = latestPrice;
            _vaults[vaultId].lastSyncedAt = uint40(block.timestamp);
        }

        // Log the event.
        emit SyncPriceFromOracle(vaultId, oracleAddress, latestPrice, uint40(block.timestamp));
```

**Recommended Mitigation:** Consider emitting the event `SyncPriceFromOracle` inside the if block as follows:

```solidity
// Get the latest price from the oracle with safety checks.
        (latestPrice,) = SafeOracle.safeOraclePrice(oracleAddress);

        // Effect: update the last synced price and timestamp if the latest price is greater than zero.
        if (latestPrice > 0) {
            _vaults[vaultId].lastSyncedPrice = latestPrice;
            _vaults[vaultId].lastSyncedAt = uint40(block.timestamp);

            // Log the event.
            emit SyncPriceFromOracle(vaultId, oracleAddress, latestPrice, uint40(block.timestamp));
        }
```


**Sablier:** Fixed in [https://github.com/sablier-labs/lockup/pull/1420](https://github.com/sablier-labs/lockup/pull/1420).

**Cyfrin:** Verified.
