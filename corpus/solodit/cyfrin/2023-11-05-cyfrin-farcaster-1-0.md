---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: Inconsistent validation of `vaultAddr`
vuln_class: []
---

# Inconsistent validation of `vaultAddr`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

In `KeyManager.setVault()` and `StorageRegistry.setVault()`, there is a validation for address(0) but we don't check in the constructors.

```solidity
File: audit-farcaster\src\KeyManager.sol
123:         vault = _initialVault;
124:         emit SetVault(address(0), _initialVault);
...
211:     function setVault(address vaultAddr) external onlyOwner {
212:         if (vaultAddr == address(0)) revert InvalidAddress();
213:         emit SetVault(vault, vaultAddr);
214:         vault = vaultAddr;
215:     }
216:
```

**Client:**
After internal discussion, we’ve decided to remove payments from the `KeyGateway` altogether and rely on per-fid limits in the `KeyRegistry` for now. We’re keeping the gateway pattern in place, which gives us the ability to introduce a payment in the future if it becomes necessary.

We don't intend to redeploy the StorageRegistry with this deployment, but we will add this validation in the next version of the storage contract.

Commit: [`11e2722`](https://github.com/farcasterxyz/farcaster-contracts-private/commit/11e27223625e4c6b5f929398e015ccda740c1593)

**Cyfrin:** Acknowledged.
