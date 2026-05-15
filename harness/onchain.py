"""Fetch verified source for a deployed address from Sourcify (no auth) or
Etherscan v2 (key required). Handles EIP-1967 proxy chains transparently.

Used by ``harness.audit_runner prep`` when the user runs
``/audit 0x... --chain mainnet``.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import httpx

SOURCIFY_BASE = "https://sourcify.dev/server"
ETHERSCAN_BASE = "https://api.etherscan.io/v2/api"

# Default JSON-RPC endpoints per chain — used only for proxy-slot lookups.
# (Free, no key. Override via W3S_RPC_<CHAIN> env var.)
DEFAULT_RPCS = {
    1: "https://eth.llamarpc.com",
    10: "https://mainnet.optimism.io",
    137: "https://polygon-rpc.com",
    42161: "https://arb1.arbitrum.io/rpc",
    8453: "https://mainnet.base.org",
}

CHAIN_NAMES = {
    1: "mainnet",
    10: "optimism",
    137: "polygon",
    42161: "arbitrum",
    8453: "base",
    11155111: "sepolia",
}

# EIP-1967 storage slots (keccak("eip1967.proxy.implementation") - 1 etc.)
IMPL_SLOT = "0x360894a13ba1a3210667c828492db98dcef42c0b6c9c6e6a2c8c1f4b76e0e6e5"
ADMIN_SLOT = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"
BEACON_SLOT = "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"

ADDR_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


@dataclass
class FetchedContract:
    address: str
    chain_id: int
    name: str | None
    source_files: dict[str, str] = field(default_factory=dict)
    """Filename (preserving directory structure as a relative path) -> content."""
    compiler_version: str | None = None
    is_proxy: bool = False
    implementation_address: str | None = None
    implementation: "FetchedContract | None" = None
    fetched_via: str = "sourcify"  # "sourcify" | "etherscan"


def chain_to_id(chain: str | int) -> int:
    if isinstance(chain, int):
        return chain
    if chain.isdigit():
        return int(chain)
    for cid, name in CHAIN_NAMES.items():
        if name == chain.lower():
            return cid
    raise ValueError(f"unknown chain: {chain}")


def _rpc_url(chain_id: int) -> str:
    env_key = f"W3S_RPC_{chain_id}"
    return os.environ.get(env_key) or DEFAULT_RPCS.get(chain_id) or DEFAULT_RPCS[1]


# ---------------------------------------------------------------------------
# Source fetchers
# ---------------------------------------------------------------------------


def fetch_sourcify(address: str, chain_id: int) -> FetchedContract | None:
    """Try Sourcify. Returns None on 404; raises on transport error."""
    for match_type in ("full", "any"):
        url = f"{SOURCIFY_BASE}/files/{match_type}/{chain_id}/{address}"
        try:
            resp = httpx.get(url, timeout=30.0, follow_redirects=True)
        except httpx.HTTPError:
            continue
        if resp.status_code == 404:
            continue
        if resp.status_code != 200:
            continue
        data = resp.json()
        files = data.get("files") or []
        if not files:
            continue
        # Source files have paths like ".../sources/<rel>"; metadata.json is
        # auxiliary. We only need .sol files.
        sources: dict[str, str] = {}
        metadata: dict = {}
        for f in files:
            name = f.get("name", "")
            content = f.get("content", "")
            path = f.get("path", "")
            if name == "metadata.json":
                try:
                    metadata = json.loads(content)
                except json.JSONDecodeError:
                    pass
                continue
            if not name.endswith(".sol"):
                continue
            # Use the post-/sources/ tail as the relative path so multi-file
            # contracts keep their directory structure intact.
            rel = path.split("/sources/", 1)[1] if "/sources/" in path else name
            sources[rel] = content

        contract_name = None
        compiler = None
        if metadata:
            target = (metadata.get("settings", {}).get("compilationTarget") or {})
            if target:
                contract_name = next(iter(target.values()), None)
            compiler = metadata.get("compiler", {}).get("version")

        if sources:
            return FetchedContract(
                address=address,
                chain_id=chain_id,
                name=contract_name,
                source_files=sources,
                compiler_version=compiler,
                fetched_via=f"sourcify-{match_type}",
            )
    return None


def fetch_etherscan(address: str, chain_id: int) -> FetchedContract | None:
    """Fallback when Sourcify has no entry. Requires ETHERSCAN_API_KEY."""
    api_key = os.environ.get("ETHERSCAN_API_KEY")
    if not api_key:
        return None

    params = {
        "chainid": chain_id,
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key,
    }
    resp = httpx.get(ETHERSCAN_BASE, params=params, timeout=30.0)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") != "1" or not payload.get("result"):
        return None
    item = payload["result"][0]
    source = (item.get("SourceCode") or "").strip()
    if not source:
        return None

    contract_name = item.get("ContractName") or None
    compiler = item.get("CompilerVersion") or None

    sources: dict[str, str] = {}
    # Etherscan returns either:
    #   (a) flattened source as a plain string
    #   (b) JSON-encoded multi-file source wrapped in either `{...}` or `{{...}}`
    if source.startswith("{{") and source.endswith("}}"):
        source = source[1:-1]
    if source.startswith("{") and source.endswith("}"):
        try:
            parsed = json.loads(source)
            files = parsed.get("sources") or {}
            for path, payload in files.items():
                content = payload.get("content", "") if isinstance(payload, dict) else str(payload)
                sources[path] = content
        except json.JSONDecodeError:
            sources[f"{contract_name or 'Contract'}.sol"] = source
    else:
        sources[f"{contract_name or 'Contract'}.sol"] = source

    return FetchedContract(
        address=address,
        chain_id=chain_id,
        name=contract_name,
        source_files=sources,
        compiler_version=compiler,
        fetched_via="etherscan",
    )


# ---------------------------------------------------------------------------
# Proxy resolution
# ---------------------------------------------------------------------------


def _eth_get_storage_at(rpc_url: str, address: str, slot: str) -> str | None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getStorageAt",
        "params": [address, slot, "latest"],
    }
    try:
        resp = httpx.post(rpc_url, json=payload, timeout=15.0)
    except httpx.HTTPError:
        return None
    if resp.status_code != 200:
        return None
    data = resp.json()
    return data.get("result")


_HEX_RE = re.compile(r"^[0-9a-fA-F]+$")


def _slot_to_address(slot_value: str | None) -> str | None:
    """Extract the right-most 20 bytes of a 32-byte storage slot value.

    Returns None if the slot is the zero word, missing the 0x prefix,
    has non-hex characters, or is too short to contain a 20-byte address.
    """
    if not slot_value or not slot_value.startswith("0x"):
        return None
    raw = slot_value[2:]
    if not _HEX_RE.match(raw) or len(raw) < 40:
        return None
    addr = "0x" + raw.lower()[-40:]
    if addr == "0x" + "0" * 40:
        return None
    return addr


def detect_proxy(address: str, chain_id: int) -> str | None:
    """Read EIP-1967 implementation/beacon slot; return impl address or None."""
    rpc = _rpc_url(chain_id)
    impl_raw = _eth_get_storage_at(rpc, address, IMPL_SLOT)
    if impl_raw:
        addr = _slot_to_address(impl_raw)
        if addr:
            return addr
    beacon_raw = _eth_get_storage_at(rpc, address, BEACON_SLOT)
    if beacon_raw:
        beacon_addr = _slot_to_address(beacon_raw)
        if beacon_addr:
            # Beacon proxy: implementation lives behind a beacon contract.
            # Read its `implementation()` view (selector 0x5c60da1b).
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_call",
                "params": [
                    {"to": beacon_addr, "data": "0x5c60da1b"},
                    "latest",
                ],
            }
            try:
                resp = httpx.post(_rpc_url(chain_id), json=payload, timeout=15.0)
                impl = resp.json().get("result")
                return _slot_to_address(impl) if impl else None
            except httpx.HTTPError:
                return None
    return None


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------


def fetch_verified_source(
    address: str,
    chain: str | int = 1,
    *,
    resolve_proxy: bool = True,
) -> FetchedContract:
    """Resolve a deployed address to its verified source.

    Tries Sourcify first (free, no key) then Etherscan v2. If the contract is
    an EIP-1967 transparent / UUPS / beacon proxy, also fetches the
    implementation's source and chains it via ``implementation``.
    """
    if not ADDR_RE.match(address):
        raise ValueError(f"invalid address: {address}")
    chain_id = chain_to_id(chain)

    fetched = fetch_sourcify(address, chain_id)
    if fetched is None:
        fetched = fetch_etherscan(address, chain_id)
    if fetched is None:
        raise RuntimeError(
            f"no verified source for {address} on chain {chain_id} "
            f"(Sourcify miss; Etherscan {'key not set' if not os.environ.get('ETHERSCAN_API_KEY') else 'miss'})"
        )

    if resolve_proxy:
        impl_addr = detect_proxy(address, chain_id)
        if impl_addr:
            fetched.is_proxy = True
            fetched.implementation_address = impl_addr
            try:
                fetched.implementation = fetch_verified_source(
                    impl_addr, chain_id, resolve_proxy=False
                )
            except Exception:  # noqa: BLE001
                pass  # proxy detected but impl unverified — fine

    return fetched


def materialize_to_disk(fetched: FetchedContract, target_dir: Path) -> Path:
    """Write all source files to ``target_dir`` and return the path.

    Proxy: writes implementation's source under ``impl/`` so static tools
    can analyze both the proxy logic and the implementation.

    Also generates a minimal ``foundry.toml`` + ``remappings.txt`` so
    slither / forge can resolve ``@``-prefixed imports without manual setup.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    aliases: set[str] = set()
    for rel, content in fetched.source_files.items():
        # Track @-prefixed import roots so we can emit remappings for them.
        if rel.startswith("@"):
            head = rel.split("/", 1)[0]  # e.g. "@openzeppelin"
            aliases.add(head)
        # Strip the leading @ for filesystem safety (Sourcify file paths use
        # @ in imports; we mirror them as plain directories on disk).
        safe_rel = rel.lstrip("@/")
        out = target_dir / safe_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)

    if fetched.implementation:
        materialize_to_disk(fetched.implementation, target_dir / "impl")

    # Emit a foundry-style toolchain manifest so slither auto-detects the
    # project layout and resolves imports without remappings flags.
    if not (target_dir / "foundry.toml").exists():
        (target_dir / "foundry.toml").write_text(
            "[profile.default]\n"
            'src = "."\n'
            'out = "out"\n'
            'libs = []\n'
            "auto_detect_solc = true\n"
        )
    if aliases and not (target_dir / "remappings.txt").exists():
        lines = [f"{alias}/={alias[1:]}/" for alias in sorted(aliases)]
        (target_dir / "remappings.txt").write_text("\n".join(lines) + "\n")

    # Write a manifest so the auditor knows what they're looking at.
    manifest = {
        "address": fetched.address,
        "chain_id": fetched.chain_id,
        "chain": CHAIN_NAMES.get(fetched.chain_id, str(fetched.chain_id)),
        "contract_name": fetched.name,
        "compiler": fetched.compiler_version,
        "source": fetched.fetched_via,
        "is_proxy": fetched.is_proxy,
        "implementation_address": fetched.implementation_address,
        "file_count": len(fetched.source_files),
        "alias_remappings": sorted(aliases),
    }
    (target_dir / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    return target_dir
