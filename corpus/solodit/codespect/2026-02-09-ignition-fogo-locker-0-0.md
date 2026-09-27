---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-09-ignition-fogo-locker-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md
tags:
- firm:codespect
- report:2026-02-09-ignition-fogo-locker
title: '[L-01] Extra guardrails in case compromised session key for create_vesting_escrow_with_session'
vuln_class: []
---

# [L-01] Extra guardrails in case compromised session key for create_vesting_escrow_with_session

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-09-Ignition-Fogo-Locker.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-09-Ignition-Fogo-Locker.md)_

---

**Files:** [`create_vesting_escrow_with_session.rs`](https://github.com/Tempest-Finance/fogo-locker/blob/c405ebd242141dafbed8476ebe9dc987de9695ab/programs/locker/src/instructions/escrow_instructions/create_vesting_escrow_with_session.rs#L47)

**Description:**

The `create_vesting_escrow_with_sessions` instruction allows creation of an escrow using the Fogo session mechanism, where such a session has permissions to transfer the required token to the escrow's account. While this mechanism is secure as long as the session key is not compromised, it is recommended to add an extra guardrails in case that happens. In case the session key gets compromised a malicious user can create the escrow on the user's behalf and put himself as `recipient` of the escrow's vested token and effectively taking them from the user.

**Impact:** Possible to bypass session token usage limitations in case of session's key compromise.

**Recommendation:** To prevent such a scenario we recommend to use the session intent's `extra` field to store the `recipient` address (or potentially a set of possible addresses, depending on the use case). This `extra` field's contents could then be obtained from the session account and used to validate provided `recipient` address.

**Status:** Fixed

**Client response:** Fixed. Added `recipient == session_user` validation in `create_vesting_escrow_with_session`. The session account already contains the user's pubkey, so no extra field is needed. This prevents a compromised session key from creating escrows with an attacker-controlled recipient. The non-session instruction (`create_vesting_escrow_v2`) intentionally allows arbitrary recipients since it requires a direct wallet signature. [484c05d6c82c85fc3977060150f0a4307d2ea1de](https://github.com/Tempest-Finance/fogo-locker/pull/1/changes/484c05d6c82c85fc3977060150f0a4307d2ea1de)

**CODESPECT fix review:** This is fixed correctly too.
