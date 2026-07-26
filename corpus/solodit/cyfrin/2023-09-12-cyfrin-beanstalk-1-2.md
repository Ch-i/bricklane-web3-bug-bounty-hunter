---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: FundraiserFacet logic does not consider contract upgrades which can increase
  token decimals
vuln_class: []
---

# FundraiserFacet logic does not consider contract upgrades which can increase token decimals

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** The fundraiser logic in `FundraiserFacet` assumes that the decimals of the token being raised will remain with the same number of decimals from when a fundraiser is created to when it is funded. In the case of USDC, a contract upgrade that increases the number of decimals would invalidate this assumption, jeopardizing the accounting handled by `s.fundraisers[id].remaining`.

**Impact:** If the original fundraiser token increases its decimals, a user can send fewer tokens than expected through `FundraiserFacet::fund` and receive more Pods than intended.

**Proof of Concept:**
1. Beanstalk creates a USDC fundraiser for 1M USDC
2. USDC decimals are updated from 6 to 18, meaning that the amount of USDC to raise should be $1,000,000 \times 10^{18}$ rather than $1,000,000 \times 10^{6} = 1 \times 10^{12}$.
3. Eve uses $1 \times 10^{12}$ basic units of USDC (now equivalent to $1 \times 10^{-18}$ USDC) to completely fund the fundraiser, receiving Pods for a value of 1M Beans.

The final result is that Beanstalk has received $1 \times 10^{-6}$ USD in USDC in exchange for the issuance of 1M Pods.

**Recommended Mitigation:** It would be advisable to save the decimals during fundraiser creation and check their consistency when calls are made to `FundraiserFacet::fund`. This can be achieved by creating a new function that updates `s.fundraisers[id].remaining` and the saved decimals in case of an update. For instance:

```diff
    // FundraiserFacet.sol
    function createFundraiser(
        address payee,
        address token,
        uint256 amount
    ) external payable {
        LibDiamond.enforceIsOwnerOrContract();

        // The {FundraiserFacet} was initially created to support USDC, which has the
        // same number of decimals as Bean (6). Fundraisers created with tokens measured
        // to a different number of decimals are not yet supported.
        if (ERC20(token).decimals() != 6) {
            revert("Fundraiser: Token decimals");
        }

        uint32 id = s.fundraiserIndex;
        s.fundraisers[id].token = token;
        s.fundraisers[id].remaining = amount;
        s.fundraisers[id].total = amount;
        s.fundraisers[id].payee = payee;
        s.fundraisers[id].start = block.timestamp;
+       s.fundraisers[id].savedDecimals = 6;
        s.fundraiserIndex = id + 1;

        // Mint Beans to pay for the Fundraiser. During {fund}, 1 Bean is burned
        // for each `token` provided to the Fundraiser.
        // Adjust `amount` based on `token` decimals to support tokens with different decimals.
        C.bean().mint(address(this), amount);

        emit CreateFundraiser(id, payee, token, amount);
    }

    function fund(
        uint32 id,
        uint256 amount,
        LibTransfer.From mode
    ) external payable nonReentrant returns (uint256) {
        uint256 remaining = s.fundraisers[id].remaining;

        // Check amount remaining and constrain
        require(remaining > 0, "Fundraiser: completed");
        if (amount > remaining) {
            amount = remaining;
        }
+
+       require(s.fundraisers[id].token.decimals() == s.fundraisers[id].savedDecimals, "Fundraiser token decimals not synchronized.");
+
        // Transfer tokens from msg.sender -> Beanstalk
        amount = LibTransfer.receiveToken(
            IERC20(s.fundraisers[id].token),
            amount,
            msg.sender,
            mode
        );
        s.fundraisers[id].remaining = remaining - amount; // Note: SafeMath is redundant here.
        emit FundFundraiser(msg.sender, id, amount);

        // If completed, transfer tokens to payee and emit an event
        if (s.fundraisers[id].remaining == 0) {
            _completeFundraiser(id);
        }

        // When the Fundraiser was initialized, Beanstalk minted Beans.
        C.bean().burn(amount);

        // Calculate the number of Pods to Sow.
        // Fundraisers bypass Morning Auction behavior and Soil requirements,
        // calculating return only based on the current `s.w.t`.
        uint256 pods = LibDibbler.beansToPods(
            amount,
            uint256(s.w.t).mul(LibDibbler.TEMPERATURE_PRECISION)
        );

        // Sow for Pods and return the number of Pods received.
        return LibDibbler.sowNoSoil(msg.sender, amount, pods);
    }
+
+   function synchronizeFundraiserDecimals(uint32 id) public {
+       uint32 currentTokenDecimals = s.fundraisers[id].token.decimals();
+       uint32 savedDecimals = s.fundraisers[id].savedDecimals;
+       require(currentTokenDecimals != savedDecimals, "Fundraiser token decimals already synchronized");
+       if (currentTokenDecimals > savedDecimals) {
+           uint32 decimalDifference = currentTokenDecimals - savedDecimals;
+           s.fundraisers[id].total = s.fundraisers[id].total * decimalDifference;
+           s.fundraisers[id].remaining = s.fundraisers[id].remaining * decimalDifference;
+       } else {
+           uint32 decimalDifference = savedDecimals - currentTokenDecimals;
+           s.fundraisers[id].total = s.fundraisers[id].total / decimalDifference;
+           s.fundraisers[id].remaining = s.fundraisers[id].remaining / decimalDifference;
+       }
+   }

    // AppStorage.sol
    struct Fundraiser {
        address payee;
        address token;
        uint256 total;
        uint256 remaining;
        uint256 start;
+       uint256 savedDecimals;
    }
```
