---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-13
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-14] Revert Case for Oracle being provided insufficient gas is inaccurate'
vuln_class: []
---

# [L-14] Revert Case for Oracle being provided insufficient gas is inaccurate

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The following finding has no impact unless Chainlinks proxy is changed to revert for OOG on purpose

Meaning that the CL team would need to:
- Replace their proxy
- Purposefully put a malicious one that reverts


In that scenario, the 1/64 gas check would result as incorrect

And due to it, any call to the price feed would always result in a revert, permanently DOSSing the system

**Proof Of Concept**

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {console} from "forge-std/console.sol";


contract MockCLFeed {
    enum Behaviour {
        NORMAL,
        REVERT,
        GASGRIEF
    }

    Behaviour behaviour = Behaviour.NORMAL;

    function setBehaviour(Behaviour b) external {
        behaviour = b;
    }

    function latestRoundData() external view returns (
            uint80 roundId, int256 answer, uint256, /* startedAt */ uint256 updatedAt, uint80 /* answeredInRound */
        ) {
            
            if(behaviour == Behaviour.REVERT) {
                revert("No out of gas");
            }

            if(behaviour == Behaviour.GASGRIEF) {
                // Grief them, burn all gas
                uint256 i;
                while (true) {
                    i++;
                }
            }


            answer = 123;   
        }
    

}

contract PriceLibTester is Test {

    function getCurrentChainlinkResponse(MockCLFeed _aggregator)
        external
        view
        returns (int256 price)
    {
        uint256 gasBefore = gasleft();

        // Try to get latest price data:
        try _aggregator.latestRoundData() returns (
            uint80 roundId, int256 answer, uint256, /* startedAt */ uint256 updatedAt, uint80 /* answeredInRound */
        ) {


            return answer;
        } catch {
            // NOTE: The check is ignoring additional costs that come from processing the error + the call
            // So even thought the check is directionally right
            // You would need to give a few thousands gas of leniency to the check to actually be safe
            
            // Require that enough gas was provided to prevent an OOG revert in the call to Chainlink
            // causing a shutdown. Instead, just revert. Slightly conservative, as it includes gas used
            // in the check itself.
            console.log("gasleft()", gasleft());
            console.log("gasBefore / 64", gasBefore / 64);
            if (gasleft() + 2000 <= gasBefore / 64) revert("InsufficientGasForExternalCall()");

            // If call to Chainlink aggregator reverts, return a zero response with success = false
            return -1;
        }
    }

    // forge test --match-test test_normal_and_revert_case -vv
    function test_normal_and_revert_case() public {
        MockCLFeed feed = new MockCLFeed();

        
        feed.setBehaviour(MockCLFeed.Behaviour.NORMAL);
        this.getCurrentChainlinkResponse(feed);
        console.log("Base case ok");

        
        feed.setBehaviour(MockCLFeed.Behaviour.REVERT);
        this.getCurrentChainlinkResponse(feed);
        console.log("Revert case ok");

        // NOTE: This fails
        feed.setBehaviour(MockCLFeed.Behaviour.GASGRIEF);
        this.getCurrentChainlinkResponse(feed);
        console.log("Gas Grief Case ok");


    }

    
}
```

**Mitigation**

Changing the code to have an additional small buffer:
```solidity
       if (gasleft() + 2000 <= gasBefore / 64) revert("InsufficientGasForExternalCall()");
```

Would ensure that the cost of processing the call and the cost of handling the error are accounted for

However, if OOG Dosses are a real concern, you should cap the gas given to CL to a certain amount (e.g. 1MLN Gas)
