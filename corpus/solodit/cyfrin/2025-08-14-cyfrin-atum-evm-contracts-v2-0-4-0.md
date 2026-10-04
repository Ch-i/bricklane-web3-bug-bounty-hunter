---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-4-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Fail fast by reverting from inputs prior to storage reads
vuln_class: []
---

# Fail fast by reverting from inputs prior to storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** Storage reads are expensive so if a function is going to revert, it is better to fail fast by reverting from inputs prior to doing unnecessary storage reads:
* `Escrow::reserve` - perform these checks at the top of the function before storage reads:
```solidity
142:        require(witness.settler != address(0), Escrow_SettlerCannotBeZeroAddress());
148:        require(block.timestamp <= witness.deadline, Escrow_SignatureExpired(witness.deadline, block.timestamp));
```

* `Escrow::refund` - perform these checks at the top of the function before storage reads:
```solidity
224:        require(block.timestamp <= witness.deadline, Escrow_SignatureExpired(witness.deadline, block.timestamp));
```

**Atum:**
Fixed in commit [6726871](https://github.com/Atum-Labs/evm-contracts/commit/672687134c9a65cba4c9eb1528c499e80bc80a49).

**Cyfrin:** Verified.
