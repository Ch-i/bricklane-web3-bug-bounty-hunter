---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-01-cyfrin-metamask-delegationframework-part3-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-05-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-01-cyfrin-metamask-delegationframework-part3-v2-0
title: Missing zero address checks in DelegationMetaSwapAdapter
vuln_class: []
---

# Missing zero address checks in DelegationMetaSwapAdapter

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-01-cyfrin-metamask-delegationFramework-part3-v2.0.md)_

---

**Description:** Missing zero address checks in the `constructor` and `setSwapApiSigner` functions of `DelegationMetaSwapAdapter`.

```solidity

  constructor(
        address _owner,
        address _swapApiSigner,
        IDelegationManager _delegationManager,
        IMetaSwap _metaSwap,
        address _argsEqualityCheckEnforcer
    )
        Ownable(_owner)
    {
        swapApiSigner = _swapApiSigner; //@audit missing address(0) check
        delegationManager = _delegationManager; //@audit missing address(0) check
        metaSwap = _metaSwap; //@audit missing address(0) check
        argsEqualityCheckEnforcer = _argsEqualityCheckEnforcer; //@audit missing address(0) check
        emit SwapApiSignerUpdated(_swapApiSigner);
        emit SetDelegationManager(_delegationManager);
        emit SetMetaSwap(_metaSwap);
        emit SetArgsEqualityCheckEnforcer(_argsEqualityCheckEnforcer);
    }
  function setSwapApiSigner(address _newSigner) external onlyOwner {
        swapApiSigner = _newSigner; //@audit missing address(0) check
        emit SwapApiSignerUpdated(_newSigner);
    }
```



**Recommended Mitigation:** Consider adding zero address checks.

**Metamask:** Resolved in commit [6912e73](https://github.com/MetaMask/delegation-framework/commit/6912e732e2ed65699152c6bfdb46a0ed433f1263).

**Cyfrin:** Resolved.
