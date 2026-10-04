---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[L-01] Claims fail when different Token program is used for fees and claimable
  tokens'
vuln_class: []
---

# [L-01] Claims fail when different Token program is used for fees and claimable tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`collect_fee.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/fee-collector/src/instructions/collect_fee.rs#L97), [`claim.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/claim.rs#L335)

**Description:**

The claim instruction is used to make two token transfers:

- The claimable token to the recipient from the unlocker vault;
- The fee token from the recipient to the protocol fee-collector vault;

The problem is that in the claim instruction, those two transfers are handled by a single program account specified in the instruction context. If those two tokens are of two different kinds, i.e. Token and Token2022, then it will be impossible to claim the tokens as the transfer of the other token will fail due to an incorrect program applied in the CPI.

**Impact:** A certain token/fee-token combination won’t be possible if they are of two different types. The protocol owner can always adjust the fee-token to match the token in an already set up unlocker.

**Recommendation:** Provide two Token Program account inputs in the claim context definition. One for the distributed token and the other for the fee token. The CPI for the `collect_fee` should use the fee token program account.

**Status:** Fixed

**Update from TokenTable:** Added `fee_token_program` account to `claim()` and `claim_cancelled_actual_tokens()` which is used in the CPI to the fee collector program in [22e51755ffe9cf1ca3a3e1a5c56bef2d80a618aa](https://github.com/EthSign/tokentable-unlocker-solana/tree/22e51755ffe9cf1ca3a3e1a5c56bef2d80a618aa).
