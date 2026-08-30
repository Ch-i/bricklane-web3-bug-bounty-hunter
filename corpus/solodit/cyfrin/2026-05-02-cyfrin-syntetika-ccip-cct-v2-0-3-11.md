---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: 'Documentation mismatches: NatSpec, docstrings and comments disagree with code'
vuln_class: []
---

# Documentation mismatches: NatSpec, docstrings and comments disagree with code

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Grouping of documentation-versus-code mismatches across the codebase. Each sub-item is a distinct instance of NatSpec, a docstring, or an inline comment that disagrees with actual contract behavior.

---

**1. `HilToken::burnFrom` NatSpec claims owner requires allowance**

`burnFrom` skips `_spendAllowance` when `spender == owner()`. The NatSpec says "The sender must have allowance for the `from` address" - which is false when sender is owner.

```solidity
issuance/src/token/HilToken.sol
161:     * @dev The sender must have allowance for the `from` address.
...
167:    function burnFrom(address from, uint256 amount) external {
168:        address spender = msg.sender;
169:        if (spender != from && spender != owner()) {
170:            _spendAllowance(from, spender, amount);
171:        }
172:        _burn(from, amount);
173:    }
```

**Recommended:** Update NatSpec to clarify the owner bypass, e.g. "...unless the sender is the owner, in which case allowance is bypassed." Owner burning arbitrary user balances is a privileged power that should ideally be emitted as a distinct event.

---

**2. `StakingVault::setMaxEarlyExitFeeBps` strict `<` makes documented 10% cap unreachable**

Comment says "(10%)"; `MAX_FEE = 1_000` (10% in BPS). The check `require(newValue < MAX_FEE, IncorrectEarlyExitFee())` rejects exactly 10%, so the advertised max is unreachable. Also inconsistent with `setCooldownDuration` which uses non-strict `<= MAX_COOLDOWN_DURATION`.

Source: `issuance/src/vault/StakingVault.sol:163-170`.

**Recommended:** Change to `<=` or correct the NatSpec/comment to say "<10%".

---

**3. `HilBTC` and `HilUSD` contract-level NatSpec copied verbatim from `HilToken`**

Both files declare the same `@dev "ERC20 token with permit functionality, minting and burning, and role-based access control."` NatSpec - they should describe their specialization (decimals difference, asset type).

**Recommended:** Update NatSpec to state decimals and intended base asset.


**Syntetika:** Fixed in commits [`5411680`](https://github.com/SyntetikaLabs/monorepo/commit/5411680b7d7b1f21e2c7240d0e928268bc55eb86), and [`ab4c806`](https://github.com/SyntetikaLabs/monorepo/commit/ab4c8065c1755c9c6a47cd5ed3abc17ee7b4341f)

**Cyfrin:** Verified.
