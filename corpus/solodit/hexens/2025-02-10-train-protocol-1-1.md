---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-10-train-protocol-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-02-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md
tags:
- firm:hexens
- report:2025-02-10-train-protocol
title: '[LYSWP2-8] Unchecked ERC20 transfer return value may cause HTLC inconsistency
  across chains'
vuln_class: []
---

# [LYSWP2-8] Unchecked ERC20 transfer return value may cause HTLC inconsistency across chains

_Section severity (from Solodit section header): Medium_  
_Audit firm: Hexens_  
_Source report: [2025-02-10-Train-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md)_

---

**Severity:** Medium

**Path:** chains/starknet/src/HashTimeLockedERC20.cairo#L391-L464, HashTimeLockedERC20.cairo#L339, HashTimeLockedERC20.cairo#L423

**Description:** The contract does not check the return value of `transferFrom()` and `transfer()` in multiple places, assuming that all ERC20 transfers will succeed. This is an issue because some ERC20 tokens do not revert on failure but instead return false. If the contract does not explicitly validate these return values, it may proceed with logic without actually transferring the funds, leading to severe inconsistencies. 

The `commit()` function executes an ERC20 `transferFrom()` call to move tokens from the user to the contract. However, the function does not check the return value of `transferFrom()`, assuming it will always succeed. In cases where the ERC20 token does not revert on failure but instead returns `false`, the function will continue execution without actually transferring funds.

This issue becomes particularly critical in a cross-chain scenario where an LP (Liquidity Provider) observes a commit event and locks funds on the destination chain (e.g., Ethereum). If the initial token transfer on the source chain (e.g., Starknet) failed silently, the LP would lock funds on the destination chain without receiving corresponding funds on the source chain.

This issue is not limited to the `commit()` function. Other functions, such as `lock()`, `redeem()`, and `refund()`, also fail to check ERC20 transfer return values, potentially leading to similar inconsistencies and unexpected behavior.
```
fn commit(
            ref self: ContractState,
            Id: u256,
            amount: u256,
            sender_key: felt252,
            dstChain: felt252,
            dstAsset: felt252,
            dstAddress: ByteArray,
            srcAsset: felt252,
            srcReceiver: ContractAddress,
            timelock: u64,
            tokenContract: ContractAddress,
        ) -> u256 {
            //Check that the ID is unique
            assert!(!self.hasHTLC(Id), "Commitment Already Exists");
            assert!(self.validTimelock(timelock), "Invalid TimeLock");
            assert!(amount != 0, "Funds Can Not Be Zero");

            // transfer the token from the user into the contract
            let token: IERC20Dispatcher = IERC20Dispatcher { contract_address: tokenContract };
            assert!(token.balance_of(get_caller_address()) >= amount, "Insufficient Balance");
            assert!(
                token.allowance(get_caller_address(), get_contract_address()) >= amount,
                "Not Enough Allowence"
            );
            token.transfer_from(get_caller_address(), get_contract_address(), amount);

            //Write the PreHTLC data into the storage
            self
                .contracts
                .write(
                    Id,
                    HTLC {
                        amount: amount,
                        hashlock: 0,
                        secret: 0,
                        tokenContract: tokenContract,
                        timelock: timelock,
                        claimed: 1,
                        sender: get_caller_address(),
                        sender_key: sender_key,
                        srcReceiver: srcReceiver,
                    }
                );

            let hop_chains = array!['null'].span();
            let hop_assets = array!['null'].span();
            let hop_addresses = array!['null'].span();

            self
                .emit(
                    TokenCommitted {
                        Id: Id,
                        hopChains: hop_chains,
                        hopAssets: hop_assets,
                        hopAddress: hop_addresses,
                        dstChain: dstChain,
                        dstAddress: dstAddress,
                        dstAsset: dstAsset,
                        sender: get_caller_address(),
                        srcReceiver: srcReceiver,
                        srcAsset: srcAsset,
                        amount: amount,
                        timelock: timelock,
                        tokenContract: tokenContract,
                    }
                );
            Id
        }
```

**Remediation:**  Explicitly check all ERC20 transfer return values (`transferFrom()` and `transfer()`). If the function returns `false`, the transaction should revert immediately.

**Status:**  Fixed


- - -
