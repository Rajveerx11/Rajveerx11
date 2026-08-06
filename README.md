# Rajveer Vadnal

**Agentic engineer building verification infrastructure, local-first AI systems,
and developer tools.**

[Portfolio][portfolio] / [CV][resume] / [LinkedIn][linkedin] / [Email][email]

Based in Solapur, India. Studying Artificial Intelligence and Machine Learning
at SIT Hyderabad. Founder and lead engineer at [neuratile][neuratile], and
founder of [Visage AI][visage].

I build systems where model output is only one part of the product. The
surrounding work matters more: tool contracts, durable context, deterministic
checks, privacy boundaries, failure handling, and evidence a reviewer can
inspect.

Current focus: coding-agent verification, specialist-model evaluation, MCP
infrastructure, and local code intelligence.

## Selected work

### [Proof-of-Work][proof-of-work]

Verification and evaluation infrastructure for AI coding agents. It re-runs
real tests, detects deleted or weakened checks and fake passes, then records
each verdict in a hash-chained, Ed25519-signed audit log.

Shipped as a [PyPI package][proof-of-work-pypi] with a CLI, pre-commit hook,
composite GitHub Action, optional mutation testing, and a versioned 20-task
agent-evaluation corpus. [Read the evaluation methodology][proof-of-work-eval].

`Python` `SQLite` `GitHub Actions` `Ed25519` `Mutation testing`

### [Tessera][tessera]

A local-first AI testing IDE built at neuratile. Tessera parses a codebase with
Tree-sitter, retrieves relevant context from local SQLite storage, and generates
schema-validated test plans, test cases, defect reports, and bug reports.

Source stays on the machine with the default Ollama setup. Generated tests can
run in an optional, network-isolated Docker sandbox.
[View the product][tessera-product].

`Rust` `Tauri` `React` `TypeScript` `Tree-sitter` `Ollama` `SQLite`

### [Master Models][master-models]

An open specialist-model experiment testing whether a Qwen3-8B frontend
specialist can beat its stock base and remain competitive with a stock
Qwen3-Coder-30B-A3B model on real repository work.

Training uses QLoRA and a frozen 20-task, three-arm gate. Current state: the
training run is reported complete, while verified GGUF export and the final gate
remain pending. The repository publishes dataset manifests, notebook hashes,
templates, status, and a runbook for reproducing or auditing the work.

`Qwen3` `QLoRA` `llama.cpp` `Jupyter` `Evaluation`

## More systems

### Developer infrastructure

- **[Obsidian Graph Intelligence][obsidian].** Analyzes Obsidian vaults as typed
  knowledge graphs, finds weak links and orphan notes, suggests repairs, and
  exposes local agent queries. `TypeScript` `Transformers.js` `MCP`
- **[GFI Scout][gfi-scout].** MCP server, CLI, and TUI that rank good-first
  issues by contributor success signals instead of label alone.
  `Python` `FastMCP` `GitHub API` `asyncio`
- **[RepoGraph Intelligence][repograph].** Builds repository dependency graphs
  for search, architecture analysis, blast radius, policy gates, drift checks,
  and agent context. `JavaScript` `Rust` `Tree-sitter` `MCP`
- **[Unified Memory MCP][unified-memory].** Unifies Claude memory exports,
  coding-session logs, and Obsidian notes into a local, queryable second brain.
  `TypeScript` `JSON` `Ollama` `MCP`

### Product and platform work

- **[Agent Skills Portfolio][skills].** Shared, outcome-driven skills for Codex
  and Claude Code with reusable scripts and verification gates.
  `Markdown` `JavaScript` `Python`
- **[Visage AI][visage].** Live mobile product for AI-assisted
  cosmetic-procedure visualization, with explicit privacy limits and medical
  disclaimers. Source is private. `TypeScript` `Computer vision` `Mobile AI`

[Browse all public repositories][repositories]

## Engineering focus

- **Agent infrastructure:** MCP servers, tool orchestration, structured outputs,
  evaluation harnesses, state, and approval boundaries.
- **Code intelligence:** Tree-sitter, dependency graphs, retrieval, embeddings,
  semantic search, and change-impact analysis.
- **Local AI:** Ollama, llama.cpp, on-device embeddings, model fine-tuning,
  reproducible gates, and explicit cloud boundaries.
- **Product engineering:** Python, TypeScript, Rust, React, Tauri, SQLite,
  Docker, automated tests, packaging, and CI.

## How I work

- **Evidence before claims.** Tests, typed contracts, reproducible checks, and
  inspectable outputs beat confidence.
- **Local-first when privacy matters.** Source, embeddings, and user data stay
  on-device by default. Cloud boundaries remain explicit.
- **Agents as systems, not prompts.** Useful agents need tools, state, failure
  handling, verification, and clear human approval points.

[email]: mailto:rajveer.r.vadnal@gmail.com
[gfi-scout]: https://github.com/Rajveerx11/gfi-scout
[linkedin]: https://www.linkedin.com/in/rajveer-vadnal-374664353
[master-models]: https://github.com/Rajveerx11/Master-Models
[neuratile]: https://github.com/neuratile
[obsidian]: https://github.com/Rajveerx11/obsidian-graph-intelligence
[portfolio]: https://rajveervadnal.netlify.app/
[proof-of-work]: https://github.com/Rajveerx11/proof-of-work
[proof-of-work-eval]: https://github.com/Rajveerx11/proof-of-work/tree/main/reports/v0.2.0
[proof-of-work-pypi]: https://pypi.org/project/proof-of-work-agent/
[repograph]: https://github.com/Rajveerx11/repograph-intelligence
[repositories]: https://github.com/Rajveerx11?tab=repositories
[resume]: https://rajveervadnal.netlify.app/Rajveer_Vadnal_Resume.pdf
[skills]: https://github.com/Rajveerx11/skills
[tessera]: https://github.com/neuratile/Tessera
[tessera-product]: https://tesseraide.vercel.app/
[unified-memory]: https://github.com/Rajveerx11/unified-memory-mcp
[visage]: https://getvisageai.online/
