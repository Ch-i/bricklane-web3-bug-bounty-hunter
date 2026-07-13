from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from pathlib import Path
import json
import glob

from harness import corpus as corpus_mod
from harness import candidates as cand_store
from harness import tui
from harness import autoresearch
from harness import scanner as scanner_mod
from harness import compositions

app = FastAPI(title="Bricklane API")

# Allow CORS for the Vite UI (usually runs on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPO_ROOT = Path(__file__).resolve().parent

@app.get("/api/stats")
def get_stats():
    """Aggregated stats for the dashboard."""
    # Corpus Stats
    try:
        c_stats = corpus_mod.stats()
    except Exception as e:
        c_stats = {"error": str(e)}

    # Queue Stats
    try:
        all_cands = cand_store.load_all()
        by_platform = {}
        by_status = {}
        for c in all_cands:
            by_platform[c.platform] = by_platform.get(c.platform, 0) + 1
            by_status[c.triage_status] = by_status.get(c.triage_status, 0) + 1
        q_stats = {
            "total_candidates": len(all_cands),
            "by_platform": by_platform,
            "by_status": by_status,
        }
    except Exception as e:
        q_stats = {"error": str(e)}

    # Recent Audits
    try:
        audits_root = REPO_ROOT / "audits"
        recent_runs = []
        if audits_root.exists():
            runs = tui._list_run_dirs(audits_root)[:10]
            for r in runs:
                s = tui._summary_row(r)
                # make path JSON serializable
                s["run_dir"] = str(s["run_dir"].name)
                recent_runs.append(s)
    except Exception as e:
        recent_runs = []

    return {
        "corpus": c_stats,
        "queue": q_stats,
        "recent_audits": recent_runs
    }

@app.get("/api/search")
def search_corpus(
    query: str,
    vuln_class: Optional[str] = None,
    severity: Optional[str] = None,
    source: Optional[str] = None,
    top_k: int = Query(20, le=100)
):
    """Full text search across the corpus."""
    try:
        v_classes = [vuln_class] if vuln_class else None
        sevs = [severity] if severity else None
        sources = [source] if source else None
        
        hits = corpus_mod.search(
            query=query,
            vuln_class=v_classes,
            severity=sevs,
            source=sources,
            top_k=top_k
        )
        return [{"id": h.id, "title": h.title, "source": h.source, "severity": h.severity, "snippet": h.snippet, "score": h.score} for h in hits]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/corpus/{entry_id}")
def get_corpus_entry(entry_id: str):
    """Get full details of a corpus entry."""
    entry = corpus_mod.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.get("/api/audits")
def list_audits():
    """List all audit runs."""
    try:
        audits_root = REPO_ROOT / "audits"
        runs = tui._list_run_dirs(audits_root)
        results = []
        for r in runs:
            s = tui._summary_row(r)
            s["run_dir"] = str(s["run_dir"].name)
            results.append(s)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audits/{run_id}")
