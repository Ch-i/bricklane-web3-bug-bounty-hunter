---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing zero address check for `recipient`
vuln_class: []
---

# Missing zero address check for `recipient`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `Licredity::exchangeFungible`, `Licredity::withdrawFungible`, `Licredity::withdrawNonFungible`, and `Licredity::seize` functions does not validate the `recipient` address. For example, if a user calls `Licredity::withdrawFungible` and provides `address(0)` as the recipient, the function will proceed to transfer the fungible tokens to the zero address. Most token standards treat a transfer to the zero address as a burn, meaning the tokens are permanently and irretrievably lost.

**Impact:** A user could accidentally provide the zero address due to a user interface bug, a scripting error, or simple human mistake. This would lead to the irreversible loss of their withdrawn assets. While the action is initiated by the user, the contract could easily prevent this common and costly error.

**Recommended Mitigation:** Add a `require` statement at the beginning of the `withdrawFungible` function to ensure the `recipient` address is not the zero address.

```solidity
// ...existing code...
    /// @inheritdoc ILicredity
    function withdrawFungible(uint256 positionId, address recipient, Fungible fungible, uint256 amount) external {
        require(recipient != address(0), "Cannot withdraw to zero address");
        Position storage position = positions[positionId];

        // require(position.owner == msg.sender, NotPositionOwner());
// ...existing code...
```

**Licredity:** Fixed in [PR#58](https://github.com/Licredity/licredity-v1-core/pull/58/files), commit [`d0b6f6d`](https://github.com/Licredity/licredity-v1-core/commit/d0b6f6da165fd48d6aca29f0b4382c2ecc3bbaae)

**Cyfrin:** Verified. A modifier `noZeroAddress` is added and used by the above mentioned functions.
