---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Missing zero delta check in `increaseDebtShare` and `decreaseDebtShare`
vuln_class: []
---

# Missing zero delta check in `increaseDebtShare` and `decreaseDebtShare`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `Licredity::increaseDebtShare` and `Licredity::decreaseDebtShare` functions do not validate that the `delta` parameter is non-zero. A user can call these functions with `delta = 0`, which will result in an `amount` of 0. The function will proceed with its execution, performing all the necessary checks and state reads, but will ultimately not alter the position's debt or the total debt balance. However, it will still emit an `IncreaseDebtShare` or `DecreaseDebtShare` event with zero values.

**Impact:**
- **Wasted Gas and Unnecessary Operations:** Calling these functions with a zero `delta` serves no purpose but still consumes gas for the function call and its internal operations.
- **Event Log Spamming:** It allows a malicious actor to spam the blockchain with zero-value events, which can clutter event logs and make it more difficult for off-chain monitoring tools and indexers to parse meaningful data. This is a low-level griefing vector.

**Recommended Mitigation:** Add a requirement at the beginning of both `increaseDebtShare` and `decreaseDebtShare` to ensure that `delta` is greater than zero.

```solidity
// ...existing code...
    function increaseDebtShare(uint256 positionId, uint256 delta, address recipient)
        external
        returns (uint256 amount)
    {
        require(delta > 0, "Delta must be greater than zero");
        Position storage position = positions[positionId];

        // require(position.owner == msg.sender, NotPositionOwner());
// ...existing code...
// ...existing code...
    function decreaseDebtShare(uint256 positionId, uint256 delta, bool useBalance) external returns (uint256 amount) {
        require(delta > 0, "Delta must be greater than zero");
        Position storage position = positions[positionId];

        uint256 _totalDebtShare = totalDebtShare; // gas saving
// ...existing code...
```

**Licredity:** Acknowledged. But we'll leave as is, the thinking is 1) this vector wastes gas for the attacker but does not change state (other than the event); 2) similar vector still exists for other functions like `open()`, which cannot be easily prevented; 3) fixing it will result others to pay a bit extra gas for the check
