---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Malicious user holding `HilBTC` tokens can front run blacklisted transaction
vuln_class: []
---

# Malicious user holding `HilBTC` tokens can front run blacklisted transaction

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** When the `blacklister` attempts to blacklist a malicious user holding `HilBTC` tokens, the maliciois user can monitor the memepool and  front-run the blacklist tx by quickly redeeming their `HilBTC` tokens through the `minter` contract before the blacklist takes effect. Once redeemed, the user successfully exits their position with the underlying assets, completely bypassing the intended blacklist enforcement mechanism.

```solidity
function redeem(
        uint256 amount
    ) external onlyWhitelisted(msg.sender) nonReentrant {
        hilBTCToken.burnFrom(msg.sender, amount);
        baseAsset.safeTransfer(msg.sender, amount);
        totalDeposits -= amount;
        emit Redeemed(msg.sender, amount);
    }

```

Note that this could not happen in the `StakingVault.sol`

**Impact:** Blacklist can be avoided if  a malicious user front run the blacklisted call

**Proof of Concept:** **Recommended Mitigation:**

Consider add a cooldown also in the `redeem` function of the minter

**Syntetika:**
Acknowledged; this is generally the case with all blacklisting mechanisms. Protocols can perform these transactions via [services](https://docs.flashbots.net/flashbots-protect/overview) which prevent front-running.

We don't think it is worth adding extra complexity to the code to deal with this issue, we'll just use a service for running blacklist txns through if this is a real concern. In practice this "attack vector" is pretty much never an issue; I'm not aware of a single instance where this attack has occurred.
