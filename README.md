<img width="100%" src="assets/profile-header.svg" alt="Rajveer Vadnal — AI Engineer" />

I build **reliable coding agents, evaluation tools and local-first developer software**.
Diploma completed; entering AI & ML at SIT Hyderabad through direct second-year admission. Based in Solapur / Hyderabad, India · Founder at [neuratile](https://github.com/neuratile).

**Open to AI / Agentic Engineering opportunities.**
[Resume](https://rajveervadnal.netlify.app/Rajveer_Vadnal_Resume.pdf) · [Portfolio](https://rajveervadnal.netlify.app/) · [LinkedIn](https://www.linkedin.com/in/rajveer-vadnal-374664353) · [Email](mailto:rajveer.r.vadnal@gmail.com)

## Selected work

### [Proof-of-Work](https://github.com/Rajveerx11/proof-of-work) · Coding-agent verification

A CLI, Git hook and GitHub Action that reruns checks, detects supported test-tampering patterns and records signed verdicts. [Published on PyPI](https://pypi.org/project/proof-of-work-agent/).

- **Evidence:** Published **60 runs across 3 agent configurations on 20 tasks**: Codex 20/20, Copilot 20/20, OpenCode 17/20. One attempt per task and configuration; an environment-specific comparison, not a general ranking. [Report, methodology and raw results](https://github.com/Rajveerx11/proof-of-work/tree/main/reports/2026-08-11-multi-agent).
- **Engineering decision:** Keep the LLM judge advisory; derive pass/fail from deterministic checks and a protected outcome verifier. The local runner is for trusted fixtures, not a security sandbox.

`Python` `SQLite` `Ed25519` `GitHub Actions`

### [Tessera](https://github.com/neuratile/Tessera) · Local-first AI testing IDE

A Rust/Tauri desktop app built at neuratile: retrieve code context, generate structured QA artifacts, then optionally run generated tests in a network-isolated Docker container. Source stays local when using local providers; cloud providers are optional.

- **My work:** Implemented the [mutation-testing engine and scoring flow](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704), the [test-improvement loop](https://github.com/neuratile/Tessera/commit/6cdbc5b3b0e0432f328451f949e5ab12c9d83fac), and [persisted self-heal history](https://github.com/neuratile/Tessera/commit/9ec127a71b818296b5ac201a2bfd7e926e69a206).
- **Engineering decision:** Measure whether tests catch seeded bugs, beyond line coverage. Keep the best test version after bounded improvement attempts.

[Product website](https://tesseraide.vercel.app/) · [Architecture and setup](https://github.com/neuratile/Tessera#architecture) · [CI](https://github.com/neuratile/Tessera/actions)

`Rust` `Tauri` `React` `Tree-sitter` `Ollama` `Docker`

### [GFI Scout](https://github.com/Rajveerx11/gfi-scout) · MCP server + CLI/TUI

Find open-source issues using repository health, maintainer responsiveness, freshness and setup friction. The configurable ranking is a heuristic score, not a calibrated probability of success.

- **Evidence:** Four MCP tools, shared CLI/TUI handlers, and [unit/integration tests](https://github.com/Rajveerx11/gfi-scout/tree/main/tests). [Watch the demo](https://github.com/Rajveerx11/gfi-scout#readme) · [CI](https://github.com/Rajveerx11/gfi-scout/actions).
- **Engineering decision:** Bound concurrent API calls, cache by namespace and credential, and degrade gracefully when optional repository checks fail. [Architecture](https://github.com/Rajveerx11/gfi-scout/blob/main/docs/ARCHITECTURE.md).

`Python` `FastMCP` `asyncio` `GitHub API`

## How I work

- **Make outcomes checkable.** Define the verifier and preserve the failures, configuration and limits alongside results. See the [evaluation methodology](https://github.com/Rajveerx11/proof-of-work/blob/main/reports/2026-08-11-multi-agent/README.md).
- **Review the edge cases.** Tessera's mutation-testing change includes review fixes for cancellation, operator coverage and unintended tracker comments, with regression checks in the [merged change](https://github.com/neuratile/Tessera/commit/48266fa55f46fff88a966aecf88c0b437e1c5704).
- **Separate experiments from shipped work.** Freeze evaluation tasks before creating training data; promote a specialist only after it beats its base model on that gate. [Master Models research status](https://github.com/Rajveerx11/Master-Models).

## More work & research

- **[Obsidian Graph Intelligence](https://github.com/Rajveerx11/obsidian-graph-intelligence):** Knowledge-graph analysis, local embeddings and vault repair, with an opt-in MCP-style query layer.
- **[Master Models](https://github.com/Rajveerx11/Master-Models) — research in progress:** V2 targets Qwen3-4B with QLoRA. Five frozen specialist evals, 20 tasks each; V2 training and gates are pending. The earlier Qwen3-8B experiment is preserved as V1 evidence.

<details>
<summary>Tools I use</summary>

- **Languages & applications:** Python, Rust, TypeScript, React, Tauri.
- **Agents & retrieval:** MCP, FastMCP, JSON Schema, Zod, Tree-sitter, SQLite, Ollama, Transformers.js.
- **Verification & delivery:** pytest, mutation testing, Docker, GitHub Actions, PyPI, Ed25519.
- **Research:** QLoRA, Qwen3, llama.cpp; current training status is documented in Master Models.

</details>

<details>
<summary>Repository archive & GitHub activity</summary>

[Browse public repositories](https://github.com/Rajveerx11?tab=repositories). The index also lists selected private project names; their source is not available here. Activity counts describe repository activity, not project quality.

<img width="100%" src="assets/project-index.svg" alt="Index of public repositories and selected private project names" />
<img width="100%" src="assets/github-stats.svg" alt="GitHub activity counts and language distribution" />

</details>
