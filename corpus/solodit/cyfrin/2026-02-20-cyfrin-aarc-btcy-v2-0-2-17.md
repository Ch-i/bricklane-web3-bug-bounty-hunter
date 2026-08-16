---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-17
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Remove unused errors
vuln_class: []
---

# Remove unused errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Consider using or removing the following unused errors:

- `IIBTCYHub.sol#L331`:

	```solidity
	    error VaultNotWhitelisted();
	```

- `IIBTCYHub.sol#L340`

	```solidity
	    error PriceNotSet();
	```

- `IPricer.sol#L166`

	```solidity
	    error NoPricesSet();
	```

- `IPricer.sol#L169`

	```solidity
	    error PriceNotFound();
	```

**Aarc:** Fixed in commit [bc8d3db](https://github.com/aarc-xyz/btcy-contracts-main/commit/bc8d3db32f7e6454a5c0fa32203c4012f85e993f).

**Cyfrin:** Verified.
