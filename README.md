<div align="center">

<img width="100%" src="assets/profile-header.svg" alt="Rajveer Vadnal — Agentic Systems Engineer building verifiable agents, local-first AI tools, and developer infrastructure" />

<p>
  <a href="https://rajveervadnal.netlify.app/Rajveer_Vadnal_Resume.pdf"><img src="https://img.shields.io/badge/Resume-0d1117?style=for-the-badge&logo=adobeacrobatreader&logoColor=ed542e" alt="Resume" /></a>
  <a href="https://rajveervadnal.netlify.app/"><img src="https://img.shields.io/badge/Portfolio-0d1117?style=for-the-badge&logo=vercel&logoColor=38bdf8" alt="Portfolio" /></a>
  <a href="mailto:rajveer.r.vadnal@gmail.com"><img src="https://img.shields.io/badge/Email-0d1117?style=for-the-badge&logo=gmail&logoColor=EA4335" alt="Email" /></a>
  <a href="https://www.linkedin.com/in/rajveer-vadnal-374664353"><img src="https://img.shields.io/badge/LinkedIn-0d1117?style=for-the-badge&logo=linkedin&logoColor=0A66C2" alt="LinkedIn" /></a>
  <a href="https://github.com/Rajveerx11?tab=repositories"><img src="https://img.shields.io/badge/Repositories-0d1117?style=for-the-badge&logo=github&logoColor=white" alt="Repositories" /></a>
</p>

