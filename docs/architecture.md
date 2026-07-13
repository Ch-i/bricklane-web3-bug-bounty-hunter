# Architecture

## System Overview

web3Sentinel is a security research platform that automatically builds a knowledge base from public vulnerability sources, then uses it to audit Solidity smart contracts with grounded, citation-backed findings.

```mermaid
graph TB
    subgraph "Data Ingestion Layer"
        CR1[Solodit Crawler] --> |findings| ING[Ingest Pipeline]
        CR2[arXiv Crawler] --> |papers| ING
        CR3[rekt.news Crawler] --> |post-mortems| ING
        CR4[Sherlock Crawler] --> |contest findings| ING
        CR5[Code4rena Crawler] --> |contest findings| ING
        CR6[Cantina Crawler] --> |audit findings| ING
        CR7[Immunefi Crawler] --> |bug bounties| ING
        CR8[SWC Registry] --> |standard weaknesses| ING
    end

    subgraph "Knowledge Base"
        ING --> CORPUS[(Corpus<br/>8,488 entries<br/>Markdown + YAML)]
        CORPUS --> DB[(SQLite<br/>FTS5 + Embeddings)]
        CORPUS --> SYN[Synthesis Engine]
        SYN --> PAT[28 Logic Patterns]
    end

    subgraph "Analysis Engine"
        DB --> SCAN[Pattern Scanner<br/>15 signatures]
        DB --> AUDIT[Audit Runner<br/>Multi-model parallel]
        AUDIT --> CIT[Citation Validator]
        AUDIT --> DD[Deep Dive]
        DD --> POC[PoC Generator]
        DB --> COMP[Composition Graph]
    end

    subgraph "Presentation Layer"
        API[FastAPI<br/>~20 endpoints] --> UI[React UI]
        SCAN --> API
        AUDIT --> API
        COMP --> API
        PAT --> API
        UI --> LIB[Pattern Library]
        UI --> AG[Attack Graph<br/>Canvas force-directed]
        UI --> SIM[Simulation Notebook]
        UI --> VER[On-Chain Verifier]
        UI --> DASH[Dashboard]
    end

    subgraph "External"
        VER --> |JSON-RPC| ETH[Ethereum Mainnet]
        VER --> |JSON-RPC| BSC[BSC]
        VER --> |JSON-RPC| POLY[Polygon]
        VER --> |Etherscan API| ESCAN[Block Explorers]
    end
```

## Data Flow

### 1. Ingestion

Each crawler in `crawlers/` implements a source-specific scraper:

```mermaid
sequenceDiagram
    participant Cron as Scheduler
    participant Crawler as Source Crawler
    participant Parser as Frontmatter Parser
    participant DB as SQLite + FTS5

    Cron->>Crawler: Run ingestion
    Crawler->>Crawler: Fetch new entries from source
    Crawler->>Parser: Parse to Markdown + YAML frontmatter
    Parser->>DB: Upsert with deduplication
    DB->>DB: Update FTS5 index
```

Corpus entries follow a standard schema:

```yaml
---
id: solodit-12345
title: "Reentrancy in Withdrawal Function"
source: solodit
severity: High
vuln_class: [reentrancy]
protocol_category: [lending]
tags: [checks-effects-interactions]
---
# Finding body in Markdown
```

### 2. Synthesis

The synthesis engine (`harness/synthesize.py`) cross-references corpus entries to build logic patterns:

- Groups entries by `vuln_class` and `protocol_category`
- Identifies common attack primitives across incidents
- Generates structured notes with `derives_from` citations
- Produces diagrams, video scripts, and simulation JSON

### 3. Auditing

```mermaid
sequenceDiagram
    participant User
    participant Runner as Audit Runner
    participant Scanner as Pattern Scanner
    participant LLM1 as Model A
    participant LLM2 as Model B
    participant Corpus as Corpus DB
    participant Validator as Citation Validator

    User->>Runner: Submit Solidity source
    Runner->>Scanner: Static pattern matching
    Scanner-->>Runner: Signature matches
    Runner->>Corpus: Retrieve relevant entries
    Corpus-->>Runner: Top-K by similarity
    Runner->>LLM1: Audit prompt + corpus context
    Runner->>LLM2: Audit prompt + corpus context
    LLM1-->>Runner: Findings with citations
    LLM2-->>Runner: Findings with citations
    Runner->>Validator: Verify all citations exist
    Validator-->>Runner: Validated report
    Runner-->>User: Final audit report
```

### 4. On-Chain Verification

The verification layer queries live blockchain nodes to prove incident data is real:

```
User clicks "Verify On-Chain"
  → API: GET /api/verify/tx/{chain}/{tx_hash}
    → Strategy 1: Etherscan API (full history, rate-limited)
    → Strategy 2: JSON-RPC fallback (recent blocks only)
  → Returns: block number, from/to, gas, status, event logs, contracts touched
```

## Key Modules

| Module | LOC | Purpose |
|---|---|---|
| `harness/audit_runner.py` | Core | Multi-model parallel audit orchestration |
| `harness/corpus.py` | Core | SQLite corpus with FTS5, embedding search |
| `harness/scanner.py` | Core | 15 vulnerability pattern signatures |
| `harness/compositions.py` | Core | Attack chain graph with incident mapping |
| `harness/deep_dive.py` | Analysis | Automated deep analysis of findings |
| `harness/poc.py` | Analysis | Proof-of-concept generation |
| `harness/citations.py` | Validation | Citation grounding verification |
| `harness/synthesize.py` | Synthesis | Cross-corpus pattern synthesis |
| `harness/autoresearch.py` | Automation | Research queue + batch processing |
| `api.py` | API | FastAPI with 20+ endpoints |

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLite + FTS5, Pydantic
- **Frontend**: React 19, Vite, Canvas API (force-directed graph)
- **Package Manager**: uv (Python), npm (JS)
- **Static Analysis**: Slither, Aderyn, Halmos, Mythril
- **CI**: GitHub Actions (pytest, ruff)
- **Data Format**: Markdown with YAML frontmatter
