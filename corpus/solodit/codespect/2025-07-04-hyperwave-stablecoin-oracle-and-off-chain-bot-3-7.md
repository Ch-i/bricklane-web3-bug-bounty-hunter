---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-7
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-08] Exponential calculations may suffer from precision loss'
vuln_class: []
---

# [I-08] Exponential calculations may suffer from precision loss

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/cea4d156cafd2d9a5757d21d85aaea1db81479d6/app/domain/boring_vault/service/boring_vault.py#L208)

**Description:**

When performing exponential calculations, if `token_contract` decimals is less than `base_token_contract` decimals, the exponent will become negative. Exponentiating 10 with a negative number will result in a value less than 1, and direct computation may lead to precision loss.

```python
def calc_withdrawable_rate_by_token(self, chain_id: str, token_address: str, exchange_rate_lower_bound: int) -> int:
    // ...
    return int(
        Decimal(exchange_rate_lower_bound)
        * Decimal(10 ** (token_contract.decimals() - base_token_contract.decimals()))
        / rate_vs_base
    )

def normalize_balances_by_oracle(self, chain_id: str, token_balances: Dict[str, Decimal]) -> Decimal:
    // ...
    total_assets += (
        balance * rate_vs_base * Decimal(10 ** (base_token_contract.decimals() - token_contract.decimals()))
    )

    return total_assets

def normalize_balances_by_rate_provider(self, chain_id: str, token_balances: Dict[str, Decimal]) -> Decimal:
    // ...
    total_assets += balance * Decimal(rate) / Decimal(10 ** (2 * decimals - base_token_contract.decimals()))

    return total_assets

def get_oracle_rate_vs_base_upper_bound(self, chain_id: str, token_address: str) -> Decimal:
    // ...
    rate_vs_base = max(
        Decimal(oracle_rate)
        / Decimal(base_token_oracle_rate)
        * Decimal(10 ** (base_token_oracle.decimals() - oracle.decimals())),
        Decimal(1),
    )
    logger.info(f"Oracle rate upper bound vs base for {token_contract.symbol()}: {rate_vs_base}")

    return rate_vs_base
```

**Impact:** Performing operations directly between a negative number and 10 may lead to some precision loss.

**Recommendation:** It is recommended to convert to `Decimal` before performing exponential calculations. For example, change the following statement:

```python
int(
    Decimal(exchange_rate_lower_bound)
    * Decimal(10 ** (token_contract.decimals() - base_token_contract.decimals()))
    / rate_vs_base
)
```

To the following:

```python
int(
    Decimal(exchange_rate_lower_bound)
    * (Decimal(10) ** Decimal(token_contract.decimals() - base_token_contract.decimals()))
    / rate_vs_base
)
```

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22).
