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

<a href="https://github.com/Rajveerx11/proof-of-work"><img width="100%" src="assets/built-proof-of-work.svg" alt="Proof-of-Work — verification gate for AI coding agents with deterministic checks, real test reruns, mutation testing, and signed audit logs" /></a>

<a href="https://github.com/Rajveerx11/gfi-scout"><img width="100%" src="assets/built-gfi-scout.svg" alt="GFI Scout — MCP server and CLI that ranks good-first issues by likelihood of contributor success" /></a>

<a href="https://github.com/neuratile/Tessera"><img width="100%" src="assets/built-tessera.svg" alt="Tessera — local-first AI testing IDE built with Rust, Tauri, React, Tree-sitter, and Ollama" /></a>

<a href="https://github.com/Rajveerx11/obsidian-graph-intelligence"><img width="100%" src="assets/built-obsidian.svg" alt="Obsidian Graph Intelligence — local knowledge-graph analysis, semantic linking, vault repair, and MCP queries" /></a>

| System | Primary architecture | Verified evidence & reviewer signals |
|---|---|---|
| **[Proof-of-Work](https://github.com/Rajveerx11/proof-of-work)** | Python · CI/CD · SQLite · Ed25519 | **[Published on PyPI](https://pypi.org/project/proof-of-work-agent/)** (`proof-of-work-agent`). Evaluated on **[60 runs across 3 agent configurations on 20 tasks](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent)** (Codex 20/20, Copilot 20/20, OpenCode 17/20). Catches deleted/weakened tests via `mutmut` mutation testing. Emits hash-chained SQLite audit logs with Ed25519 DSSE signatures. |
| **[GFI Scout](https://github.com/Rajveerx11/gfi-scout)** | Python · FastMCP · asyncio · Rich/Textual | **4 FastMCP tools** (`find_issues`, `check_repo_health`, `check_issue_status`, `get_contribution_guide`) + shared CLI/TUI. **[Unit & integration tests](https://github.com/Rajveerx11/gfi-scout/tree/main/tests)** (100+ tests), strict mypy typing, async GitHub API pipeline with TTL caching. [Watch demo](https://github.com/Rajveerx11/gfi-scout#readme) · [Architecture](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md). |
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
