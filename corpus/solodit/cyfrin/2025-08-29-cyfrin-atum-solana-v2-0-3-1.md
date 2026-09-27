---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-atum-solana-v2-0-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-atum-solana-v2-0
title: Solana version is passing `settler` address  in Solana public key format
vuln_class: []
---

# Solana version is passing `settler` address  in Solana public key format

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-atum-solana-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-atum-solana-v2.0.md)_

---

**Description:** In the `fullfillment_proxy` the settler address is passed in Solana Address where it is emited as Public Key.

[fulfillment_proxy/src/lib.rs#L29](https://github.com/Atum-Labs/solana-escrow/blob/main/programs/fulfillment_proxy/src/lib.rs#L29)
```rust
    pub fn fulfill(ctx: Context<Fulfill>, request_hash: [u8; 32], amount: u64) -> Result<()> {
        token::transfer_checked( ... )?;
        emit!(Fulfilled {
            request_hash,
>>          settler: ctx.accounts.settler.key(),
            to: ctx.accounts.to.key(),
            from: ctx.accounts.settler.key(),
            token: ctx.accounts.mint.key(),
            amount,
            timestamp: Clock::get()?.unix_timestamp as u64,
        });
        Ok(())
    }
```

The problem is that the settle address is coming from the source chain as an EVM address, and the `fulfillment_proxy` is desired to be called at destination chain.

So in case the exection was Ethereum->Solana. On EVM version, the settler address is passed in `EVM::address`, which results in incompatibility between the EVM events and Solana events

In EVM version settler address is independent to the address that sending the funds, and is passed regarding the `from` address (sender) of the tokens

[FulfillmentProxy.sol#L19](https://github.com/Atum-Labs/audit-2025-08-atum/blob/main/src/FulfillmentProxy.sol#L19)
```solidity
    function fulfill(Fulfillment calldata params) public whenNotPaused {
        IERC20(params.token).safeTransferFrom(msg.sender, params.to, params.amount);
        emit Fulfilled(
>>          params.requestHash, params.settler, params.to, msg.sender, params.token, params.amount, block.timestamp
        );
    }
// -----------
    event Fulfilled(
        bytes32 indexed requestHash,
>>      address indexed settler,
        address indexed to,
>>      address from,
        address token,
        uint256 amount,
        uint256 timestamp
    );
```

**Impact:**
- Incorrect event emiting in Solana side on Destination chain compared to the EVM Source chain

**Recommended Mitigation:** We should pass `settler` address independently in EVM format, or we can simply remove it, since it is not used by the system anymore

**Atum:**
Fixed in [88674a7](https://github.com/Atum-Labs/solana-escrow/commit/88674a7bbdf34186954db30783c154ef0bdf6bff).

**Cyfrin:** Verified.
