
Version
License
Build Status
Issues
Discord Community
# ECLYPSA AI
> **A modular, privacy-first, developer-friendly artificial intelligence engine and open platform.**
> 
ECLYPSA AI is an open-source artificial intelligence foundation designed to serve as an extensible engine for local-first inference, autonomous agent orchestration, cross-platform client integration, and enterprise-grade privacy controls. Built from the ground up to respect user data ownership, ECLYPSA AI decouples inference mechanics from client applications to provide a consistent, robust runtime environment across edge, desktop, mobile, and server environments.
## Vision
To democratize artificial intelligence by delivering an open, modular ecosystem where users maintain absolute ownership over their data, models, and workflows without sacrificing enterprise performance or developer ergonomics.
## Mission
To construct a universal, modular runtime and SDK layer that enables developers to build, deploy, and scale privacy-preserving AI applications across any hardware infrastructure—from resource-constrained personal devices to distributed cloud environments.
## Core Principles
 * **🔒 Privacy by Design:** Data never leaves the local environment unless explicitly configured by the operator.
 * **🧩 Modular Architecture:** Every core subsystem—from model loaders to transport layers—is pluggable and extensible.
 * **⚡ Developer Ergonomics:** Clean APIs, comprehensive SDKs, and predictable CLI interfaces engineered for developer productivity.
 * **🌐 Hardware Agnostic:** Seamless operational support spanning CPU, GPU, and specialized edge accelerators.
 * **📖 Open Governance:** Driven by transparent community collaboration and strict open-source licensing.
## Current Project Status
> [!IMPORTANT]
> **Stage:** Foundation (v0.0.1-alpha)
> ECLYPSA AI is currently in its early structural foundation phase. The repository contains the core architectural skeleton, early engine abstractions, and setup scripts. Subsystems marked as **Under Development** or **Planned** are actively undergoing engineering work and should not be used in production environments.
> 
## Development Philosophy
ECLYPSA AI follows strict engineering practices rooted in systems reliability, explicit boundaries, and zero hidden magic:
 1. **Explicit Architecture over Implicit Magic:** Interfaces are clearly typed and bounded to ensure predictable execution.
 2. **Minimal External Dependencies:** Core functionality prioritizes lean, audited standard libraries and minimal third-party supply chain exposure.
 3. **Strict Versioning and Contract Stability:** Public APIs adhere strictly to Semantic Versioning (SemVer).
 4. **Test-Driven Rigor:** Foundation code requires comprehensive unit and integration test coverage prior to release candidate staging.
## Table of Contents
 * Vision
 * Mission
 * Core Principles
 * Current Project Status
 * Development Philosophy
 * Project Goals
 * Why ECLYPSA AI?
 * Features
 * Architecture Overview
 * ASCII Architecture Diagram
 * Repository Structure
 * Technology Stack
 * System Requirements
 * Installation
 * Quick Start
 * Configuration
 * Environment Variables
 * Usage
 * CLI
 * API
 * Plugin System
 * SDK
 * Documentation Index
 * Development Workflow
 * Branch Strategy
 * Commit Convention
 * Versioning
 * Roadmap
 * Testing
 * Security
 * Contributing
 * Code of Conduct
 * FAQ
 * Known Limitations
 * Future Plans
 * Acknowledgements
 * License
 * Support
 * Contact
## Project Goals
 1. **Unified Inference Runtime:** Standardize model execution across local GGUF/ONNX weights and remote provider APIs.
 2. **Modular Agent Orchestration:** Provide a light, deterministic execution frame for multi-step agent reasoning and tool usage.
 3. **Pluggable Middleware Architecture:** Allow developers to easily inject custom guardrails, memory providers, and loggers.
 4. **Cross-Platform Native Clients:** Deliver seamless integration across CLI, Web, Desktop (Electron/Tauri), and Mobile (Flutter/React Native).
## Why ECLYPSA AI?

