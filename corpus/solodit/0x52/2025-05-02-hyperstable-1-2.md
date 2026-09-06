---
affected_contracts: []
derives_from: []
id: solodit-0x52-2025-05-02-hyperstable-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
tags:
- firm:0x52
- report:2025-05-02-hyperstable
title: '[M-03] Curve gauge rewards can be griefed'
vuln_class: []
---

# [M-03] Curve gauge rewards can be griefed

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2025-05-02-Hyperstable.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md)_

---

**Details**

[Gauge.sol#L123-L131](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/Gauge.sol#L123-L131)

        function claimFees() external lock {
    @>      require(msg.sender == IVotingEscrow(_ve).team(), "only team");

            if (staking == address(0)) {
                return;
            }

            ICurveGauge(staking).claimRewards(address(this), msg.sender);
        }

`Gauge#claimFees` attempts to lock down claims so that only the team can claim however if you look at the curve gauge code, the claim process is permissionless if `_receiver == address(0)`. When claimed with `_receiver == address(0)` it will send the rewards to the holder which in this case is the `gauge` contract itself.

[LiquidityGaugeV5.vy#L416-L426](https://github.com/curvefi/curve-dao-contracts/blob/567927551903f71ce5a73049e077be87111963cc/contracts/gauges/LiquidityGaugeV5.vy#L416-L426)

        def claim_rewards(_addr: address = msg.sender, _receiver: address = ZERO_ADDRESS):
            """
            @notice Claim available reward tokens for _addr
            @param _addr Address to claim for
            @param _receiver Address to transfer rewards to - if set to
                            ZERO_ADDRESS, uses the default reward receiver
                            for the caller
            """
            if _receiver != ZERO_ADDRESS:
    @>          assert _addr == msg.sender  # dev: cannot redirect when claiming for another user
            self._checkpoint_rewards(_addr, self.totalSupply, True, _receiver)

As a result the `gauge` rewards can be griefed and sent directly to the `gauge` contract instead of being sent to the team which will result in them being permanently unrecoverable.

**Lines of Code**

[Gauge.sol#L123-L131](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/Gauge.sol#L123-L131)

**Recommendation**

LP should be staked via a proxy contract. This way all rewards can be sent to the team and there is never any chance they are mixed with user rewards or stranded.

**Remediation**

Fixed in [1aeb762](https://github.com/hyperstable/contracts/commit/1aeb762d777ebd59321713497dd5a6d17b2db01a). reward_receiver is set to team address direct all permissionless claims there instead of the gauge contract.