def get_audit(run_id: str):
    """Get detailed info about a specific audit run."""
    audits_root = REPO_ROOT / "audits"
    run_dir = audits_root / run_id
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    
    try:
        s = tui._summary_row(run_dir)
        s["run_dir"] = str(s["run_dir"].name)
        prep = tui._load_prep(run_dir)
        findings = tui._load_findings(run_dir)
        static = tui._load_static_tools(run_dir)

        # Pipeline stages — which artifacts exist tells us how far the run got
        pipeline = []
        stage_files = [
            ("prep", "prep.json", "Preparation & target analysis"),
            ("static", "static-tools.json", "Static analysis (Slither, Aderyn, Foundry)"),
            ("auditor", "auditor-output.json", "Primary auditor (Claude)"),
            ("codex", "codex-output.json", "Cross-validator (Codex)"),
            ("reconciler", "reconciled.json", "Multi-model reconciliation"),
            ("findings", "findings.json", "Final findings extraction"),
            ("report", "report.md", "Markdown report generation"),
        ]
        for stage_id, filename, label in stage_files:
            fp = run_dir / filename
            pipeline.append({
                "id": stage_id,
                "label": label,
                "complete": fp.exists(),
                "file": filename,
            })

        return {
            "summary": s,
            "prep": prep,
            "findings": findings,
            "static_tools": static,
            "pipeline": pipeline,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audits/{run_id}/report")
def get_audit_report(run_id: str):
    """Return the markdown report for an audit run."""
    audits_root = REPO_ROOT / "audits"
    run_dir = audits_root / run_id
    report_path = run_dir / "report.md"
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return {"markdown": report_path.read_text()}


@app.get("/api/audits/{run_id}/findings/{finding_idx}")
def get_finding_detail(run_id: str, finding_idx: int):
    """Return full detail of a single finding by index."""
    audits_root = REPO_ROOT / "audits"
    run_dir = audits_root / run_id
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    findings = tui._load_findings(run_dir)
    if finding_idx < 0 or finding_idx >= len(findings):
        raise HTTPException(status_code=404, detail="Finding index out of range")

    f = findings[finding_idx]

    # Attach PoC log contents if available
    poc_logs = {}
    arts = f.get("poc_artifacts") or {}
    for key in ("stdout_log", "stderr_log"):
        log_rel = arts.get(key)
        if log_rel:
            log_path = run_dir / log_rel
            if log_path.exists():
                poc_logs[key] = log_path.read_text()[-5000:]  # tail 5k chars

    return {
        "finding": f,
        "poc_logs": poc_logs,
    }


# ---------------------------------------------------------------------------
# Library endpoints
# ---------------------------------------------------------------------------

@app.get("/api/library/patterns")
def list_patterns():
    """List all web3 logic patterns with their synthesis and contract status."""
    topics = autoresearch.get_topics_with_status()
    results = []
    for t in topics:
        # Check if synthesis note exists (uses alias resolution)
        synthesis_id = t.get("synthesis_id")
        has_synthesis = synthesis_id is not None

        # Check if contract exists
        contract_path = REPO_ROOT / "contracts" / "src" / "patterns" / f"{_slug_to_contract_name(t['slug'])}.sol"
        has_contract = contract_path.exists()

        results.append({
            "slug": t["slug"],
            "title": t["title"],
            "domain": t["domain"],
            "domain_label": autoresearch.DOMAINS.get(t["domain"], t["domain"]),
            "description": t["description"],
            "status": t["status"],
            "has_synthesis": has_synthesis,
            "has_contract": has_contract,
        })
    return results


_CONTRACT_MAP = {
    "amm-constant-product-invariant": "MinimalAmm",
    "flash-loan-mechanics": "FlashLoanReceiver",
    "erc4626-tokenized-vault-standard": "VaultErc4626",
}


def _slug_to_contract_name(slug: str) -> str:
    """Map a topic slug to its reference contract filename."""
    return _CONTRACT_MAP.get(slug, "".join(w.capitalize() for w in slug.split("-")))


@app.get("/api/library/patterns/{slug}")
def get_pattern(slug: str):
    """Full detail for a single logic pattern."""
    # Find the topic
    topic = None
    for t in autoresearch.TOPIC_QUEUE:
        if t.slug == slug:
            topic = t
            break
    if not topic:
        raise HTTPException(status_code=404, detail="Pattern not found")

    # Get synthesis note (resolve alias)
    synthesis_id = autoresearch._get_synthesis_id(topic)
    synthesis = corpus_mod.get_entry(synthesis_id) if synthesis_id else None

    # Get related corpus entries — SEVERITY-WEIGHTED SEARCH
    related_entries = []
    seen_ids = {synthesis_id} if synthesis_id else set()
    try:
        # First: pull Critical findings
        crit_hits = corpus_mod.search(
            query=topic.seed_query,
            severity="Critical",
            exclude_ids=list(seen_ids) if seen_ids else None,
            top_k=10,
        )
        for h in crit_hits:
            if h.id not in seen_ids:
                related_entries.append({"id": h.id, "title": h.title, "source": h.source, "severity": h.severity})
                seen_ids.add(h.id)

        # Second: pull High findings
        high_hits = corpus_mod.search(
            query=topic.seed_query,
            severity="High",
            exclude_ids=list(seen_ids) if seen_ids else None,
            top_k=10,
        )
        for h in high_hits:
            if h.id not in seen_ids:
                related_entries.append({"id": h.id, "title": h.title, "source": h.source, "severity": h.severity})
                seen_ids.add(h.id)

        # Third: fill with general results
        general_hits = corpus_mod.search(
            query=topic.seed_query,
            exclude_ids=list(seen_ids) if seen_ids else None,
            top_k=15,
        )
        for h in general_hits:
            if h.id not in seen_ids and len(related_entries) < 25:
                related_entries.append({"id": h.id, "title": h.title, "source": h.source, "severity": h.severity})
                seen_ids.add(h.id)

    except Exception:
        pass

    # Compute severity profile of related entries
    severity_counts = {}
    for e in related_entries:
        sev = (e.get("severity") or "Unknown").strip()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    crit_high = severity_counts.get("Critical", 0) + severity_counts.get("High", 0)
    total_entries = len(related_entries)
    critical_ratio = round(crit_high / total_entries, 2) if total_entries else 0

    # Get reference contract source
    contract_name = _slug_to_contract_name(slug)
    contract_path = REPO_ROOT / "contracts" / "src" / "patterns" / f"{contract_name}.sol"
    contract_source = None
    if contract_path.exists():
        contract_source = contract_path.read_text()

    return {
        "pattern": {
            "slug": topic.slug,
            "title": topic.title,
            "domain": topic.domain,
            "domain_label": autoresearch.DOMAINS.get(topic.domain, topic.domain),
            "description": topic.description,
            "seed_query": topic.seed_query,
        },
        "synthesis": synthesis,
        "related_entries": related_entries,
        "severity_profile": {
            "counts": severity_counts,
            "critical_ratio": critical_ratio,
            "crit_high_total": crit_high,
            "total": total_entries,
        },
        "contract_source": contract_source,
    }


@app.get("/api/library/domains")
def list_domains():
    """Domain summaries with pattern counts."""
    return autoresearch.get_domains_summary()


# ---------------------------------------------------------------------------
# Autoresearch endpoints
# ---------------------------------------------------------------------------

@app.get("/api/autoresearch/topics")
def autoresearch_topics():
    return autoresearch.get_topics_with_status()


@app.get("/api/autoresearch/domains")
def autoresearch_domains():
    return autoresearch.get_domains_summary()


@app.post("/api/autoresearch/run")
def autoresearch_run(n: int = Query(3, le=10)):
    """Trigger synthesis for the next N pending topics.
    Note: this runs synchronously and may take several minutes.
    """
    try:
        results = autoresearch.run_batch(n=n)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/autoresearch/live")
def autoresearch_live():
    """Return the current live process state (what's running right now)."""
    state_file = REPO_ROOT / "autoresearch-live.json"
    if not state_file.exists():
        return {"status": "idle", "current_topic": None, "completed_this_session": 0}
    try:
        return json.loads(state_file.read_text())
    except (json.JSONDecodeError, OSError):
        return {"status": "idle", "current_topic": None, "completed_this_session": 0}


@app.get("/api/autoresearch/logs")
def autoresearch_logs(
    tail: int = Query(100, le=500),
    after: Optional[str] = Query(None, description="ISO timestamp — only return entries after this")
):
    """Stream the autoresearch JSONL log. Returns the latest `tail` entries,
    or only entries after `after` timestamp for incremental polling."""
    log_file = REPO_ROOT / "autoresearch-log.jsonl"
    if not log_file.exists():
        return {"entries": [], "total": 0}

    lines = log_file.read_text().strip().splitlines()

    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if after:
        entries = [e for e in entries if e.get("ts", "") > after]

    # Return the latest `tail` entries
    entries = entries[-tail:]

    return {"entries": entries, "total": len(entries)}


@app.get("/api/autoresearch/synthesis-log/{slug}")
def synthesis_log(slug: str, tail: int = Query(200, le=1000)):
    """Return the raw synthesis subprocess output for a specific topic."""
    log_dir = REPO_ROOT / "audits" / f"synthesize-{slug}"
    if not log_dir.exists():
        raise HTTPException(status_code=404, detail="No synthesis log found")

    # Find stdout/stderr files
    result = {}
    for f in sorted(log_dir.iterdir()):
        if f.suffix in (".txt", ".log", ".json", ".md"):
            content = f.read_text()
            # Tail to last N lines
            lines = content.splitlines()
            result[f.name] = {
                "lines": lines[-tail:],
                "total_lines": len(lines),
                "truncated": len(lines) > tail,
            }
    return result


# ---------------------------------------------------------------------------
# Contract library endpoints
# ---------------------------------------------------------------------------

@app.get("/api/contracts")
def list_contracts():
    """List all reference contracts."""
    contracts_dir = REPO_ROOT / "contracts" / "src" / "patterns"
    if not contracts_dir.exists():
        return []
    results = []
    for sol_file in sorted(contracts_dir.glob("*.sol")):
        source = sol_file.read_text()
        # Extract NatSpec title from first /// @title line
        title = sol_file.stem
        for line in source.splitlines():
            if "@title" in line:
                title = line.split("@title")[-1].strip()
                break
        results.append({
            "name": sol_file.stem,
            "title": title,
            "size": len(source),
        })
    return results


@app.get("/api/contracts/{name}")
def get_contract(name: str):
    """Return full source of a reference contract."""
    contracts_dir = REPO_ROOT / "contracts" / "src" / "patterns"
    sol_file = contracts_dir / f"{name}.sol"
    if not sol_file.exists():
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"name": name, "source": sol_file.read_text()}


