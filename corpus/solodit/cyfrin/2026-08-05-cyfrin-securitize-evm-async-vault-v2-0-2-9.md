---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-9
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Zero live NAV bypasses settlement price validation
vuln_class: []
---

# Zero live NAV bypasses settlement price validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::_checkNavPrice` skips validation when the normalized live NAV is zero:

```solidity
uint256 live =
    $.navProvider.rate() * WAD
        / (10 ** uint256($.dsDecimals));

if (live == 0) return;
```

The settler can consequently fulfill deposits or redemptions using any nonzero `navPriceWAD`, bypassing the configured tolerance.

**Impact:** An incorrect settlement price can cause depositors to receive the wrong number of DS Tokens or redeemers to receive the wrong liquidity amount, resulting in irreversible accounting losses.

**Recommended Mitigation:** Revert when the live NAV is zero:

```solidity
if (live == 0) revert InvalidLiveNavPrice();
```

Settlement should resume only after the NAV provider returns a valid price.

**Securitize:** Fixed in commit [5ad7619](https://github.com/securitize-io/bc-async-ramp-sc/commit/5ad7619fdd28190302579d905edd75ae8d2b08ca).

**Cyfrin:** Verified.
