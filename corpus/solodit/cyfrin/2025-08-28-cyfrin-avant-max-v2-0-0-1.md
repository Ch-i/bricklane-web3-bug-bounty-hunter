---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Use multi-sig wallet for contract admin and owner
vuln_class: []
---

# Use multi-sig wallet for contract admin and owner

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** As part of the audit we were asked to investigate the on-chain state of the deployed contracts. Using Ethereum as the example:
* the primary deployer appears to be [0xA5Ab0683d4f4AD107766a9fc4dDd49B5a960e661](https://etherscan.io/address/0xA5Ab0683d4f4AD107766a9fc4dDd49B5a960e661)
* it has transferred ownership and admin to [0xD47777Cf34305Dec4F1095F164792C1A4AFB327e](https://etherscan.io/address/0xd47777cf34305dec4f1095f164792c1a4afb327e)

Both of these are [EOA addresses](https://academy.binance.com/en/glossary/externally-owned-account-eoa):
```
cast code 0xA5Ab0683d4f4AD107766a9fc4dDd49B5a960e661 --rpc-url $ETH_RPC_URL
cast code 0xD47777Cf34305Dec4F1095F164792C1A4AFB327e --rpc-url $ETH_RPC_URL
0x
0x
```

**Impact:** EOAs present significant security risks:
* Single point of failure (one compromised private key = total control)
* No ability to implement time delays, spending limits, or approval requirements
* No recovery mechanism if keys are lost
* Vulnerable to phishing, device compromise, or coercion

**Recommended Mitigation:** Transfer admin and ownership to a multi-signature wallet (e.g., Gnosis Safe) with:
* Minimum 3-of-5 or 2-of-3 threshold
* Time delays for critical operations
* Trusted Third-Party Entity who can veto/cancel time-locked admin actions
* Signers using hardware wallets
* Documented key management procedures

**Avant:**
Acknowledged; Avant intends to transfer contract ownership and admin privileges to EOAs within the ForDeFi custodian ecosystem used to hold the protocol’s funds. The MPC wallets associated with the RBAC structure provided by their platform function similarly to the suggested multisig configuration. Avant’s setup ensures that only a quorum of admin-level users will be allowed to perform admin contract calls.

\clearpage
