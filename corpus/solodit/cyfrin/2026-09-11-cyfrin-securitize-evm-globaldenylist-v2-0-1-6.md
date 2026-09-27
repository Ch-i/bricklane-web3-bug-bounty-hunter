---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-6
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`ComplianceService::validateSeize` screens the seize destination only for
  special-wallet status, so a globally denylisted special wallet can still receive
  seized tokens'
vuln_class: []
---

# `ComplianceService::validateSeize` screens the seize destination only for special-wallet status, so a globally denylisted special wallet can still receive seized tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `ComplianceService::validateSeize` gates the seize destination on a single requirement:

```solidity
function validateSeize(
    address _from,
    address _to,
    uint256 _value
) public virtual override onlyToken returns (bool) {
    require(getWalletManager().isIssuerSpecialWallet(_to), "Target wallet type error");

    return recordSeize(_from, _to, _value);
}
```

Notably `_to` is never checked against the global denylist, only that it is a special wallet. While very narrow it is theoretically possible that:
* a special wallet is sanctioned by OFAC
* seize is used to move funds to that special wallet, in breach of OFAC sanctions

**Recommended Mitigation:** Enforce that the `_to` address where seized funds are sent is not on the global denylist.

**Securitize:** Acknowledged; platform wallets are managed by the Operations team and are not expected to be affected by this scenario.

\clearpage
