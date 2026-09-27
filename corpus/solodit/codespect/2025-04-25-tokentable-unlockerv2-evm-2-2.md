---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-2-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[I-03] Implementation of CustomERC2771Context based on the vulnerable version
  of OZ contract'
vuln_class: []
---

# [I-03] Implementation of CustomERC2771Context based on the vulnerable version of OZ contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [CustomERC2771Context.sol](https://github.com/EthSign/tokentable-v2-evm/blob/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/libraries/CustomERC2771Context.sol)

**Description:**

`ERC2771/*.sol` extensions inherit from `CustomERC2771Context.sol`, which facilitates gasless transaction execution. This abstract contract is based on OpenZeppelin’s `ERC2771Context` implementation, version 4.7.0.

However, this version of the OpenZeppelin contract contains a known issue disclosed in the following security advisory: [[ref]](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-g4vp-m682-qqmp). As cited: *“Contracts using ERC2771Context along with a custom trusted forwarder may see `_msgSender` return `address(0)` in calls that originate from the forwarder with calldata shorter than 20 bytes.”*

To prevent this, the contract should be updated to align with the latest OpenZeppelin implementation, which addresses this issue.

**Impact:** If a custom trusted forwarder is used and a transaction includes calldata shorter than 20 bytes, `_msgSender()` will return `address(0)`. This can lead to unexpected behaviour.

**Recommendation:** Upgrade `CustomERC2771Context.sol` to reflect the latest secure implementation provided by OpenZeppelin.

**Status:** Fixed

**Update from TokenTable:** Fixed in [5faa20f8fe1c7937ff72b00bb3579d39980a792b](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/5faa20f8fe1c7937ff72b00bb3579d39980a792b)
