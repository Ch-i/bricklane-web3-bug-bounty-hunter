---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Extra validation on `CentralToken::addChildToken` will prevent adding incorrect
  `ChildToken`
vuln_class: []
---

# Extra validation on `CentralToken::addChildToken` will prevent adding incorrect `ChildToken`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** Currently, it is possible to:
- Create a `childToken0` which sets `centralToken0` as its parent
- For a different central call `centralToken1::addChildToken(centralToken0)`

**Recommended Mitigation:** To prevent this mismatch the following extra validation is recommended:

```diff
+  error ChildTokenNotChildOfThis();
```

```diff
  interface IChildRWAToken {
+     function centralToken() external view returns (address);
      function domestic() external view returns (bool);
      function distributePayout(uint128 amount) external;
      function mint(address to, uint256 amount) external;
      function balanceOf(address account) external view returns (uint256);
      function toggleBurning(bool newState) external;
      function togglePause(bool newState) external;
}
```

```diff
    function addChildToken(
        address tokenAddress
    ) external nonReentrant restricted {
        if (tokenAddress == address(0) || tokenAddress.code.length == 0)
            revert InvalidAddress();

+       if (IChildRWAToken(tokenAddress).centralToken() != address(this)) revert ChildTokenNotChildOfThis();
        // 0 for domestic, 1 for foreign
        bool isDomestic = IChildRWAToken(tokenAddress).domestic();
        uint256 childIndex = isDomestic ? 0 : 1;


        if (childTokens[childIndex] != address(0)) revert ChildTokenAlreadyExists();
        childTokens[uint256(childIndex)] = tokenAddress;

        emit ChildTokenAdded(tokenAddress, isDomestic);
    }
```

**Remora:** Fixed at commit [846851a](https://github.com/remora-projects/remora-dynamic-tokens/commit/846851ae7f691ed77d235185584ac0fb82b43e77).

**Cyfrin:** Verified.
