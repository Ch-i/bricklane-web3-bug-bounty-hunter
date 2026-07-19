---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Operator Swap Signatures Are Replayable and Not Bound to a Specific On‑Ramp
  or Mints
vuln_class: []
---

# Operator Swap Signatures Are Replayable and Not Bound to a Specific On‑Ramp or Mints

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The operator swap signature payload (`SwapSplTokenMessage`) lacks a nonce and does not include identifiers for `on_ramp_state`, `asset_mint`, or `liquidity_mint`. As a result, a valid signature can be replayed within its deadline and reused across on‑ramp instances. Because operators are trusted, this is categorized as low severity, but it still expands the blast radius if an operator key or signed payload is reused or leaked.
```rust
pub fn validate_investor_signature<'info>(
    ixs_account: &AccountInfo<'info>,
    expected_message: SwapSplTokenMessage,
) -> Result<()> {
    let ix_account = sysvar_instructions::get_instruction_relative(-1, ixs_account)?;

    require_gte!(
        expected_message.deadline,
        Clock::get()?.unix_timestamp,
        SecuritizeOnRampError::ExpiredSignature
    );

    utils::ed25519::validate_ed25519_ix(&ix_account)?;

    let ix_data = &ix_account.data;
    let public_key_bytes = &ix_data[16..48];

    require!(
        Pubkey::new_from_array(public_key_bytes.try_into().unwrap())
            == expected_message.investor_wallet,
        SecuritizeOnRampError::InvalidEd25519Instruction
    );

    let actual_message_hash = &ix_data[112..];

    let expected_message_bytes = expected_message.try_to_vec()?;
    let pid = crate::ID;
    let expected_message_hash =
        hashv(&[SWAP_SPL_TOKEN_TAG, pid.as_ref(), &expected_message_bytes]).to_bytes();

    require!(
        actual_message_hash == expected_message_hash,
        SecuritizeOnRampError::InvalidEd25519Instruction
    );

    Ok(())
}
```


**Impact:** Replay or cross‑on‑ramp reuse is possible, but exploitation requires a trusted operator to submit the transaction.

**Recommended Mitigation:** Include on_ramp_state, asset_mint, and liquidity_mint in the signed message and add a per‑investor nonce (stored and consumed on‑chain). This preserves trust assumptions while preventing replay across transactions or on‑ramp instances.

**Securitize:** Acknowledged, the nonce is not included to resemble the EVM version.
