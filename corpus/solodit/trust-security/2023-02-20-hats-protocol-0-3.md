---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-0-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-H-4 maxSigners can be bypassed
vuln_class: []
---

# TRST-H-4 maxSigners can be bypassed

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
**maxSigners** is specified when creating an HSG and is left constant. It is enforced in two ways 
**–targetThreshold** may never be set above it, and new signers cannot register to the HSG 
when the signer count reached **maxSigners**. Below is the implementation code in 
HatsSignerGate.
```solidity
        function claimSigner() public virtual {
             if (signerCount == maxSigners) {
                revert MaxSignersReached();
        }
        if (safe.isOwner(msg.sender)) {
                revert SignerAlreadyClaimed(msg.sender);
            }
        if (!isValidSigner(msg.sender)) {
             revert NotSignerHatWearer(msg.sender);
         }
         _grantSigner(msg.sender);
           }
```
An issue that arises is that this doesn't actually limit the number of registered signers. 
Indeed, **signerCount** is a variable that can fluctuate when wearers lose eligibility or a hat is 
inactive. At this point, `reconcileSignerCount()` can be called to update the signerCount to the 
current valid wearer count. A simple attack which achieves unlimited claims is as follows:
1. Assume **maxSigners** = 10
2. 10 signers claim their spot, so **signerCount** is maxed out
3. A signer misbehaves, loses eligibility and the hat. 
4. reconcile() is called, so **signerCount** is updated to 9
5. A new signer claims, making **signerCount** = 10
6. The malicious signer behaves nicely and regains the hat.
7. reconcile() is called again, making **signerCount** = 11
8. At this point, any eligible hat wearer can claim their hat, easily overrunning the 
**maxSigners** restriction.

**Recommended Mitigation:**
The root cause is that users which registered but lose their hat are still stored in the safe's 
owners array, meaning they can always get re-introduced and bump the **signerCount**.
Instead of checking the **signerCount**, a better idea would be to compare with the list of 
owners saved on the safe. If there are owners that are no longer holders, `removeSigner()` can 
be called to vacate space for new signers.

**Team response:**
Accepted; added a `swapSigner()` flow to `claimSigner()`.

**Mitigation review:**
Fixed but introduced a new issue. The new code will swap the new signer with an invalid old 
signer.
```solidity
    address[] memory owners = safe.getOwners();
         uint256 ownerCount = owners.length;
    if (ownerCount >= maxSigs) {
        _swapSigner(owners, ownerCount, maxSigs, currentSignerCount, msg.sender);
    } else {
        _grantSigner(owners, currentSignerCount, msg.sender);
        }
```
However, it's possible that all current owners are valid signers, in this case `_swapSigner()` will 
complete the loop and return gracefully. A user will think they have claimed signer 
successfully, but nothing has changed.