| Feature / Goal | Vendor Cloud APIs | Monolithic Local Tools | ECLYPSA AI Framework |
| :--- | :--- | :--- | :--- |
| **Data Privacy** | ❌ Third-party hosted | ✅ Fully Local | ✅ Local-First / Encrypted |
| **Architecture** | ❌ Proprietary SaaS | ❌ Monolithic | ✅ Fully Modular & Engine-Based |
| **Extensibility** | ❌ Limited Hooking | ❌ Hardcoded Tools | ✅ Plugin & Driver Ecosystem |
| **Cross-Platform** | ✅ REST/gRPC | ❌ Desktop/CLI Only | ✅ CLI, Desktop, Mobile, SDK |
| **Agent Controls** | ❌ Opaque | ❌ Basic Loops | ✅ Deterministic Execution Pipeline | <br> ## Features <br> Below is the status matrix for features within the v0.0.1-alpha foundation release:
| Subsystem | Feature Description | Status |
| :--- | :--- | :--- |
| **Core** | Modular Engine Initialization & Config Parser | ✅ Available |
| **Core** | Driver Interface Abstractions (Inference, Storage, Transport) | ✅ Available |
| **CLI** | Base Command Line Interface Setup (eclypsa) | ✅ Available |
| **API** | REST API Routing & OpenAPI Schema Generator | 🚧 Under Development |
| **API** | Real-time WebSocket / SSE Streaming Endpoints | 🚧 Under Development |
| **Agent** | Single-step Task Execution Loop | 🚧 Under Development |
| **Agent** | Multi-agent Collaborative Workflows | 🗺 Planned |
| **Plugins** | Plugin Lifecycle Loader & Hook Registration | 🚧 Under Development |
| **SDK** | Python Software Development Kit (eclypsa-sdk) | 🚧 Under Development |
| **SDK** | TypeScript / Node.js SDK | 🗺 Planned |
| **Desktop** | Cross-platform Tauri Client Shell | 🗺 Planned |
| **Mobile** | Native Mobile Client Framework | 🗺 Planned |
| **Security** | End-to-End Local Vector Store Encryption | 🗺 Planned | <br> ## Architecture Overview <br> ECLYPSA AI is organized around a core execution engine (core) that decouples client user interfaces (cli, desktop, mobile) from model providers and agent logic (agent). <br> * **Core Engine:** Manages lifecycle, configuration, pipeline registration, and thread execution. <br> * **Transport & API Layer:** Exposes standard gRPC, REST, and WebSocket abstractions to external or local clients. <br> * **Agent Core:** Handles memory, tool evaluation, context assembly, and step-based processing. <br> * **Plugin Abstraction:** Provides strictly defined interfaces for custom vector stores, external tools, and model adapters. <br> ## ASCII Architecture Diagram <br> ```text <br> +-----------------------------------------------------------------------+
| CLIENT LAYERS |
| +-----------------+   +------------------+   +------------------+ |
|  | CLI Client |  | Desktop Client |  | Mobile Client |  |
|  | (`cli/`) |  | (`desktop/`) |  | (`mobile/`) |  |
| +--------+--------+   +--------+---------+   +--------+---------+ | <br> +------------|---------------------|----------------------|-------------+
| :--- | :--- | <br> +------------------+  |  +-------------------+
| :--- | :--- | <br> +-------------------------------v--v--v---------------------------------+
| API & SDK LAYER |
| +--------------------/ API Gateway (`api/`) \-------------------+ |
|  | REST Endpoints | WebSocket / SSE Streams | gRPC Interfaces |  |
| +---------------------------------------------------------------+ |
| +--------------------/ SDK Layer (`sdk/`) \---------------------+ |
|  | Python SDK | TypeScript SDK | Go Core Bindings |  |
| +---------------------------------------------------------------+ | <br> +-----------------------------------|-----------------------------------+
| <br> +-----------------------------------v-----------------------------------+
| CORE AI ENGINE |
| +-----------------------------------------------------------------+ |
|  | ECLYPSA CORE (`core/`) |  |
|  | +--------------------+  +-------------------+  +------------+ |  |
|  |  | Pipeline Registry |  | Context Assembler |  | Event Bus |  |  |
|  | +--------------------+  +-------------------+  +------------+ |  |
| +-----------------------------------------------------------------+ |
| :--- | :--- |
| +--------------------------------v--------------------------------+ |
|  | AGENT FRAMEWORK (`agent/`) |  |
|  | +--------------------+  +-------------------+  +------------+ |  |
|  |  | Memory Controller |  | Tool Evaluator |  | Task Loop |  |  |
|  | +--------------------+  +-------------------+  +------------+ |  |
| +-----------------------------------------------------------------+ | <br> +-----------------------------------|-----------------------------------+
| <br> +-----------------------------------v-----------------------------------+
| PLUGINS & EXTENSIONS |
| +---------------------------------------------------------------+ |
|  | Plugin System (`plugins/`) |  |
|  | +-------------------+  +------------------+  +------------+ |  |
|  |  | Local Model Driver |  | Cloud Model API |  | Vector Store |  |  |
|  | +-------------------+  +------------------+  +------------+ |  |
| +---------------------------------------------------------------+ |

