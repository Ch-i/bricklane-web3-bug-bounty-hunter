---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-0-2
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
title: TRST-H-3 Target signature threshold can be bypassed leading to minority TXs
vuln_class: []
---

# TRST-H-3 Target signature threshold can be bypassed leading to minority TXs

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
`checkTransaction()` is the enforcer of the HSG logic, making sure signers are wearers of hats 
and so on. The check below makes sure sufficient hat wearers signed the TX:
```solidity
        uint256 validSigCount = countValidSignatures(txHash, signatures, signatures.length / 65);
                // revert if there aren't enough valid signatures
        if (validSigCount < safe.getThreshold()) {
                     revert InvalidSigners();
         }
```
The issue is that the safe's threshold is not guaranteed to be up to date. For example, 
initially there were 5 delegated signers. At some point, three lost eligibility. 
`reconcileSignerCount()` is called to update the safe's threshold to now have 2 signers. At a 
later point, the three signers which lost eligibility regained it. At this point, the threshold is 
still two, but there are 5 valid signers, so if **targetThreshold** is not below 5, they should all 
sign for a TX to be executed. That is not the case, as the old threshold is used. There are 
various scenarios which surface the lack of synchronization between the wearer status and 
safe's stored threshold.

**Recommended Mitigation:**
Call `reconcileSignerCount()` before the validation code in `checkTransaction()`.
 
**Team response:**
Fixed
