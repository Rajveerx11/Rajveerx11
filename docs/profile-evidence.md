# Profile evidence and accessible text

This is the text companion to [Rajveer Vadnal's terminal profile](../README.md). The README highlights selected projects; this document keeps the broader project descriptions, individual links, contribution attribution, and limitations readable and searchable.

## About

I build coding tools and local-first AI products. My work focuses on context, controlled execution, and verification. My main languages are Python and TypeScript. I also use Rust.

Founder at [neuratile](https://neuratile.rajveer.codes/), building developer tools including Tessera. [GitHub organization](https://github.com/neuratile). Founder of [Visage AI](https://getvisageai.online/), an aesthetic outcome preview product.

Education: Diploma in Computer Science Engineering; B.Tech in Artificial Intelligence & Machine Learning.

[Portfolio](https://rajveer.codes/) · [Resume](https://rajveer.codes/Rajveer_Vadnal_Resume.pdf) · [LinkedIn](https://www.linkedin.com/in/rajveer-vadnal-374664353) · [Email](mailto:rajveer.r.vadnal@gmail.com)

## Execution atlas

**Roles, not wiring.** The paths group projects by purpose. They do not claim integrations between repositories. The image is a static map. Human approval is an explicit boundary.

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

## Selected systems

### Proof-of-Work

A CLI, Git hook, and GitHub Action that reruns checks, detects deleted or weakened tests, and records signed verdicts. Hash-chained and Ed25519-signed verification logs can be checked locally.

Stack: Python · FastMCP · SQLite · Ed25519 · GitHub Actions

[Source](https://github.com/Rajveerx11/proof-of-work) · [PyPI](https://pypi.org/project/proof-of-work-agent/) · [Published evaluation](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent)

### GFI Scout

Find open-source issues using repository health and maintainer responsiveness. Also assess issue freshness and setup friction. Available through four FastMCP tools and a shared CLI/TUI.

Stack: Python · FastMCP · asyncio · Rich / Textual · GitHub API

[Source and demo](https://github.com/Rajveerx11/gfi-scout) · [Architecture](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md)

### Tessera

A Rust/Tauri desktop app built at neuratile. Retrieve code context, generate structured QA artifacts, and optionally execute tests in network-isolated Docker containers.

My public contributions include the [mutation-testing engine and scoring flow](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704), the [test-improvement loop](https://github.com/neuratile/Tessera/commit/6cdbc5b3b0e0432f328451f949e5ab12c9d83fac), and [persisted self-heal history](https://github.com/neuratile/Tessera/commit/9ec127a71b818296b5ac201a2bfd7e926e69a206).

Stack: Rust · Tauri · React · Tree-sitter · Ollama · Docker

[Source](https://github.com/neuratile/Tessera) · [Website](https://tesseraide.vercel.app/)

### Obsidian Graph Intelligence

Analyze a vault as a knowledge graph, find missing links, and apply repair actions. Semantic embeddings run offline with Transformers.js. The optional query layer requires explicit opt-in. External model providers have their own data boundaries.

Stack: TypeScript · Obsidian API · Transformers.js

[Read features and boundaries](https://github.com/Rajveerx11/obsidian-graph-intelligence)

## Flight recorder: a public commit, not a session replay

Tessera's mutation-testing change included a review correction for a cancellation gap. The [public commit 48266fa, dated 18 June 2026](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704) records the implementation and its fixes. No timings or simulated tool logs are shown.

- **Build the engine:** Mutate covered source lines and rerun the suite in the Docker runner. Report mutations that the tests catch and those that survive. [Engine at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/providers/runners/mutation.rs).
- **Catch the cancellation gap:** A Stop request could be lost between the baseline run and the mutant sweep. The correction registers one token across both phases. [Mutation service at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/services/mutation_service.rs).
- **Keep the regression test:** `stop_during_baseline_aborts_before_any_mutant_runs` checks that cancelling the baseline prevents mutant runs. The engine also tests the corrected arithmetic cycle with `arithmetic_operators_form_a_distinct_cycle`.
- **Guard the side effect:** The internal baseline passes `post_jira_comment = false`, including error and cancellation paths. User-requested runs keep their existing behavior. [Sandbox service at the cited commit](https://github.com/neuratile/Tessera/blob/48266fa55f46fff88a966aecf88c0b437e1c5704/apps/desktop/src-tauri/src/services/sandbox_service.rs).

## Published evaluation and limitations

The [published Proof-of-Work report](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md) records **60 runs on 20 tasks across three agent configurations**. One attempt per task and configuration. All outcomes are retained.

| Published configuration | Passed | Failed |
| --- | ---: | ---: |
| Codex CLI 0.146.0 / `gpt-5.6-sol` | 20 | 0 |
| GitHub Copilot CLI 1.0.79 / auto router | 20 | 0 |
| OpenCode CLI 1.4.0 / Nemotron 3 Nano | 17 | 3 |

A pass required a successful agent exit, a protected outcome verifier, and the deterministic anti-tampering gate. The three failures were outcome-verifier failures, not anti-tampering findings.

These are recorded results from the August 2026 cohort, **not a general ranking of agents**. Codex rows were recorded eight days earlier and imported unchanged. Token usage and exact cost are unknown. [Methodology and limitations](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md#limitations).

## Working principles

- **Evidence before claims.** Tests and inspectable outputs beat a claim that the task is complete.
- **Local-first when privacy matters.** Keep sensitive context on-device by default and make external boundaries explicit.
- **Agents as systems.** Build state and recovery around the model. Keep human approval points explicit.

## Technical working set

| Area | Tools |
| --- | --- |
| Agent systems | MCP / FastMCP, tool orchestration, Zod and JSON Schema, eval gates, RAG |
| Languages | Python, TypeScript / JavaScript, Rust, Kotlin |
| Local AI and code intelligence | Ollama, Transformers.js, Tree-sitter, PyTorch, graph analytics |
| Systems and desktop | Tauri, SQLite, Docker, Node.js, React, Next.js, Flask |
| Delivery and verification | GitHub Actions, mutation testing, Ed25519 signing, PyPI packaging |

## Public catalog and activity

[Open the full linked repository index](public-repositories.md). It includes public repositories from Rajveerx11 and associated organizations, with forks marked. Inclusion does not imply sole authorship.

The catalog and activity data refresh daily. Each generated artifact shows its UTC snapshot date. These are not live counters. Calendar and activity cards share one GitHub GraphQL snapshot. [The accessible activity snapshot](activity.md) records the same metrics, dates, and every daily calendar count as text.

- The calendar covers the displayed date range (365 days before refresh through the refresh date). Counts follow GitHub's contribution rules, not commits alone. Calendar aggregates can include anonymized private contribution counts when exposed by GitHub; no private repository names or metadata are requested or published.
- Heatmap colors are relative to the busiest day within that window. Calendar cells are aligned to Sunday-first weeks. The narrow version splits the same dates into two panels; it does not discard older activity.
- Current streak means consecutive nonzero calendar days through today, or yesterday while today's UTC date is unfinished. Only today's zero gets that grace period. The longest streak is scoped to the displayed window, not an all-time claim.
- Merged PRs are public, all time. Repository and star totals include all paginated owned public non-forks, not organization repositories or forks. Followers are recorded at refresh.
- API failures fail the refresh without replacing the existing artwork. Its previous snapshot date remains visible. Activity is not a productivity score.
- The short heatmap reveal honors reduced motion. Calendar cells remain visible without animation. Light/dark and narrow/wide variants are committed locally; the README does not rely on third-party image endpoints.

The shell prompts are section labels, not an interactive terminal or a transcript of commands that were executed. The ASCII initials are original artwork, not a photograph or simulated portrait.

## Interactive design

The [single-file HTML version](execution-atlas.html) includes territory selection, project details, repository search, and theme switching. Download it and open it in a browser. GitHub displays the HTML as source rather than running it. Its repository data is explicitly dated and does not refresh with the daily catalog.

The profile uses SVG images (a short CSS reveal on the contribution calendar) and native links. It does not depend on JavaScript or a third-party image service. SVG-internal links do not work in GitHub-embedded images, so navigation remains native Markdown.

## Contact

Building tools for developers or agentic systems?

[Email me](mailto:rajveer.r.vadnal@gmail.com) · [Connect on LinkedIn](https://www.linkedin.com/in/rajveer-vadnal-374664353) · [Explore my portfolio](https://rajveer.codes/)
