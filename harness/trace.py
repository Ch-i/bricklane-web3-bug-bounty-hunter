"""On-chain transaction trace replay via `cast run --trace`.

For post-mortem audits of deployed protocols, the most dramatic
demonstration of a bug is the actual exploit transaction replayed
step-by-step. ``cast run --trace`` forks the chain at the tx's block,
executes the tx in an Anvil-style sandbox, and emits a hierarchical
call trace with state diffs.

This is the DAoB "rerun the crash input under a debugger" analog.

Usage (CLI):
    python -m harness.trace <chain> <tx_hash>
    python -m harness.trace mainnet 0xabc...

Usage (programmatic):
    result = replay_tx("0xabc...", "mainnet")
    result.trace_text        # full annotated trace
    result.success           # tx succeeded vs reverted
    result.gas_used          # int
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# Chain id -> default JSON-RPC URL. Mirrors harness.onchain.DEFAULT_RPCS so
# trace and source-fetch share the same network defaults.
CHAIN_RPCS = {
    1: "https://eth.llamarpc.com",
    10: "https://mainnet.optimism.io",
    137: "https://polygon-rpc.com",
    42161: "https://arb1.arbitrum.io/rpc",
    8453: "https://mainnet.base.org",
    11155111: "https://ethereum-sepolia-rpc.publicnode.com",
}
CHAIN_NAMES = {
    "mainnet": 1,
    "ethereum": 1,
    "optimism": 10,
    "polygon": 137,
    "arbitrum": 42161,
    "base": 8453,
    "sepolia": 11155111,
}

TX_HASH_RE = re.compile(r"^0x[a-fA-F0-9]{64}$")


@dataclass
class TraceResult:
    chain_id: int
    tx_hash: str
    trace_text: str
    stdout: str
    stderr: str
    rc: int
    success: bool
    gas_used: int | None = None


def _cast_bin() -> str | None:
    for c in (Path(sys.prefix) / "bin" / "cast", Path.home() / ".foundry" / "bin" / "cast"):
        if c.is_file() and os.access(c, os.X_OK):
            return str(c)
    return shutil.which("cast")


def _rpc_url(chain_id: int) -> str:
    env_key = f"W3S_RPC_{chain_id}"
    return os.environ.get(env_key) or CHAIN_RPCS.get(chain_id) or CHAIN_RPCS[1]


def chain_to_id(chain: str | int) -> int:
    if isinstance(chain, int):
        return chain
    s = str(chain).lower().strip()
    if s.isdigit():
        return int(s)
    if s in CHAIN_NAMES:
        return CHAIN_NAMES[s]
    raise ValueError(f"unknown chain: {chain}")


def replay_tx(
    tx_hash: str,
    chain: str | int = "mainnet",
    *,
    timeout_seconds: int = 180,
) -> TraceResult:
    """Run `cast run --trace <hash>` against the chain's RPC."""
    if not TX_HASH_RE.match(tx_hash):
        raise ValueError(f"invalid tx hash: {tx_hash}")

    chain_id = chain_to_id(chain)
    rpc = _rpc_url(chain_id)
    cast = _cast_bin()
    if not cast:
        raise FileNotFoundError("cast not on PATH (install Foundry via foundryup)")

    cmd = [cast, "run", "--trace", "--rpc-url", rpc, tx_hash]
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join(
        [str(Path(sys.prefix) / "bin"), str(Path.home() / ".foundry" / "bin"), env.get("PATH", "")]
    )

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return TraceResult(
            chain_id=chain_id,
            tx_hash=tx_hash,
            trace_text="",
            stdout="",
            stderr=f"cast run timed out after {timeout_seconds}s",
            rc=-1,
            success=False,
        )

    # cast run's trace goes to stdout. Parse a few summary signals out.
    out = proc.stdout
    success_match = re.search(r"^Status:\s*(\d+)", out, re.MULTILINE) or re.search(
        r"Transaction successfully executed", out
    )
    success = False
    if success_match:
        if success_match.re.pattern.startswith("^Status"):
            success = success_match.group(1) == "1"
        else:
            success = True
    gas_used = None
    g = re.search(r"Gas used:\s*(\d+)", out)
    if g:
        try:
            gas_used = int(g.group(1))
        except ValueError:
            pass

    return TraceResult(
        chain_id=chain_id,
        tx_hash=tx_hash,
        trace_text=out,
        stdout=out,
        stderr=proc.stderr,
        rc=proc.returncode,
        success=success,
        gas_used=gas_used,
    )


def replay_to_run_dir(
    tx_hash: str,
    chain: str | int,
    run_dir: Path,
) -> Path:
    """Convenience: replay and persist to ``run_dir/trace-<short>.log``."""
    result = replay_tx(tx_hash, chain)
    out_path = run_dir / f"trace-{tx_hash[:12]}.log"
    header = (
        f"# cast run --trace {tx_hash} (chain={result.chain_id})\n"
        f"# rc={result.rc} success={result.success} gas_used={result.gas_used}\n"
        f"# ---\n"
    )
    out_path.write_text(header + result.trace_text)
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chain", help="Chain name or id (mainnet | optimism | ... | <chain-id>).")
    parser.add_argument("tx_hash", help="0x-prefixed 32-byte tx hash.")
    parser.add_argument("--out", help="Optional output path; defaults to stdout.")
    args = parser.parse_args(argv)

    try:
        result = replay_tx(args.tx_hash, args.chain)
    except (FileNotFoundError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.out:
        Path(args.out).write_text(result.trace_text)
        print(f"trace written to {args.out} (rc={result.rc} success={result.success})")
    else:
        sys.stdout.write(result.trace_text)
    return 0 if result.rc == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
