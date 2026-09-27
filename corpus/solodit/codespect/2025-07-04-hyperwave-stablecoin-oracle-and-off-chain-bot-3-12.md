---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-12
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
title: '[I-13] Consider applying parameter validation'
vuln_class: []
---

# [I-13] Consider applying parameter validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Original severity:** Best Practices

**Files:** [`atomic_queue.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/contract/atomic_queue.py#L20)

**Description:**

The function lacks proper input validation and error handling for blockchain interactions. Specifically, `request.offer` and `request.user_address` are passed to the smart contract without verifying they are valid checksummed Ethereum addresses.

**Impact:** Invalid address formats may cause contract calls to fail.

**Recommendation:** Implement address validation using `Web3.is_checksum_address()` for both `request.offer` and `request.user_address` before contract interaction.

**Status:** Fixed

**Client response:** Fixed in [7b5fd1148af2fc90b76af58918300968a668eab2](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/7b5fd1148af2fc90b76af58918300968a668eab2).
