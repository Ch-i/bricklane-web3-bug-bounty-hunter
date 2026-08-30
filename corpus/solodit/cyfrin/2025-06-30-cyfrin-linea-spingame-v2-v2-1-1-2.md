---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Stale request id mapping persists for losing spins
vuln_class: []
---

# Stale request id mapping persists for losing spins

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** One change from the previous version of `SpinGame` is the removal of the "LuckyNFT," which served as a consolation prize for users who did not win a "proper" prize.

As part of this change, the clearing of the request mapping (`requestIdToUser`) was moved so that it now occurs **only** in the prize win path, as shown in [`SpinGame::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/0af327319636960e9683897c5935aa1a78d1ded5/contracts/src/Spin.sol#L604-L612):

```solidity
            userToPrizesWon[user][selectedPrizeId] += 1;
            delete requestIdToUser[_requestId];
            emit PrizeWon(user, selectedPrizeId);

            return;
        }
    }
    emit NoPrizeWon(user);
}
```

However, it is considered good housekeeping to clear the `requestIdToUser` mapping regardless of whether the user wins or not. This ensures consistent state cleanup and prevents potential stale entries from persisting.

Consider unconditionally clearing the request mapping as follows:
```diff
function _fulfillRandomness(
    uint256 _randomness,
    uint256 _requestId,
    bytes memory
) internal override {
    address user = requestIdToUser[_requestId];
    if (user == address(0)) {
        revert InvalidRequestId(_requestId);
    }
+   delete requestIdToUser[_requestId];

    ...

            userToPrizesWon[user][selectedPrizeId] += 1;
-           delete requestIdToUser[_requestId];
            emit PrizeWon(user, selectedPrizeId);


            return;
        }
    }
    emit NoPrizeWon(user);
}
```

**Linea:** Fixed in commit [`9f9d9fd`](https://github.com/Consensys/linea-hub/pull/554/commits/9f9d9fd76d2672f572e31079b5811bf6f0f48eed)

**Cyfrin:** Verified. `requestIdToUser` deleted at the beginning of `_fulfillRandomness`.