**Diploma completed · Entering AI & ML at SIT Hyderabad (direct second-year admission) · Solapur / Hyderabad, India**<br />
**Founder at [neuratile](https://github.com/neuratile) · Open to AI & Agentic Engineering opportunities**

</div>

## What I do

I build AI systems that must do more than generate plausible output: they need to **use tools, preserve context, expose evidence, and survive verification**.

My work sits at the intersection of agent orchestration, developer infrastructure, local-first AI, and product engineering. I build across Python, TypeScript, and Rust.

> **Current focus**: Verifiable coding agents, MCP infrastructure, local model evaluation, and tools that help engineers understand unfamiliar systems.

## Selected work

### ⚡ [Proof-of-Work](https://github.com/Rajveerx11/proof-of-work) · Coding-Agent Verification Gate

A CLI, Git hook, and GitHub Action that re-runs checks, catches deleted or weakened tests, and records signed verdicts.

[![PyPI Version](https://img.shields.io/pypi/v/proof-of-work-agent?color=38bdf8&style=flat-square&logo=pypi)](https://pypi.org/project/proof-of-work-agent/)
[![License](https://img.shields.io/badge/License-Apache_2.0-ed542e?style=flat-square)](https://github.com/Rajveerx11/proof-of-work/blob/main/LICENSE)
[![CI](https://img.shields.io/badge/CI-Passing-3fb950?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/Rajveerx11/proof-of-work/actions)

- **Verified evidence:** Published **[60 runs across 3 agent configurations on 20 tasks](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent)**: Codex 20/20, Copilot 20/20, OpenCode 17/20. One attempt per task and configuration; environment-specific comparison with zero estimated scores.
- **Tamper-evident log:** Results are hash-chained (`SHA-256`) and Ed25519-signed in SQLite; verifiable locally anytime via `proof-of-work verify-log`.
- **Mutation testing:** Integrated `mutmut` mutation testing to detect gutted test suites and coverage drops.
- **Tech stack:** `Python` `FastMCP` `SQLite` `Ed25519` `GitHub Actions` `PyPI`

---

### 🔍 [GFI Scout](https://github.com/Rajveerx11/gfi-scout) · Contributor-Focused MCP Server & CLI/TUI

Find open-source issues using repository health, maintainer responsiveness, freshness, and setup friction.

[![Tests](https://img.shields.io/badge/Tests-106_Passing-3fb950?style=flat-square&logo=pytest&logoColor=white)](https://github.com/Rajveerx11/gfi-scout/tree/main/tests)
[![Type Checked](https://img.shields.io/badge/Mypy-Strict-38bdf8?style=flat-square)](https://github.com/Rajveerx11/gfi-scout)
[![License](https://img.shields.io/badge/License-MIT-ed542e?style=flat-square)](https://github.com/Rajveerx11/gfi-scout/blob/main/LICENSE)

- **Verified evidence:** **4 FastMCP tools** (`find_issues`, `check_repo_health`, `check_issue_status`, `get_contribution_guide`) + shared CLI/TUI. Over 100 unit & integration tests passing in ~2s.
- **Architecture:** Async GitHub API pipeline, TTL caching, graceful rate-limit handling, and strict typing. [Watch demo](https://github.com/Rajveerx11/gfi-scout#readme) · [Architecture specs](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md).
- **Tech stack:** `Python` `FastMCP` `asyncio` `Rich / Textual` `GitHub API`

---

### 🛡️ [Tessera](https://github.com/neuratile/Tessera) · Local-First AI Testing IDE

A Rust/Tauri desktop app built at neuratile: retrieve code context, generate structured QA artifacts, and optionally run generated tests in network-isolated Docker containers.

[![Website](https://img.shields.io/badge/Website-tesseraide.vercel.app-38bdf8?style=flat-square)](https://tesseraide.vercel.app/)
[![Platform](https://img.shields.io/badge/Platform-Tauri_v2_Desktop-24c8db?style=flat-square)](https://github.com/neuratile/Tessera)
[![Architecture](https://img.shields.io/badge/Architecture-Local--First-3fb950?style=flat-square)](https://github.com/neuratile/Tessera#architecture)

- **Core contributions:** Implemented the [mutation-testing engine and scoring flow](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704), the [test-improvement loop](https://github.com/neuratile/Tessera/commit/6cdbc5b3b0e0432f328451f949e5ab12c9d83fac), and [persisted self-heal history](https://github.com/neuratile/Tessera/commit/9ec127a71b818296b5ac201a2bfd7e926e69a206).
- **Contract-driven generation:** AST parsing with Tree-sitter, local embeddings with Ollama, structured outputs validated by Zod schemas, optional sandboxed Docker runner.
- **Tech stack:** `Rust` `Tauri v2` `React` `Tree-sitter` `Ollama` `Docker`

---

### 🧠 [Obsidian Graph Intelligence](https://github.com/Rajveerx11/obsidian-graph-intelligence) · Offline Knowledge-Graph Analytics

Local-first knowledge-graph analysis, offline neural embeddings, and vault repair with an opt-in MCP query layer.

[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local_Embeddings-3fb950?style=flat-square)](https://github.com/Rajveerx11/obsidian-graph-intelligence)
[![Integration](https://img.shields.io/badge/Integration-MCP_Compatible-38bdf8?style=flat-square)](https://github.com/Rajveerx11/obsidian-graph-intelligence)

- **Verified evidence:** 100% offline Transformers.js neural embeddings on-device, graph topological analysis for cluster detection, automated *"Fix My Vault"* batch repair engine, and local Ollama/OpenAI MCP server.
- **Privacy-first:** Personal knowledge stays entirely on-device; bridges to models only through explicit user-approved MCP queries.
- **Tech stack:** `TypeScript` `React` `Transformers.js` `Obsidian API` `MCP`

---

### Reviewer verification matrix

| System | Primary architecture | Verified evidence & reviewer signals |
|---|---|---|
| **[Proof-of-Work](https://github.com/Rajveerx11/proof-of-work)** | Python · CI/CD · SQLite · Ed25519 | **[Published on PyPI](https://pypi.org/project/proof-of-work-agent/)** (`proof-of-work-agent`). Evaluated on **[60 runs across 3 agent configs on 20 tasks](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent)** (Codex 20/20, Copilot 20/20, OpenCode 17/20). Catches deleted/weakened tests via `mutmut` mutation testing. Emits hash-chained SQLite audit logs with Ed25519 DSSE signatures. |
| **[GFI Scout](https://github.com/Rajveerx11/gfi-scout)** | Python · FastMCP · asyncio · Rich/Textual | **4 FastMCP tools** (`find_issues`, `check_repo_health`, `check_issue_status`, `get_contribution_guide`) + shared CLI/TUI. **[106 automated tests](https://github.com/Rajveerx11/gfi-scout/tree/main/tests)**, strict mypy typing, async GitHub API pipeline with TTL caching. [Watch demo](https://github.com/Rajveerx11/gfi-scout#readme) · [Architecture](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md). |
| **[Tessera](https://github.com/neuratile/Tessera)** | Rust · Tauri v2 · React · Tree-sitter · Ollama | **Local-first AI testing IDE**. Implemented the [mutation-testing engine and scoring flow](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704), [test-improvement loop](https://github.com/neuratile/Tessera/commit/6cdbc5b3b0e0432f328451f949e5ab12c9d83fac), and [persisted self-heal history](https://github.com/neuratile/Tessera/commit/9ec127a71b818296b5ac201a2bfd7e926e69a206). Optional sandboxed Docker runner. [Product website](https://tesseraide.vercel.app/). |
| **[Obsidian Graph Intelligence](https://github.com/Rajveerx11/obsidian-graph-intelligence)** | TypeScript · React · Transformers.js · MCP | **100% offline Transformers.js embeddings**. Graph topological analysis for orphan notes and missing link discovery, automated *"Fix My Vault"* batch repair engine, and local Ollama/OpenAI MCP server. |

## Technical arsenal

| Category | Production working set |
|---|---|
| **Agent systems & evals** | Model Context Protocol (MCP), FastMCP, tool calling & orchestration, structured schema validation (Zod, JSON Schema), deterministic eval gates, anti-tampering verification, RAG, prompt caching |
| **Languages & core** | Python (asyncio, uv, mypy, pytest), TypeScript / JavaScript, Rust (Cargo, Clippy, Tauri), Kotlin (Android Jetpack) |
| **Local AI & code intelligence** | Ollama (local model inference), Transformers.js (in-browser / on-device embeddings), Tree-sitter (AST parsing), PyTorch, graph analytics (topological clustering, centrality) |
| **Systems & desktop** | Tauri (Rust desktop runtime), SQLite (WAL mode, hash-chained log stores), Docker, Node.js, React, Next.js, Flask |
| **Delivery & security** | GitHub Actions (CI/CD pipelines), mutation testing (`mutmut`), Ed25519 DSSE signing, PyPI packaging, Vercel, Netlify |

## How I work

- **Evidence before claims.** Tests, typed contracts, reproducible check re-runs, and inspectable outputs beat “it seems to work.” See the [evaluation methodology](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md).
- **Review the edge cases.** Catching cancellation bugs, operator coverage regressions, and state leaks before shipping. See Tessera's mutation-testing regression checks in the [merged change](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704).
- **Local-first when privacy matters.** Keep source code, embeddings, and user data on-device by default; make cloud boundaries explicit and auditable.
- **Agents as systems, not prompts.** Design the tools, state machines, error recovery, verification gates, and human approval points around the model.

## Product & research work

- **[neuratile](https://github.com/neuratile)** — AI-first developer tools organization. Leading **[Tessera](https://github.com/neuratile/Tessera)**, the local-first AI testing IDE.
- **[Master Models](https://github.com/Rajveerx11/Master-Models)** — Specialist-model evaluation benchmark across 5 developer roles (Frontend, Backend, Security Review, Code Review, Testing & QA) with 100 frozen repository tasks.
- **[Visage AI](https://getvisageai.online)** — Consumer AI mobile product for previewing aesthetic and cosmetic procedure outcomes. Public product experience, private source.

## Public and selected private builds

<div align="center">

<a href="https://github.com/Rajveerx11?tab=repositories"><img width="100%" src="assets/project-index.svg" alt="Live index of Rajveer Vadnal's public repositories and intentionally disclosed private builds" /></a>

<sub>Public data refreshes from GitHub daily. Private names come from an explicit allowlist (<code>data/private-projects.json</code>); their source code remains private.</sub>

</div>

## GitHub activity footprint

<div align="center">

<img width="100%" src="assets/github-stats.svg" alt="Live GitHub statistics: contributions, commits, merged pull requests, stars, followers, repositories, and top languages" />

</div>

## Contact & collaboration

Building an agentic-AI product, MCP integration, developer tool, or local-first AI system? Let's connect:

<div align="center">

<a href="mailto:rajveer.r.vadnal@gmail.com"><img src="https://img.shields.io/badge/Email_Directly-ed542e?style=for-the-badge&logo=gmail&logoColor=white" alt="Email Directly" /></a>
<a href="https://www.linkedin.com/in/rajveer-vadnal-374664353"><img src="https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Connect on LinkedIn" /></a>
<a href="https://rajveervadnal.netlify.app/"><img src="https://img.shields.io/badge/Explore_Portfolio-0d1117?style=for-the-badge&logo=vercel&logoColor=38bdf8" alt="Explore Portfolio" /></a>

</div>
