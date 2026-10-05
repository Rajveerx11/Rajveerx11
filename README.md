# Rajveer Vadnal

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/profile-header-light.svg" />
  <img width="100%" src="assets/profile-header.svg" alt="Systems that can prove themselves. Rajveer Vadnal, agentic systems engineer building coding tools and local-first AI products." />
</picture>

I build coding tools and local-first AI products. My work focuses on context, controlled execution, and verification. My main languages are Python and TypeScript. I also use Rust.

[Portfolio](https://rajveervadnal.netlify.app/) · [Resume](https://rajveervadnal.netlify.app/Rajveer_Vadnal_Resume.pdf) · [LinkedIn](https://www.linkedin.com/in/rajveer-vadnal-374664353) · [Email](mailto:rajveer.r.vadnal@gmail.com)

Founder at [neuratile](https://github.com/neuratile), building developer tools including Tessera. Founder of [Visage AI](https://getvisageai.online/), an aesthetic outcome preview product.

**Education:** Diploma in Computer Science Engineering · B.Tech in Artificial Intelligence & Machine Learning

## Execution atlas

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/execution-atlas-mobile-light.svg" />
  <source media="(max-width: 600px)" srcset="assets/execution-atlas-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/execution-atlas-light.svg" />
  <img width="100%" src="assets/execution-atlas.svg" alt="Execution atlas: AgentWisper for human input; GFI Scout and RepoGraph for context; Neura for orchestration; Tessera for testing; Proof-of-Work for verification; Obsidian Graph Intelligence for memory. Human approval is an explicit boundary." />
</picture>

**Roles, not wiring.** The paths group my projects by purpose. They do not claim integrations between these repositories. Use the links below to inspect the work. The image itself is a static map.

| Territory | Project | What it does |
| --- | --- | --- |
| Human input | [AgentWisper](https://github.com/Rajveerx11/AgentWisper) | Windows voice dictation with local technical vocabulary correction. Early-stage open source. |
| Context | [GFI Scout](https://github.com/Rajveerx11/gfi-scout) · [RepoGraph Intelligence](https://github.com/Rajveerx11/repograph-intelligence) | Contribution discovery through MCP and a CLI/TUI. Structural codebase context through repository graphs. |
| Orchestration | [Neura](https://github.com/Rajveerx11/neura) | Windows-first engineering-agent harness for Pi with explicit modes and policy guardrails. Includes recovery and verification. |
| Testing | [Tessera](https://github.com/neuratile/Tessera) | Local-first testing IDE built at neuratile. Code context, structured QA artifacts, and optional Docker test execution. |
| Verification | [Proof-of-Work](https://github.com/Rajveerx11/proof-of-work) | Rerun checks, inspect test integrity, and record signed verdicts for coding-agent work. |
| Memory | [Obsidian Graph Intelligence](https://github.com/Rajveerx11/obsidian-graph-intelligence) · [Unified Memory MCP](https://github.com/Rajveerx11/unified-memory-mcp) | Local knowledge-graph analysis and repair. An MCP layer for querying local memory sources. |
| Human approval | [PR Reliability Platform](https://github.com/Rajveerx11/pr-reliability-platform) | Approval-first GitHub App for evidence-backed AI pull request review. |
| Model evaluation | [Master Models](https://github.com/Rajveerx11/Master-Models) | Local specialist-model evaluation against a stock baseline using frozen repository tasks. |

<details>
<summary>Inspect the flagship systems</summary>

### Proof-of-Work

A CLI, Git hook, and GitHub Action that reruns checks, detects deleted or weakened tests, and records signed verdicts. Hash-chained and Ed25519-signed verification logs can be checked locally.

**Stack:** Python · FastMCP · SQLite · Ed25519 · GitHub Actions

[Source](https://github.com/Rajveerx11/proof-of-work) · [PyPI](https://pypi.org/project/proof-of-work-agent/) · [Published evaluation](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent)

### GFI Scout

Find open-source issues using repository health and maintainer responsiveness. Also assess issue freshness and setup friction. Available through four FastMCP tools and a shared CLI/TUI.

**Stack:** Python · FastMCP · asyncio · Rich / Textual · GitHub API

[Source and demo](https://github.com/Rajveerx11/gfi-scout) · [Architecture](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md)

### Tessera

A Rust/Tauri desktop app built at neuratile. Retrieve code context, generate structured QA artifacts, and optionally execute tests in network-isolated Docker containers.

My public contributions include the [mutation-testing engine and scoring flow](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704), the [test-improvement loop](https://github.com/neuratile/Tessera/commit/6cdbc5b3b0e0432f328451f949e5ab12c9d83fac), and [persisted self-heal history](https://github.com/neuratile/Tessera/commit/9ec127a71b818296b5ac201a2bfd7e926e69a206).

**Stack:** Rust · Tauri · React · Tree-sitter · Ollama · Docker

[Source](https://github.com/neuratile/Tessera) · [Website](https://tesseraide.vercel.app/)

### Obsidian Graph Intelligence

Analyze a vault as a knowledge graph, find missing links, and apply repair actions. Semantic embeddings run offline with Transformers.js. The optional query layer requires explicit opt-in. External model providers have their own data boundaries.

**Stack:** TypeScript · Obsidian API · Transformers.js

[Read features and boundaries](https://github.com/Rajveerx11/obsidian-graph-intelligence)

</details>

## How I work, in the Git history

Tessera's mutation-testing change included a review correction for a cancellation gap. The [public commit](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704) records the implementation and its fixes.

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/flight-recorder-mobile-light.svg" />
  <source media="(max-width: 600px)" srcset="assets/flight-recorder-mobile.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/flight-recorder-light.svg" />
  <img width="100%" src="assets/flight-recorder.svg" alt="Tessera flight recorder, commit 48266fa dated 18 June 2026: build the mutation engine, fix a lost Stop request with one shared cancellation token, retain the regression test, and suppress tracker comments for the internal baseline." />
</picture>

**A commit reading, not an agent-session replay.** No timings or simulated tool logs are shown.

<details>
<summary>Inspect the correction and regression checks</summary>

- **Build the engine:** Mutate covered source lines and rerun the suite in the Docker runner. Report mutations that the tests catch and those that survive. [Engine at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/providers/runners/mutation.rs).
- **Catch the cancellation gap:** A Stop request could be lost between the baseline run and the mutant sweep. The correction registers one token across both phases. [Mutation service at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/services/mutation_service.rs).
- **Keep the regression test:** `stop_during_baseline_aborts_before_any_mutant_runs` checks that cancelling the baseline prevents mutant runs. The engine also tests the corrected arithmetic cycle with `arithmetic_operators_form_a_distinct_cycle`.
- **Guard the side effect:** The internal baseline passes `post_jira_comment = false`, including error and cancellation paths. User-requested runs keep their existing behavior. [Sandbox service at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/services/sandbox_service.rs).

</details>

### A comparison you can inspect

The [published Proof-of-Work report](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md) records **60 runs on 20 tasks across three agent configurations**. One attempt per task and configuration. All outcomes are retained.

| Published configuration | Passed | Failed |
| --- | ---: | ---: |
| Codex CLI 0.146.0 / `gpt-5.6-sol` | 20 | 0 |
| GitHub Copilot CLI 1.0.79 / auto router | 20 | 0 |
| OpenCode CLI 1.4.0 / Nemotron 3 Nano | 17 | 3 |

A pass required a successful agent exit, a protected outcome verifier, and the deterministic anti-tampering gate. The three failures were outcome-verifier failures, not anti-tampering findings.

These are recorded results from the August 2026 cohort, **not a general ranking of agents**. Codex rows were recorded eight days earlier and imported unchanged. Token usage and exact cost are unknown. [Methodology and limitations](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md#limitations).

### Working principles

- **Evidence before claims.** Tests and inspectable outputs beat a claim that the task is complete.
- **Local-first when privacy matters.** Keep sensitive context on-device by default and make external boundaries explicit.
- **Agents as systems.** Build state and recovery around the model. Keep human approval points explicit.

<details>
<summary>Technical working set</summary>

| Area | Tools |
| --- | --- |
| Agent systems | MCP / FastMCP, tool orchestration, Zod and JSON Schema, eval gates, RAG |
| Languages | Python, TypeScript / JavaScript, Rust, Kotlin |
| Local AI and code intelligence | Ollama, Transformers.js, Tree-sitter, PyTorch, graph analytics |
| Systems and desktop | Tauri, SQLite, Docker, Node.js, React, Next.js, Flask |
| Delivery and verification | GitHub Actions, mutation testing, Ed25519 signing, PyPI packaging |

</details>

## The rest of the work

[Open the full linked repository index](docs/public-repositories.md). It includes public repositories from Rajveerx11 and associated organizations, with forks marked. Inclusion does not imply sole authorship.

<a href="docs/public-repositories.md"><img width="100%" src="assets/project-index.svg" alt="Public repository catalog. Forks are marked; open the full Markdown index for repository namespaces, descriptions, and individual source links." /></a>

The catalog and activity data refresh daily. Each generated artifact shows its snapshot date. These are not live counters.

<details>
<summary>GitHub activity snapshot</summary>

<img width="100%" src="assets/github-stats.svg" alt="Recorded GitHub API activity totals and byte shares within the displayed top languages. The image includes its snapshot date and refreshes daily." />

</details>

<details>
<summary>Open the interactive HTML design</summary>

The [single-file HTML version](docs/execution-atlas.html) includes territory selection, project details, repository search, and theme switching. Download it and open it in a browser. GitHub displays the HTML as source rather than running it. Its repository data is explicitly dated and does not refresh with the daily catalog.

The profile above uses static SVG images, native links, and expandable Markdown sections. It does not depend on JavaScript or a third-party image service.

</details>

## Contact & collaboration

Building tools for developers or agentic systems?

[Email me](mailto:rajveer.r.vadnal@gmail.com) · [Connect on LinkedIn](https://www.linkedin.com/in/rajveer-vadnal-374664353) · [Explore my portfolio](https://rajveervadnal.netlify.app/)
