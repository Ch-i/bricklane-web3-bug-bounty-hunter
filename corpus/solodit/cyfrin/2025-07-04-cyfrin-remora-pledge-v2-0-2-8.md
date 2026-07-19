---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Minting new PropertyTokens close to the end of the distribution period will
  dilute rewards for holders who were holding for the full period
vuln_class: []
---

# Minting new PropertyTokens close to the end of the distribution period will dilute rewards for holders who were holding for the full period

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Holder's balanceHistory is updated each time a transfer of tokens occurs (mint or burn too). The [accounting saves the holders' balance during a certain index](https://github.com/remora-projects/remora-smart-contracts/blob/main/contracts/RWAToken/DividendManager.sol#L533-L540), which is used to determine the payout earned from the distributed amount of stablecoin for the index.

```solidity
    function _updateHolders(address from, address to) internal {
        ...
            } else {
                // else update status data and create new entry
                tHolderStatus.mostRecentEntry = payoutIndex;
//@audit => saves the holder balance for the current payout, regardless of how much time is left for the distribution to end
                $._balanceHistory[to][payoutIndex] = TokenBalanceChange({
                    isValid: true,
                    tokenBalance: toBalance
                });
            }
        }

```

New mintings of PropertyTokens mean that the same amount of payout distributed for all holders will give less payout to each PropertyToken. The problem is that new mintings that occur close to the end of the distribution period will dilute payouts for holders who have held their PropertyTokens for the full period.

**Impact:** Holders who have held their PropertyTokens for the full distribution period will get their rewards diluted by new PropertyTokens that get minted close to the end of the period.

**Recommended Mitigation:** On the [mint()](https://github.com/remora-projects/remora-smart-contracts/blob/main/contracts/RWAToken/RemoraToken.sol#L268-L270) calculate how much time has passed on the current distribution period, and if a certain threshold (maybe 75-80%) has passed, don't allow new mintings until the next distribution period.

**Remora:** Acknowledged.
