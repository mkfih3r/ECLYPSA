# Changelog

All notable changes to the ECLYPSA AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Experimental support for dynamic multi-agent task routing.
- Initial draft of automated model benchmark evaluation scripts.

---

## [1.0.0] - 2026-07-25

### Added
- Core architecture launch for the ECLYPSA AI pipeline.
- Streaming inference engine supporting real-time response generation.
- Built-in tool calling framework for external API and database integration.
- Context window optimization module with selective memory compression.
- Comprehensive security guidelines, issue templates, and community standards (`SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`).
- Automated CI/CD pipeline for unit testing and code linting.

---

## [0.2.0] - 2026-06-10

### Added
- Multi-provider model configuration support (OpenAI, Anthropic, Hugging Face local instances).
- Structured JSON output parser with strict schema validation.
- Standardized logging and telemetry pipeline for token tracking and latency metrics.

### Changed
- Refactored prompt routing logic to improve token throughput by 25%.
- Updated memory manager to prune low-relevance conversation fragments dynamically.

### Fixed
- Fixed memory leak in websocket connections during high-concurrency streaming.
- Resolved race condition during multi-threaded tool execution.

---

## [0.1.0] - 2026-05-01

### Added
- Initial public pre-release proof-of-concept (PoC).
- Basic prompt execution engine with single-turn chat completion.
- Configurable environment setup and base CLI execution interface.

[Unreleased]: https://github.com/mkfih3r/ECLYPSA/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/mkfih3r/ECLYPSA/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/NexarAcademy/ECLYPSA-AI/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/NexarAcademy/ECLYPSA-AI/releases/tag/v0.1.0