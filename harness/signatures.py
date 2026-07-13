"""Pattern signature registry — detection heuristics for each web3 logic pattern.

Each signature defines regex patterns, function selectors, and keywords that
indicate a contract may be affected by a specific vulnerability or logic pattern.
Used by the scanner to produce instant audit checklists from raw Solidity source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class PatternSignature:
    slug: str
    title: str
    severity: str  # Critical, High, Medium
    detectors: list[str]  # regex patterns to match against source code
    checklist: list[str]  # audit checklist items if pattern is detected
    description: str = ""
    confidence_boost_keywords: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Registry — ordered by severity (Critical first)
# ---------------------------------------------------------------------------

SIGNATURES: list[PatternSignature] = [
    # --- Critical Severity ---
    PatternSignature(
        slug="flash-loan-mechanics",
        title="Flash Loan Composability",
        severity="Critical",
        detectors=[
            r"\bflashLoan\b",
            r"\bonFlashLoan\b",
            r"\bIERC3156\b",
            r"\bflash\s*[Ll]oan\b",
            r"\bexecuteOperation\b",  # Aave
            r"\buniswapV[23]Call\b",  # Uniswap flash
            r"\bpancakeCall\b",
        ],
        checklist=[
            "Verify flash loan callback caller is the expected pool contract",
            "Check that initiator == address(this) to prevent unauthorized callbacks",
            "Ensure atomicity — all state changes revert if repayment fails",
            "Verify no untrusted external calls within the callback body",
            "Check for donation/inflation attacks on vault shares during flash context",
            "Audit for oracle price manipulation within flash loan scope",
        ],
        confidence_boost_keywords=["callback", "repay", "borrow", "pool"],
    ),

    PatternSignature(
        slug="checks-effects-interactions",
        title="Reentrancy / CEI Violation",
        severity="Critical",
        detectors=[
            r"\.call\{.*value\s*:",        # low-level call with value
            r"\.call\{",                     # any low-level call
            r"\btransfer\s*\(",              # ERC20 transfer (external call)
            r"\bsafeTransfer\s*\(",
            r"\bsafeTransferFrom\s*\(",
            r"nonReentrant",                 # has protection (good signal)
            r"ReentrancyGuard",
        ],
        checklist=[
            "Verify Checks-Effects-Interactions ordering: state updates BEFORE external calls",
            "Check for cross-function reentrancy (function A calls external, function B reads stale state)",
            "Check for cross-contract reentrancy via shared state (e.g., vault balance)",
            "Verify read-only reentrancy protection on view functions used for pricing",
            "Confirm ReentrancyGuard is applied to ALL state-changing functions, not just some",
            "Check callback hooks (ERC-777 tokensReceived, ERC-1155 onERC1155Received) for reentrancy",
        ],
        confidence_boost_keywords=["balanceOf", "state", "update", "withdraw", "deposit"],
    ),

    PatternSignature(
        slug="oracle-aggregation-staleness",
        title="Oracle Manipulation / Staleness",
        severity="Critical",
        detectors=[
            r"\blatestRoundData\b",
            r"\bAggregatorV3Interface\b",
            r"\bgetPrice\b",
            r"\bpriceFeed\b",
            r"\bTWAP\b",
            r"\bgetReserves\b",  # on-chain TWAP from reserves
            r"\bslot0\b",       # Uniswap V3 spot price
        ],
        checklist=[
            "Verify staleness check: require(updatedAt > block.timestamp - HEARTBEAT)",
            "Check for sequencer uptime feed on L2 deployments (Arbitrum, Optimism)",
            "Verify oracle returns are validated: price > 0, answeredInRound >= roundId",
            "Check for TWAP manipulation resistance — is the window long enough?",
            "Verify fallback oracle exists if primary feed goes stale",
            "Check that spot prices (getReserves, slot0) are NOT used for critical pricing",
            "Audit flash loan attack surface on any on-chain price calculation",
        ],
        confidence_boost_keywords=["Chainlink", "oracle", "price", "feed", "heartbeat"],
    ),

    PatternSignature(
        slug="proxy-upgrade-patterns",
        title="Proxy & Upgradeability Risks",
        severity="Critical",
        detectors=[
            r"\bdelegatecall\b",
            r"\bUUPSUpgradeable\b",
            r"\bTransparentUpgradeableProxy\b",
            r"\b_implementation\b",
            r"\bupgradeTo\b",
            r"\binitialize\b",   # initializer pattern
            r"\binitializer\b",
            r"\bERC1967\b",
        ],
        checklist=[
            "Verify initializer can only be called once (initializer modifier)",
            "Check for uninitialized proxy implementation contracts (front-running initialize)",
            "Verify no storage layout collisions between proxy and implementation",
            "Check UUPS: _authorizeUpgrade has proper access control",
            "Verify selfdestruct/delegatecall cannot be called on the implementation directly",
            "Check storage gaps in base contracts for upgrade safety",
            "Verify no immutable variables that break across upgrades",
        ],
        confidence_boost_keywords=["proxy", "upgrade", "implementation", "storage", "slot"],
    ),

    PatternSignature(
        slug="erc4626-tokenized-vault-standard",
        title="ERC-4626 Vault Inflation Attack",
        severity="Critical",
        detectors=[
            r"\bERC4626\b",
            r"\bconvertToShares\b",
            r"\bconvertToAssets\b",
            r"\btotalAssets\b",
            r"\bpreviewDeposit\b",
            r"\bpreviewMint\b",
        ],
        checklist=[
            "Check for first-depositor inflation attack (donation before first deposit)",
            "Verify virtual offset / dead shares defense (OpenZeppelin _decimalsOffset)",
            "Check rounding direction: deposit rounds DOWN shares, withdraw rounds UP shares",
            "Verify totalAssets cannot be manipulated via direct token transfer (donation)",
            "Check for sandwich attacks on deposit/withdraw via share price manipulation",
            "Audit maxDeposit/maxMint/maxWithdraw/maxRedeem limits",
        ],
        confidence_boost_keywords=["vault", "share", "deposit", "withdraw", "asset"],
    ),

    # --- High Severity ---
    PatternSignature(
        slug="access-control-hierarchies",
        title="Access Control & Authorization",
        severity="High",
        detectors=[
            r"\bonlyOwner\b",
            r"\bOwnable\b",
            r"\bAccessControl\b",
            r"\bhasRole\b",
            r"\bgrantRole\b",
            r"\bDEFAULT_ADMIN_ROLE\b",
            r"\btx\.origin\b",    # dangerous auth pattern
            r"\brequire\s*\(\s*msg\.sender\s*==",
        ],
        checklist=[
            "Verify no tx.origin for authentication (phishing vector)",
            "Check two-step ownership transfer pattern for critical admin roles",
            "Verify DEFAULT_ADMIN_ROLE holder cannot be renounced accidentally",
            "Check for missing access control on sensitive functions (mint, pause, upgrade)",
            "Audit role hierarchy — can a lower role escalate to admin?",
            "Verify timelock on admin operations that affect user funds",
        ],
        confidence_boost_keywords=["admin", "owner", "role", "permission", "auth"],
    ),

    PatternSignature(
        slug="signature-replay-eip712",
        title="Signature Replay & EIP-712",
        severity="High",
        detectors=[
            r"\becrecover\b",
            r"\bEIP712\b",
            r"\bDOMAIN_SEPARATOR\b",
            r"\bpermit\b",
            r"\bnonces\b",
            r"\bsignTypedData\b",
            r"\bECDSA\b",
            r"\bSignatureChecker\b",
        ],
        checklist=[
            "Verify nonce increment on every signature use (prevent replay)",
            "Check DOMAIN_SEPARATOR includes chainId (prevent cross-chain replay)",
            "Verify signature includes contract address (prevent cross-contract replay)",
            "Check for signature malleability (s-value normalization)",
            "Verify deadline/expiry on all signed messages",
            "Check ecrecover return value != address(0)",
            "Audit permit() for front-running griefing attacks",
        ],
        confidence_boost_keywords=["signature", "sign", "verify", "nonce", "permit"],
    ),

    PatternSignature(
        slug="integer-overflow-precision-loss",
        title="Integer Overflow & Precision Loss",
        severity="High",
        detectors=[
            r"\bunchecked\b",
            r"\btype\(uint\d+\)\.max\b",
            r"\bmulDiv\b",
            r"\bFullMath\b",
            r"\bFixedPointMathLib\b",
            r"\b/\s*\d+",           # division (potential precision loss)
            r"\bwad\b",
            r"\bray\b",
        ],
        checklist=[
            "Verify unchecked blocks are intentional and bounded (e.g., loop counters)",
            "Check division-before-multiplication (precision loss) in fee/share calculations",
            "Verify rounding direction favors the protocol in all accounting math",
            "Check for dust accumulation from repeated rounding",
            "Audit type casts (uint256 → uint128) for silent truncation",
            "Verify intermediate multiplication cannot overflow uint256",
        ],
        confidence_boost_keywords=["math", "precision", "rounding", "overflow", "scale"],
    ),

    PatternSignature(
        slug="liquidation-mechanics-health-factor",
        title="Liquidation & Health Factor",
        severity="High",
        detectors=[
            r"\bhealthFactor\b",
            r"\bliquidat\w+\b",
            r"\bcollateral\w*Factor\b",
            r"\bltv\b",
            r"\bborrow\b",
            r"\brepay\b",
            r"\bseize\b",
        ],
        checklist=[
            "Verify health factor calculation uses latest oracle prices (not cached)",
            "Check liquidation bonus doesn't exceed collateral value (bad debt creation)",
            "Verify partial liquidation is supported to minimize borrower loss",
            "Check for liquidation cascades under volatile conditions",
            "Verify close factor limits prevent over-liquidation",
            "Audit for self-liquidation gaming",
        ],
        confidence_boost_keywords=["lending", "borrow", "collateral", "debt", "health"],
    ),

    PatternSignature(
        slug="cross-chain-message-passing",
        title="Cross-Chain Bridge & Messaging",
        severity="High",
        detectors=[
            r"\bbridge\b",
            r"\bcrossChain\b",
            r"\bsendMessage\b",
            r"\breceiveMessage\b",
            r"\brelayer\b",
            r"\bLayerZero\b",
            r"\bCCIP\b",
            r"\bAxelar\b",
        ],
        checklist=[
            "Verify message sender validation (source chain + source address)",
            "Check for replay protection on received messages",
            "Verify bridge token accounting matches actual transfers",
            "Check for finality assumptions — are L2→L1 messages waited on properly?",
            "Audit relayer trust assumptions — can a malicious relayer forge messages?",
            "Verify no re-initialization of bridge on destination chain",
        ],
        confidence_boost_keywords=["chain", "message", "relay", "bridge", "cross"],
    ),

    PatternSignature(
        slug="denial-of-service-gas-griefing",
        title="Denial of Service & Gas Griefing",
        severity="High",
        detectors=[
            r"\bfor\s*\(",           # loops
            r"\bwhile\s*\(",
            r"\.length\b",           # unbounded array iteration
            r"\bpush\b",
            r"\bgasleft\b",
        ],
        checklist=[
            "Check for unbounded loops over user-controlled arrays",
            "Verify external calls inside loops have gas limits (pull > push pattern)",
            "Check that failed transfers in a loop don't revert the entire batch",
            "Verify block gas limit cannot be exceeded by any single transaction",
            "Audit for returnbomb attacks (external call returning excessive data)",
            "Check that require() messages aren't excessively long (gas cost)",
        ],
        confidence_boost_keywords=["loop", "array", "iterate", "batch", "gas"],
    ),

    PatternSignature(
        slug="amm-constant-product-invariant",
        title="AMM / DEX Logic",
        severity="High",
        detectors=[
            r"\bswap\b",
            r"\bgetAmountOut\b",
            r"\bgetAmountIn\b",
            r"\breserve[01]\b",
            r"\baddLiquidity\b",
            r"\bremoveLiquidity\b",
            r"\bk\s*=\s*",          # invariant check
        ],
        checklist=[
            "Verify constant product invariant (k) is maintained after every swap",
            "Check for sandwich attack resistance (minimum output / slippage check)",
            "Verify fee accounting doesn't break the invariant",
            "Check for skim/sync manipulation (direct token transfers to pair)",
            "Audit for price manipulation via flash-swap callbacks",
            "Verify LP token minting math handles edge cases (first deposit, tiny amounts)",
        ],
        confidence_boost_keywords=["liquidity", "pool", "pair", "reserve", "swap"],
    ),

    PatternSignature(
        slug="timelock-governance-patterns",
        title="Timelock & Governance",
        severity="High",
        detectors=[
            r"\btimelock\b",
            r"\bTimelockController\b",
            r"\bpropose\b",
            r"\bexecute\b",
            r"\bqueue\b",
            r"\bGovernor\b",
        ],
        checklist=[
            "Verify minimum delay is enforced and cannot be set to 0",
            "Check that proposal execution requires quorum AND timelock passage",
            "Verify cancel functionality exists for malicious proposals",
            "Audit for flash loan governance attacks (borrow tokens, vote, return)",
            "Check that voting power is snapshot-based, not live balance",
            "Verify guardian/veto role for emergency shutdown",
        ],
        confidence_boost_keywords=["governance", "proposal", "vote", "delay", "execute"],
    ),

    PatternSignature(
        slug="merkle-proof-verification",
        title="Merkle Proof Verification",
        severity="Medium",
        detectors=[
            r"\bMerkleProof\b",
            r"\bmerkleRoot\b",
            r"\bverify\b.*\bproof\b",
            r"\bwhitelist\b",
            r"\bairdrop\b",
        ],
        checklist=[
            "Verify leaf encoding prevents second-preimage attacks (hash internal vs leaf nodes differently)",
            "Check that claims are marked as used (prevent double-claiming)",
            "Verify merkle root can be updated by admin but not front-run",
            "Check for proof manipulation via sorted pair hashing",
            "Audit claim deadline enforcement",
        ],
        confidence_boost_keywords=["proof", "root", "claim", "leaf", "tree"],
    ),

    PatternSignature(
        slug="account-abstraction-erc4337",
        title="Account Abstraction (ERC-4337)",
        severity="Medium",
        detectors=[
            r"\bUserOperation\b",
            r"\bEntryPoint\b",
            r"\bvalidateUserOp\b",
            r"\bpaymaster\b",
            r"\bbundler\b",
            r"\bIAccount\b",
        ],
        checklist=[
            "Verify validateUserOp returns correct sigTimeRange values",
            "Check paymaster signature validation and gas sponsorship limits",
            "Verify nonce management prevents replay of UserOperations",
            "Audit execution phase for unexpected reverts (griefing bundlers)",
            "Check storage access rules compliance (ERC-7562)",
        ],
        confidence_boost_keywords=["account", "wallet", "operation", "entrypoint"],
    ),
]


def get_all_signatures() -> list[PatternSignature]:
    """Return all registered pattern signatures."""
    return SIGNATURES


def get_signature(slug: str) -> PatternSignature | None:
    """Get a specific pattern signature by slug."""
    for sig in SIGNATURES:
        if sig.slug == slug:
            return sig
    return None