+-----------------------------------------------------------------------+
```
## Repository Structure
The project directory structure is organized as follows:
```text
.
├── .github/          # GitHub Workflows, issue templates, and CI/CD pipelines
├── agent/            # Autonomous agent logic, memory systems, and tool execution engines
├── api/              # REST, WebSocket, and gRPC interface servers
├── assets/           # Media assets, brand identity, architectural diagrams, and banners
├── cli/              # Command-line interface binaries and command handlers
├── core/             # Base engine, pipeline abstractions, context management, and lifecycle logic
├── desktop/          # Cross-platform desktop application workspace
├── docs/             # Complete project documentation, specifications, and architecture guides
├── examples/         # Reference implementations, script samples, and integration patterns
├── mobile/           # Mobile client source code and platform bindings
├── plugins/          # Official plugin distribution tree and plugin loader interface
├── scripts/          # Automation scripts for build, setup, linting, and development environment setup
├── sdk/              # Official multi-language SDK source code (Python, TS, Go)
├── tests/            # End-to-end testing suite, unit tests, integration tests, and benchmarks
└── tools/            # Developer tools, code generators, and repository maintenance utilities
```
## Technology Stack
### Current (Foundation)
 * **Core Engine:** Go (v1.22+) / Python (v3.11+)
 * **CLI Engine:** Cobra / Typer
 * **Configuration:** YAML / TOML with Strict Schema Validation
 * **Build System:** Make / Taskfile / Cargo
### Planned
 * **API Transport:** gRPC, FastAPI, Tokio/Axum
 * **Desktop Client:** Tauri / Rust / React
 * **Mobile Client:** Flutter / Dart
 * **Database & Vector Storage:** DuckDB, SQLite, Qdrant / Milvus Local Drivers
## System Requirements
### Hardware Requirements

| Resource | Minimum | Recommended |
| :--- | :--- | :--- |
| **CPU** | Dual-core 64-bit x86_64 / ARM64 | 8-core modern processor with AVX2/NEON |
| **RAM** | 4 GB | 16 GB+ (for local model execution) |
| **Storage** | 500 MB (Engine only) | 50 GB+ NVMe SSD (for local model weights) |
| **GPU** | Optional | NVIDIA CUDA compatible (V100/RTX 3060+) or Apple Silicon |

### Software Prerequisites
 * **Operating System:** Linux (Ubuntu 22.04+), macOS (12.0+), Windows 11 (WSL2 recommended)
 * **Go:** 1.22.0 or higher
 * **Python:** 3.11 or higher
 * **Git:** 2.34.0 or higher
## Installation
### Method 1: Building from Source
```bash
# Clone the repository
git clone https://github.com/mkfih3r/eclypsa/eclypsa.git
cd eclypsa
# Run the foundation setup script
./scripts/setup.sh
# Build the core binary
make build
```
### Method 2: Development Installation (Python Environment)
```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate
# Install development dependencies and core modules
pip install -e .[dev]
```
## Quick Start
Initialize the ECLYPSA engine and run a basic health verification check:
```bash
# Verify CLI installation
eclypsa --version
# Initialize local workspace configuration
eclypsa init
# Start the core service daemon (Dry run mode)
eclypsa start --dry-run
```
Output:
```text
[INFO] ECLYPSA AI Engine v0.0.1-alpha (Foundation)
[INFO] Initializing Core Engine...
[INFO] Loaded configuration from: ~/.eclypsa/config.yaml
[INFO] Health check passed: All core interfaces initialized.
[INFO] Dry run complete. Service shutdown cleanly.
```
## Configuration
ECLYPSA AI is configured via a central file located at ~/.eclypsa/config.yaml or through environment variables.
### Example Configuration (config.yaml)
```yaml
version: "v0.0.1-alpha"
engine:
  environment: "development"
  log_level: "info"
  host: "127.0.0.1"
  port: 8080
telemetry:
  enabled: false
plugins:
  directory: "./plugins"
  auto_load: false
agent:
  max_iterations: 10
  timeout_seconds: 120