# ---------------------------------------------------------------------------
# Content enrichment endpoints (diagrams, videos)
# ---------------------------------------------------------------------------

CONTENT_DIR = REPO_ROOT / "content"


@app.get("/api/content/{slug}")
def get_content(slug: str):
    """Return all enriched content for a pattern (diagrams, video scripts, simulation)."""
    content_dir = CONTENT_DIR / slug
    result = {"slug": slug, "diagrams": None, "video_script": None, "simulation": None}

    diagrams_file = content_dir / "diagrams.json"
    if diagrams_file.exists():
        try:
            result["diagrams"] = json.loads(diagrams_file.read_text())
        except json.JSONDecodeError:
            pass

    video_file = content_dir / "video_script.py"
    if video_file.exists():
        result["video_script"] = video_file.read_text()

    sim_file = content_dir / "simulation.json"
    if sim_file.exists():
        try:
            result["simulation"] = json.loads(sim_file.read_text())
        except json.JSONDecodeError:
            pass

    return result


@app.post("/api/content/{slug}/generate")
def generate_content(slug: str, background_tasks: BackgroundTasks):
    """Trigger content enrichment (diagrams + video script) for a pattern."""
    import subprocess
    try:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/enrich_patterns.py", "--slug", slug],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        return {
            "status": "done" if result.returncode == 0 else "error",
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/content/generate-all")
def generate_all_content():
    """Trigger content enrichment for ALL synthesized patterns."""
    import subprocess
    try:
        result = subprocess.run(
            ["uv", "run", "python", "scripts/enrich_patterns.py", "--all"],
            capture_output=True, text=True, timeout=1800,
            cwd=str(REPO_ROOT),
        )
        return {
            "status": "done" if result.returncode == 0 else "error",
            "stdout": result.stdout[-5000:] if result.stdout else "",
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Contract scanner endpoints
# ---------------------------------------------------------------------------

class ScanRequest(BaseModel):
    source_code: str
    name: Optional[str] = "contract"


@app.post("/api/scan")
def scan_contract(req: ScanRequest):
    """Scan Solidity source code against all pattern signatures."""
    matches = scanner_mod.scan_source(req.source_code)
    return {
        "name": req.name,
        "total_patterns": len(matches),
        "critical": sum(1 for m in matches if m.severity == "Critical"),
        "high": sum(1 for m in matches if m.severity == "High"),
        "matches": [
            {
                "slug": m.slug,
                "title": m.title,
                "severity": m.severity,
                "confidence": m.confidence,
                "detector_hits": m.detector_hits,
                "total_hits": m.total_hits,
                "matched_lines": [
                    {"line_number": ml.line_number, "content": ml.content, "detector": ml.detector}
                    for ml in m.matched_lines
                ],
                "checklist": m.checklist,
            }
            for m in matches
        ],
    }


@app.get("/api/scan/signatures")
def list_signatures():
    """List all available pattern signatures."""
    from harness.signatures import SIGNATURES
    return [
        {
            "slug": s.slug,
            "title": s.title,
            "severity": s.severity,
            "detector_count": len(s.detectors),
            "checklist_count": len(s.checklist),
        }
        for s in SIGNATURES
    ]


# ---------------------------------------------------------------------------
# Attack composition graph endpoints
# ---------------------------------------------------------------------------

@app.get("/api/graph/compositions")
def get_composition_graph():
    """Return the full attack composition graph (nodes + edges)."""
    return compositions.get_graph_data()


# ---------------------------------------------------------------------------
# On-chain verification — query live block explorers & RPCs
# ---------------------------------------------------------------------------

CHAIN_CONFIG = {
    "Ethereum": {
        "explorer": "https://etherscan.io",
        "api": "https://api.etherscan.io/api",
        "rpcs": ["https://virginia.rpc.blxrbdn.com"],
        "symbol": "ETH",
    },
    "BSC": {
        "explorer": "https://bscscan.com",
        "api": "https://api.bscscan.com/api",
        "rpcs": ["https://bsc-dataseed1.binance.org", "https://bsc-dataseed2.binance.org"],
        "symbol": "BNB",
    },
    "Polygon": {
        "explorer": "https://polygonscan.com",
        "api": "https://api.polygonscan.com/api",
        "rpcs": ["https://polygon-rpc.com"],
        "symbol": "MATIC",
    },
    "Arbitrum": {
        "explorer": "https://arbiscan.io",
        "api": "https://api.arbiscan.io/api",
        "rpcs": ["https://arb1.arbitrum.io/rpc"],
        "symbol": "ETH",
    },
    "Optimism": {
        "explorer": "https://optimistic.etherscan.io",
        "api": "https://api-optimistic.etherscan.io/api",
        "rpcs": ["https://mainnet.optimism.io"],
        "symbol": "ETH",
    },
}


def _rpc_call(rpc_url, method, params):
    """Make a JSON-RPC call."""
    import urllib.request
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    req = urllib.request.Request(rpc_url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise Exception(data["error"].get("message", str(data["error"])))
    return data.get("result")


def _etherscan_get(api_url, params):
    """Query an Etherscan-family API."""
    import urllib.request, urllib.parse
    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Bricklane/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data


@app.get("/api/verify/tx/{chain}/{tx_hash}")
def verify_transaction(chain: str, tx_hash: str):
    """Query live mainnet to verify a transaction exists on-chain."""
    import urllib.request

    cfg = CHAIN_CONFIG.get(chain)
    if not cfg:
        raise HTTPException(status_code=400, detail=f"Unsupported chain: {chain}. Supported: {list(CHAIN_CONFIG.keys())}")

    explorer_base = cfg["explorer"]
    symbol = cfg["symbol"]
    receipt = None
    tx = None
    used_source = None

    # Strategy 1: Etherscan-family API (free, no key, full history)
    try:
        receipt_resp = _etherscan_get(cfg["api"], {
            "module": "proxy",
            "action": "eth_getTransactionReceipt",
            "txhash": tx_hash,
        })
        receipt = receipt_resp.get("result")

        tx_resp = _etherscan_get(cfg["api"], {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": tx_hash,
        })
        tx = tx_resp.get("result")

        if receipt and tx and isinstance(receipt, dict) and isinstance(tx, dict):
            used_source = cfg["api"]
    except Exception:
        receipt = None
        tx = None

    # Strategy 2: Fallback to raw JSON-RPC
    if not receipt or not tx or not isinstance(receipt, dict):
        for rpc_url in cfg["rpcs"]:
            try:
                receipt = _rpc_call(rpc_url, "eth_getTransactionReceipt", [tx_hash])
                tx = _rpc_call(rpc_url, "eth_getTransaction", [tx_hash])
                if receipt and tx:
                    used_source = rpc_url
                    break
            except Exception:
                continue

    if not receipt or not tx or not isinstance(receipt, dict):
        return {
            "verified": False,
            "chain": chain,
            "tx_hash": tx_hash,
            "error": "Transaction not found on chain — may be invalid or from a different chain",
            "explorer_url": f"{explorer_base}/tx/{tx_hash}",
        }

    # Parse hex values
    def hex_to_int(h):
        if not h:
            return 0
        return int(h, 16)

    def hex_to_eth(h):
        return round(hex_to_int(h) / 1e18, 6)

    block_number = hex_to_int(receipt.get("blockNumber", "0x0"))
    gas_used = hex_to_int(receipt.get("gasUsed", "0x0"))
    gas_price = hex_to_int(tx.get("gasPrice", "0x0"))
    tx_fee = round((gas_used * gas_price) / 1e18, 6)
    status_hex = receipt.get("status")
    status = "Success" if status_hex == "0x1" else "Reverted" if status_hex == "0x0" else "Pre-Byzantium (assumed success)"
    log_count = len(receipt.get("logs", []))

    unique_contracts = set()
    for log in receipt.get("logs", []):
        addr = log.get("address", "")
        if addr:
            unique_contracts.add(addr)

    return {
        "verified": True,
        "chain": chain,
        "tx_hash": tx_hash,
        "source": used_source,
        "explorer_url": f"{explorer_base}/tx/{tx_hash}",
        "on_chain": {
            "block_number": block_number,
            "from": tx.get("from", ""),
            "to": tx.get("to", ""),
            "status": status,
            "value": hex_to_eth(tx.get("value", "0x0")),
            "symbol": symbol,
            "gas_used": gas_used,
            "gas_price_gwei": round(gas_price / 1e9, 2),
            "tx_fee": tx_fee,
            "nonce": hex_to_int(tx.get("nonce", "0x0")),
            "log_count": log_count,
            "contracts_touched": len(unique_contracts),
            "contract_addresses": sorted(unique_contracts)[:20],
            "input_data_size": len(tx.get("input", "0x")) // 2 - 1 if tx.get("input") else 0,
        },
    }


