"""On-chain reconnaissance toolkit.

For a target contract address, surface:
  * The deployment metadata (creator EOA, creation tx, block, compiler, source)
  * Recent transactions calling the contract — who interacted, how often
  * ERC20 / ERC721 token flows in and out (Transfer events)
  * The creator's other contracts (related deployments)
  * Contracts THIS contract calls (basic call-graph via tx traces)

Sources, in priority order:
  1. Sourcify (free, no API key)
  2. Etherscan v2 multichain API (needs ETHERSCAN_API_KEY for high-rate use)
  3. Public JSON-RPC (LlamaRPC defaults, override via W3S_RPC_<chain-id>)

Designed for use in notebooks (returns pandas DataFrames where useful).
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    import pandas as pd  # noqa: F401

from harness.onchain import (
    CHAIN_NAMES,
    DEFAULT_RPCS,
    chain_to_id,
    fetch_verified_source as _fetch_source,
)

ETHERSCAN_V2 = "https://api.etherscan.io/v2/api"
USER_AGENT = "web3sentinel-explorer/0.1"


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def _api_key() -> str | None:
    return os.environ.get("ETHERSCAN_API_KEY")


def _rpc_url(chain_id: int) -> str:
    return (
        os.environ.get(f"W3S_RPC_{chain_id}")
        or DEFAULT_RPCS.get(chain_id)
        or DEFAULT_RPCS[1]
    )


def _etherscan(params: dict, chain_id: int, timeout: float = 30.0) -> dict:
    """Single Etherscan v2 call. Raises if the API rejects."""
    p = {**params, "chainid": chain_id}
    if _api_key():
        p["apikey"] = _api_key()
    resp = httpx.get(ETHERSCAN_V2, params=p, timeout=timeout, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.json()


def _rpc(method: str, params: list, chain_id: int, timeout: float = 30.0) -> dict:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    resp = httpx.post(_rpc_url(chain_id), json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Deployment metadata
# ---------------------------------------------------------------------------


@dataclass
class DeploymentInfo:
    address: str
    chain_id: int
    chain_name: str
    creator: str | None
    creation_tx: str | None
    creation_block: int | None
    contract_name: str | None
    compiler: str | None
    is_proxy: bool = False
    implementation: str | None = None
    source_files: dict[str, str] = field(default_factory=dict)
    source_via: str | None = None


def get_deployment_info(address: str, chain: str | int = "mainnet") -> DeploymentInfo:
    """Resolve creator + source for a deployed contract."""
    chain_id = chain_to_id(chain)
    info = DeploymentInfo(
        address=address,
        chain_id=chain_id,
        chain_name=CHAIN_NAMES.get(chain_id, str(chain_id)),
        creator=None,
        creation_tx=None,
        creation_block=None,
        contract_name=None,
        compiler=None,
    )

    # Source + proxy from existing onchain module
    try:
        fetched = _fetch_source(address, chain=chain_id)
        info.contract_name = fetched.name
        info.compiler = fetched.compiler_version
        info.is_proxy = fetched.is_proxy
        info.implementation = fetched.implementation_address
        info.source_files = fetched.source_files
        info.source_via = fetched.fetched_via
    except Exception:  # noqa: BLE001
        pass

    # Creator + creation tx via Etherscan
    if _api_key():
        try:
            r = _etherscan(
                {"module": "contract", "action": "getcontractcreation", "contractaddresses": address},
                chain_id,
            )
            if r.get("status") == "1" and r.get("result"):
                row = r["result"][0]
                info.creator = row.get("contractCreator")
                info.creation_tx = row.get("txHash")
        except Exception:  # noqa: BLE001
            pass

    return info


# ---------------------------------------------------------------------------
# Recent transactions / participants
# ---------------------------------------------------------------------------


def recent_transactions(
    address: str,
    chain: str | int = "mainnet",
    n: int = 100,
    *,
    sort: str = "desc",
) -> list[dict]:
    """List the most-recent N transactions touching the address.

    Requires ETHERSCAN_API_KEY (Etherscan API has no free unauth tier for
    txlist queries). Returns raw Etherscan result dicts.
    """
    if not _api_key():
        raise RuntimeError(
            "recent_transactions needs ETHERSCAN_API_KEY in env; "
            "set it via `export ETHERSCAN_API_KEY=...` or in .env"
        )
    chain_id = chain_to_id(chain)
    r = _etherscan(
        {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": n,
            "sort": sort,
        },
        chain_id,
    )
    if r.get("status") not in ("1", 1) or not isinstance(r.get("result"), list):
        return []
    return r["result"]


def participants(
    address: str,
    chain: str | int = "mainnet",
    n: int = 1000,
) -> "pd.DataFrame":
    """Unique addresses that called the contract, with call counts + last-seen.

    Returns a pandas DataFrame indexed by `from` address, with columns
    `calls`, `eth_value_sent_wei`, `last_block`, `first_block`.
    """
    import pandas as pd
    txs = recent_transactions(address, chain, n=n)
    if not txs:
        return pd.DataFrame(columns=["calls", "eth_value_sent_wei", "first_block", "last_block"])
    df = pd.DataFrame(txs)
    df["blockNumber"] = df["blockNumber"].astype(int)
    df["value"] = df["value"].astype(int)
    agg = df.groupby("from").agg(
        calls=("hash", "count"),
        eth_value_sent_wei=("value", "sum"),
        first_block=("blockNumber", "min"),
        last_block=("blockNumber", "max"),
    ).sort_values("calls", ascending=False)
    return agg


# ---------------------------------------------------------------------------
# Token flows (ERC20 / ERC721 Transfer events)
# ---------------------------------------------------------------------------


def token_transfers(
    address: str,
    chain: str | int = "mainnet",
    n: int = 1000,
    kind: str = "erc20",
) -> "pd.DataFrame":
    """Transfer events with this address as `from` or `to`.

    kind: "erc20" or "erc721". Etherscan's tokentx vs tokennfttx endpoints.
    """
    import pandas as pd
    if not _api_key():
        raise RuntimeError("token_transfers needs ETHERSCAN_API_KEY")
    chain_id = chain_to_id(chain)
    action = "tokentx" if kind == "erc20" else "tokennfttx"
    r = _etherscan(
        {
            "module": "account",
            "action": action,
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": n,
            "sort": "desc",
        },
        chain_id,
    )
    if r.get("status") not in ("1", 1) or not isinstance(r.get("result"), list):
        return pd.DataFrame()
    df = pd.DataFrame(r["result"])
    if df.empty:
        return df
    for c in ("blockNumber", "timeStamp", "value", "tokenDecimal"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


# ---------------------------------------------------------------------------
# Creator's other deployments (related contracts)
# ---------------------------------------------------------------------------


def creator_deployments(
    creator: str,
    chain: str | int = "mainnet",
    n: int = 1000,
) -> list[dict]:
    """Other contracts deployed by the same EOA / factory.

    Heuristic: walk recent txs FROM the creator address, filter those with
    `to == ""` (contract creation) or `contractAddress != ""`. Returns
    Etherscan tx rows enriched with the deployed contract address.
    """
    if not _api_key():
        raise RuntimeError("creator_deployments needs ETHERSCAN_API_KEY")
    chain_id = chain_to_id(chain)
    txs = recent_transactions(creator, chain_id, n=n)
    deployments = []
    for t in txs:
        if (t.get("contractAddress") or "").strip() and (t.get("to") in ("", None)):
            deployments.append(t)
    return deployments


# ---------------------------------------------------------------------------
# Contracts THIS contract calls (call graph, 1-hop)
# ---------------------------------------------------------------------------


def _is_code(address: str, chain_id: int) -> bool:
    """True if address has bytecode (is a contract, not an EOA)."""
    r = _rpc("eth_getCode", [address, "latest"], chain_id)
    code = r.get("result") or "0x"
    return len(code) > 2  # "0x" alone is empty


def outgoing_call_targets(
    address: str,
    chain: str | int = "mainnet",
    n: int = 200,
) -> "pd.DataFrame":
    """Addresses this contract has called (1-hop call graph).

    Uses Etherscan's `txlistinternal` which captures internal calls.
    """
    import pandas as pd
    if not _api_key():
        raise RuntimeError("outgoing_call_targets needs ETHERSCAN_API_KEY")
    chain_id = chain_to_id(chain)
    r = _etherscan(
        {
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": n,
            "sort": "desc",
        },
        chain_id,
    )
    if r.get("status") not in ("1", 1) or not isinstance(r.get("result"), list):
        return pd.DataFrame()
    df = pd.DataFrame(r["result"])
    if df.empty:
        return df
    # Keep only outbound (from == our address)
    df = df[df["from"].str.lower() == address.lower()]
    df["blockNumber"] = pd.to_numeric(df["blockNumber"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    agg = df.groupby("to").agg(
        calls=("hash", "count"),
        eth_value_sent_wei=("value", "sum"),
        first_block=("blockNumber", "min"),
        last_block=("blockNumber", "max"),
    ).sort_values("calls", ascending=False)
    return agg


# ---------------------------------------------------------------------------
# Participant graph (NetworkX)
# ---------------------------------------------------------------------------


def participant_graph(
    address: str,
    chain: str | int = "mainnet",
    n: int = 500,
    *,
    include_internal: bool = True,
) -> "tuple":
    """Build a NetworkX directed graph: (participant -> contract).

    Returns (graph, nodes_metadata) where nodes_metadata is a dict
    address → {is_contract, calls, eth_sent_wei}.
    """
    import networkx as nx

    chain_id = chain_to_id(chain)
    G = nx.DiGraph()
    meta: dict[str, dict] = {}

    parts = participants(address, chain_id, n=n)
    # Add edges from each caller into the contract
    G.add_node(address.lower(), node_type="contract")
    meta[address.lower()] = {"is_contract": True}
    for caller, row in parts.iterrows():
        c = caller.lower()
        is_contract = False
        try:
            is_contract = _is_code(c, chain_id)
        except Exception:  # noqa: BLE001
            pass
        G.add_node(c, node_type="contract" if is_contract else "eoa")
        G.add_edge(c, address.lower(), calls=int(row["calls"]), eth_sent_wei=int(row["eth_value_sent_wei"]))
        meta[c] = {
            "is_contract": is_contract,
            "calls": int(row["calls"]),
            "eth_sent_wei": int(row["eth_value_sent_wei"]),
        }
        # Polite rate limit between eth_getCode probes
        time.sleep(0.05)

    if include_internal:
        try:
            out = outgoing_call_targets(address, chain_id, n=n)
            for target, row in out.iterrows():
                t = target.lower()
                if t and t != address.lower():
                    G.add_node(t, node_type="contract")
                    G.add_edge(address.lower(), t, calls=int(row["calls"]))
                    meta.setdefault(t, {})["is_contract"] = True
        except Exception:  # noqa: BLE001
            pass

    return G, meta


def draw_graph(G, meta: dict, ax=None, max_label_len: int = 8) -> None:
    """Quick matplotlib draw of the participant graph."""
    import matplotlib.pyplot as plt
    import networkx as nx

    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.6, iterations=40, seed=42)

    eoa_nodes = [n for n in G.nodes if (meta.get(n, {}).get("is_contract") is False)]
    contract_nodes = [n for n in G.nodes if (meta.get(n, {}).get("is_contract") is True)]

    nx.draw_networkx_nodes(G, pos, nodelist=eoa_nodes, node_color="#FACC15", node_size=80, ax=ax, label="EOA")
    nx.draw_networkx_nodes(G, pos, nodelist=contract_nodes, node_color="#6366F1", node_size=200, ax=ax, label="Contract")
    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, arrows=True, arrowsize=8)
    labels = {n: n[:max_label_len] + "…" for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
    ax.legend()
    ax.set_axis_off()
