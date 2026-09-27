---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[M-03] Potential misreporting of vault balance'
vuln_class: []
---

# [M-03] Potential misreporting of vault balance

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`hypercore.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/shared/hyperliquid/hypercore.py)

**Description:**

The bot, when calculating the new exchange ratio, takes into account all balances across the ecosystem. One of these balances is the multi-sig balance held in the HLP vault, which is fetched via an API call and returned by the following function:

```python
def get_vault_equities(self, address: str) -> Dict[str, any]:
    request_data = {"type": "userVaultEquities", "user": address}
    equities = self.exchange.info.post("/info", request_data)
    if not equities or len(equities) == 0:
        return {
            "vaultAddress": base_config.hyperliquid.vault_address,
            "equity": "0",
            "lockedUntilTimestamp": 0,
        }
    return equities[0]
```

This function returns only the first element of the equities array. The array itself consists of dictionaries, each representing vault deposits associated with a given wallet.

Although the protocol team has stated that deposits will only be made to the HLP vault, a mistake (e.g., a deposit to a different vault) or an external actor depositing on someone else’s behalf (in the context of Hyperliquid’s closed system) could alter the content of the array. As a result, an incorrect vault balance may be returned, potentially skewing the accounting logic.

*Note: The CODESPECT team cannot confirm whether depositing on someone else’s behalf is possible. Based on the available documentation, this is not allowed or supported, which reduces the severity of the issue.*

**Impact:** Incorrect accounting of vault balances may lead to an inaccurate exchange ratio calculation, ultimately devaluing user shares.

**Recommendation:** Filter and return only the equity associated with the specific HLP vault address to ensure accurate balance reporting.

**Status:** Fixed

**Client response:** Fixed in [0179e8db97501b7b0f29d628ad6df1769432f3cd](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/0179e8db97501b7b0f29d628ad6df1769432f3cd).
