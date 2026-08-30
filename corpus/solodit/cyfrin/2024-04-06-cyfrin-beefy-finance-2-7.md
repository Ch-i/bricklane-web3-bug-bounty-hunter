---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Withdraw can return zero tokens while burning a positive amount of shares
vuln_class: []
---

# Withdraw can return zero tokens while burning a positive amount of shares

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Invariant fuzzing found an edge-case where a user could burn an amount of shares > 0 but receive zero output tokens. The cause appears to be a rounding down to zero precision loss for small `_shares` value in `BeefyVaultConcLiq::withdraw` [L220-221](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/vault/BeefyVaultConcLiq.sol#L220-L221):
```solidity
uint256 _amount0 = (_bal0 * _shares) / _totalSupply;
uint256 _amount1 = (_bal1 * _shares) / _totalSupply;
```

**Impact:** Protocol can enter a state where a user burns their shares but receives zero output tokens in return.

**Proof of Concept:** Invariant fuzz testing suite supplied at the conclusion of the audit.

**Recommended Mitigation:** Change the slippage check to also revert if no output tokens are returned:
```solidity
if (_amount0 < _minAmount0 || _amount1 < _minAmount1 ||
   (_amount0 == 0 && _amount1 == 0)) revert TooMuchSlippage();
```

**Beefy:**
Fixed in commit [04acaee](https://github.com/beefyfinance/experiments/commit/04acaeecca9a69f0cc1399dac68da21fcf598f17).

**Cyfrin:** Verified.
