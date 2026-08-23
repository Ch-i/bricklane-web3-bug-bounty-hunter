---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_XLayer_Asset_Oracle::PRICE_DECIMALS` defaults to `0` and silently corrupts
  every price conversion until an admin calls `setPriceDecimals`'
vuln_class: []
---

# `STBL_XLayer_Asset_Oracle::PRICE_DECIMALS` defaults to `0` and silently corrupts every price conversion until an admin calls `setPriceDecimals`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_XLayer_Asset_Oracle` declares `PRICE_DECIMALS` as a storage variable and the constructor never initialises it. The only writer is `setPriceDecimals`, gated by `DEFAULT_ADMIN_ROLE`, and `getPriceDecimals` simply returns the slot:

```solidity
uint256 public PRICE_DECIMALS;

constructor(address _oracleAddr) AccessControl() {
    _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
    oracle = IRWAOracle(_oracleAddr);
    Enabled = true;
}
```

`STBL_OracleLib` consumes the slot in both directions:

```solidity
forwardPrice = ((oracle.fetchPrice() * amount) / (10 ** oracle.getPriceDecimals()));
inversePrice = (amount * (10 ** oracle.getPriceDecimals())) / oracle.fetchPrice();
```

With `PRICE_DECIMALS == 0`, `10 ** 0 == 1`, so `forwardPrice = fetchPrice() * amount` (inflated by `10^expected_decimals`) and `inversePrice = amount / fetchPrice()` (collapsed by the same factor). The conversion does not revert and produces no on-chain signal; every downstream call (`depositERC20`, `withdrawERC20`, `generateMetaData`, `deriveAssetValue`, yield differential) consumes the corrupted value silently.

**Impact:** If `setPriceDecimals` is forgotten at deploy, every deposit and withdraw silently executes with conversion math off by `10^expected_decimals`, so ESS supply grows against negligible asset backing and depositors lose nearly all of their value in a single round trip before any operator notices.

**Recommended Mitigation:** Initialize `PRICE_DECIMALS` in the constructor and guard `fetchPrice` so a zero value reverts loudly:

```solidity
constructor(address _oracleAddr, uint256 _priceDecimals) AccessControl() {
    if (_priceDecimals == 0) revert STBL_Asset_InvalidPriceDecimals();
    _grantRole(DEFAULT_ADMIN_ROLE, _msgSender());
    oracle = IRWAOracle(_oracleAddr);
    PRICE_DECIMALS = _priceDecimals;
    Enabled = true;
}
```

Apply the same shape to `PRICE_THRESHOLD` so neither config slot can be left at its zero default.

**STBL:** **Cyfrin:**
