# Case Study: Bricklane Web3 Bug Bounty Hunter

**AI-native bug bounty operations platform with a self-growing exploit corpus.**

---

## The One-Liner

Bricklane is an AI-augmented research and submission pipeline for Web3 security bounties, grounded in over 8,000+ real-world exploits. It continuously crawls active Code4rena, Sherlock, Cantina, and Immunefi opportunities, scores targets to isolate high-yield programs, performs dual-model audits backed by verified corpus citations, and exports submission-ready markdown reports.

---

## The Problem: The Fragmented Auditor Loop

In smart contract auditing and bug bounty hunting, security researchers face a fragmented workflow:

* **Information Asymmetry**: Attack prior art is scattered across post-mortems, whitepapers, databases (Solodit, SWC, rekt.news), and academic preprints. Cross-referencing current targets with historical bugs requires constant tab-switching.
* **Static Tool Noise**: Static analysis tools (like Slither and Aderyn) flood the researcher with low-priority warnings while missing complex multi-contract logic and economic exploits.
* **LLM Hallucinations**: Standard LLM prompting misses protocol-specific context, invents non-existent functions, and hallucinates citations.
* **Operations Overhead**: Formatting reports to fit unique platform-specific submission schemas (Code4rena vs. Sherlock vs. Immunefi) adds manual friction to every single draft.

---

## The Solution: A Grounded Auditing Engine

Bricklane consolidates research, static scans, LLM orchestration, and template formatting into a single, cohesive terminal and web dashboard:

```
  Intelligence           Triage             Audit             Submit
 ┌────────────┐      ┌────────────┐     ┌────────────┐     ┌────────────┐
 │ 8K+ Exploit│      │  Stage 1   │     │ Dual-Model │     │ Platform   │
 │   Corpus   │ ───> │   Ranker   │ ──> │   Audits   │ ───> │ Templates  │
 │ SQLite FTS5│      │ (Opus/1-10)│     │ & Citations│     │ (C4/Immun) │
 └────────────┘      └────────────┘     └────────────┘     └────────────┘
```

1. **Auto-Growing Exploits Corpus**: Crawls and indexes 8 distinct vulnerability databases into an 8,488-entry SQLite FTS5 search index.
2. **Stage 1 Triage Ranker**: Analyzes danger primitives (e.g., inline assembly, `delegatecall`, custom token transfers) alongside historical similarities to grade incoming contest codebases from 1 to 10.
3. **Dual-Model Audit Reconciliation**: Audits contract targets using Claude and Codex in parallel. A second-opinion filter agent merges findings, flags disagreements, and validates citations against the database to eliminate hallucinations.
4. **Interactive Exploits Simulator**: Models complex multi-contract attack graphs and transaction traces inside the React frontend.
5. **Auto-Scaffolded PoC**: Auto-generates Foundry test scripts (`.t.sol` files) to accelerate exploit reproduction.

---

## Technical Architecture & Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & Ingestion** | Python 3.11, FastAPI, SQLite (FTS5 + BM25), Pydantic |
| **Static Analyzers** | Slither, Aderyn, Foundry compiler tools |
| **Orchestration** | Claude CLI (Opus/Haiku), Codex API, Custom Filter Agent |
| **Frontend Web App** | React 19, Vite, Tailwind-ready custom CSS, Canvas force-directed graph |
| **Reproducibility** | Foundry (Forge test harness auto-scaffolding) |

---

## Current Status & Results

* **Corpus Density**: 8,488 curated exploits parsed, tagged, and indexed.
* **Triage Pipeline**: 170 active candidates cataloged and processed.
* **Dual-Model Audits**: 38 integration tests confirming recall accuracy on historical benchmarks (e.g., Euler finance donation exploit, classic reentrancy, Nomad bridge upgrade replay).
* **Maturity**: Bricklane functions as a high-fidelity research tool and submission draft factory. It is currently being targeted at active Code4rena contests to produce first-pass, citation-grounded submissions.
