---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-30
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-31] Incorrect encoding for Permit'
vuln_class: []
---

# [L-31] Incorrect encoding for Permit

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

```solidity
  function permit(
    address owner,
    address spender,
    uint amount,
    uint deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external override {
    if (deadline < block.timestamp) revert ExpiredDeadline();
    bytes32 digest = keccak256(
      abi.encodePacked(
        '\x19\x01',
        this.domainSeparator(),
        keccak256(abi.encode(_PERMIT_TYPEHASH, owner, spender, amount, _nonces[owner]++, deadline))
      )
    );

    bytes32 signedMsg = MessageHashUtils.toEthSignedMessageHash(digest); /// @audit this is not necessary /  incorrect, it's a double encoding
    address recoveredAddress = ECDSA.recover(signedMsg, v, r, s); /// @audit QA: This is not Permit EIP!
    if (recoveredAddress != owner) revert InvalidSignature();
    _approve(owner, spender, amount);
  }
```

The additional `MessageHashUtils.toEthSignedMessageHash(digest);` is not necessary and is re-encoding the user signature

Per the EIP, you're supposed to simply sign on the digest
https://eips.ethereum.org/EIPS/eip-2612

Also check this implementation of a JS signature library:
https://github.com/dmihal/eth-permit/blob/34f3fb59f0e32d8c19933184f5a7121ee125d0a5/src/rpc.ts#L59-L71

As you can see the signature is done on the digest, the additional encoding you're doing would require re-encoding with ethSignedMessage on the encoded digest

Even when relying on RPC the method is `eth_signTypedData_v4`
https://github.com/dmihal/eth-permit/blob/34f3fb59f0e32d8c19933184f5a7121ee125d0a5/src/rpc.ts#L73-L93


See: https://docs.metamask.io/wallet/reference/eth_signtypeddata_v4/

**Mitigation**


Change the code to compare the signature against the digest

```solidity
  function permit(
    address owner,
    address spender,
    uint amount,
    uint deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external override {
    if (deadline < block.timestamp) revert ExpiredDeadline();
    bytes32 digest = keccak256(
      abi.encodePacked(
        '\x19\x01',
        this.domainSeparator(),
        keccak256(abi.encode(_PERMIT_TYPEHASH, owner, spender, amount, _nonces[owner]++, deadline))
      )
    );

    address recoveredAddress = ECDSA.recover(digest, v, r, s);
    if (recoveredAddress != owner) revert InvalidSignature();
    _approve(owner, spender, amount);
  }
```
