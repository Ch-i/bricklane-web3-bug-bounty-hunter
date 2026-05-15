---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-H-2 TXs can be executed by less than the minimum required signatures
vuln_class: []
---

# TRST-H-2 TXs can be executed by less than the minimum required signatures

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
In HatsSignerGateBase, `checkTransaction()` is the function called by the Gnosis safe to 
approve the transaction. Several checks are in place.
```solidity
        uint256 safeOwnerCount = safe.getOwners().length;
             if (safeOwnerCount < minThreshold) {
                 revert BelowMinThreshold(minThreshold, safeOwnerCount);
        }
```
```solidity
           uint256 validSigCount = countValidSignatures(txHash, signatures, signatures.length / 65);
        // revert if there aren't enough valid signatures
             if (validSigCount < safe.getThreshold()) {
              revert InvalidSigners();
                  }
 ```
The first check is that the number of owners registered on the safe is at least **minThreshold**. 
The second check is that the number of valid signatures (wearers of relevant hats) is not 
below the safe's threshold. However, it turns out these requirements are not sufficient. A 
possible situation is that there are plenty of owners registered, but currently most do not
wear a hat. `reconcileSignerCount()` could be called to reduce the safe's threshold to the 
current validSigCount, which can be below **minThreshold**. That would make both the first 
and second check succeed. However, **minThreshold** is defined to be the smallest number of 
signers that must come together to make a TX. The result is that a single signer could 
execute a TX on the safe, if the other signers are not wearers of hats (for example, their 
toggle has been temporarily set off in the case of multi-hat signer gate.

**Recommended Mitigation:**
Add another check in `checkTransaction()`, which states that **validSigCount >= minThreshold**.


**Team Response:**
Accepted.

**Mitigation review:**
Fixed