```
## Environment Variables
All settings defined in config.yaml can be overridden using environment variables prefixed with ECLYPSA_:

| Environment Variable | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| ECLYPSA_ENV | String | development | Defines execution mode (development, staging, production) |
| ECLYPSA_LOG_LEVEL | String | info | Logverbosity (debug, info, warn, error) |
| ECLYPSA_HOST | String | 127.0.0.1 | Network binding interface |
| ECLYPSA_PORT | Integer | 8080 | Port for REST / gRPC API layer |
| ECLYPSA_CONFIG_PATH | Path | ~/.eclypsa/config.yaml | Explicit path to configuration file |

## Usage
### Running the Local Daemon
```bash
# Start daemon in verbose debug mode
eclypsa daemon --verbose
```
### Invoking Foundation Tasks
```bash
# Execute a core utility test task
eclypsa run --task "verify-environment"
```
## CLI
The cli/ subsystem provides the primary terminal interface for developers and system administrators.
```text
Usage: eclypsa [COMMAND] [OPTIONS]
Commands:
  init        Initialize default local configuration directory and environment
  start       Start the ECLYPSA core runtime engine
  daemon      Run the ECLYPSA service in background daemon mode
  plugin      Manage system plugins, drivers, and external tools
  status      Report current status of engine, plugins, and active workers
  version     Display engine build and version details
Options:
  -c, --config TEXT   Path to custom configuration file
  -v, --verbose       Enable verbose debug output logging
  -h, --help          Show help message and exit
```
## API
> [!NOTE]
> The API specification is currently undergoing active implementation. The interface below represents the target contract for v0.1.0.
> 
### REST Endpoint Specification (Draft)
#### GET /v1/health
Checks the operational health status of the runtime engine.
 * **Request:** GET /v1/health
 * **Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "v0.0.1-alpha",
  "uptime_seconds": 1420,
  "subsystems": {
    "core": "active",
    "agent": "idle",
    "plugins": "loaded"
  }
}
```
#### POST /v1/agent/execute
Submits a task execution payload to the local agent engine.
 * **Request Payload:**
```json
{
  "task": "Analyze logs in ./var/logs",
  "max_steps": 5,
  "options": {
    "dry_run": true
  }
}
```
## Plugin System
ECLYPSA AI utilizes a dynamic plugin system located in plugins/ to maintain a lean core framework while enabling vast driver options.
### Plugin Types
 1. **Inference Drivers:** Standardized connectors for local runtimes (e.g., llama.cpp, ONNX Runtime) and cloud APIs.
 2. **Tool Drivers:** Dynamic capabilities consumable by autonomous agents (e.g., file system access, terminal execution, search).
 3. **Storage Drivers:** Connectors for vector stores, key-value stores, and relational data repositories.
### Plugin Contract Structure
All plugins must export an initialization interface matching the system specification:
```python
# Specification example for Python-based plugin interface
class PluginInterface:
    def initialize(self, context: dict) -> bool:
        """Initialize the plugin with core context."""
        pass
    def execute(self, action: str, payload: dict) -> dict:
        """Perform action defined by plugin spec."""
        pass
```
## SDK
Language-specific software development kits reside in the sdk/ directory.
### Python SDK (Preview Snippet)
```python
# Example Usage of the ECLYPSA Python SDK (In Development)
from eclypsa import Client
client = Client(host="http://localhost:8080")
# Verify Engine Status
status = client.health()
print(f"Engine Status: {status.status}")
```
## Documentation Index
Comprehensive documentation resides in the docs/ folder:
 * docs/architecture/: Detailed architectural system design specifications.
 * docs/api/: OpenAPI schemas and endpoint reference guides.
 * docs/plugins/: Authoring guide for building third-party plugins.
 * docs/contributing/: Developer setup and workflow guidelines.
## Development Workflow
To set up your local development environment for contributing:
```bash
# 1. Fork and clone repository
git clone https://github.com/mkfih3r/eclypsa.git
cd eclypsa
# 2. Setup dev dependencies
make dev-setup
# 3. Create feature branch
git checkout -b feature/my-new-feature
# 4. Run tests before submitting
make test
```
## Branch Strategy
We strictly follow a structured branching model:
 * main: Production-ready releases and stable releases only.
 * develop: Integration branch for functional features targeting the next release milestone.
 * feature/*: Dedicated branches for individual feature development.
 * bugfix/*: Targeted fix branches for verified issues.
 * release/*: Release candidate preparation branches.
## Commit Convention
ECLYPSA AI enforces the **Conventional Commits** specification (v1.0.0).
Commit message structure:
```text
<type>(<scope>): <short summary>
[optional body]
[optional footer(s)]
```
### Supported Types
 * feat: A new feature added to the platform.
 * fix: A bug fix.
 * docs: Documentation changes only.
 * style: Changes that do not affect the meaning of the code (formatting, missing semi-colons).
 * refactor: Code change that neither fixes a bug nor adds a feature.
 * test: Adding missing tests or updating existing tests.
 * chore: Maintenance tasks, dependencies, or build tool updates.
## Versioning
This project adheres to Semantic Versioning 2.0.0:
MAJOR.MINOR.PATCH
 * **MAJOR**: Breaking structural API changes.
 * **MINOR**: Backwards-compatible feature additions.
 * **PATCH**: Backwards-compatible bug fixes and stability patches.
## Roadmap
### Phase 1: Foundation (Current - v0.0.1-alpha)
 * [x] Initial repository architecture and folder organization.
 * [x] Basic CLI framework and configuration parsers.
 * [x] Abstract driver interfaces for inference and tools.
### Phase 2: Core Engine & API (v0.1.0)
 * [ ] Implement complete REST and gRPC API layer.
 * [ ] Develop native local inference driver bindings.
 * [ ] Complete single-step agent loop in agent/.
### Phase 3: Ecosystem & Extensibility (v0.2.0)
 * [ ] Publish stable Python SDK (sdk/python).
 * [ ] Implement dynamic plugin loading runtime (plugins/).
 * [ ] Launch basic Desktop Client shell (desktop/).
## Testing
Testing scripts are located in tests/ and run using the primary Makefile targets:
```bash
# Run unit test suite
make test-unit
# Run integration tests
make test-integration
# Run code coverage reporting
make test-coverage
```
## Security
Security is paramount to the ECLYPSA project.

### Reporting a Vulnerability
Please **DO NOT** report security vulnerabilities through public GitHub issues.
Instead, submit security reports directly to our team via email at security@eclypsa.org or through our confidential vulnerability advisory page on GitHub. We pledge to acknowledge reports within 24 hours and provide regular progress updates.
For more details, see our full SECURITY.md policy.

## Contributing
We welcome community contributions! Please review our guidelines before submitting a pull request:
 1. Read the CONTRIBUTING.md guide.
 2. Sign the Developer Certificate of Origin (DCO) on commits.

 3. Ensure all tests pass and code matches repo style guidelines.

## Code of Conduct
ECLYPSA AI is committed to providing a welcoming, inclusive, and harassment-free environment for all contributors. Please review our CODE_OF_CONDUCT.md before interacting with the project.

## FAQ
#### Q: Is ECLYPSA AI ready for production deployment?

**A:** No. v0.0.1-alpha is a foundation release intended for contributors, architects, and early developers.

#### Q: How does ECLYPSA AI differ from existing agent frameworks?

**A:** ECLYPSA AI is designed as a local-first, engine-decoupled system offering native cross-platform support (CLI, Desktop, Mobile) through a unified client architecture rather than a Python-only script library.

#### Q: Can I run ECLYPSA AI completely offline?

**A:** Yes, local-first execution without external telemetry or remote cloud dependencies is a core design requirement.

## Known Limitations
 * **Alpha Release Constraints:** Public APIs are actively evolving and subject to non-backward-compatible updates prior to v0.1.0.

 * **Plugin Execution Sandbox:** Plugin isolation mechanisms are under active development; third-party plugins should currently be inspected prior to execution.
## Future Plans
 * Enterprise Multi-Node Agent Clustering.
 * Native Hardware Acceleration bindings for Apple Metal, Vulkan, and DirectML.
 * Fine-Grained Role-Based Access Control (RBAC) for Enterprise Deployments.

## Acknowledgements
Special thanks to the open-source communities behind projects like Kubernetes, LangChain, Ollama, FastAPI, and Docker whose operational design standards inspired the ECLYPSA architecture.
## License
ECLYPSA AI is released under the permissive MIT License.
```text

MIT License
Copyright (c) 2026 ECLYPSA AI Authors
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```
## Support
 * **Documentation:** Read the guides in docs/.

 * **GitHub Issues:** Report verified bugs or submit request features via GitHub Issues.

 * **Discord Community:** Join our community for real-time discussions at discord.gg/eclypsa.

## Contact
 * **Project Lead:** ECLYPSA Core Team
 * **Email:** maintainers@eclypsa.org
 * **Website:** [https://eclypsa.org](https://eclypsa.org)

Built with care by the ECLYPSA AI Open Source Community.