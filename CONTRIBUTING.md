```markdown
# Contributing to ECLYPSA AI

First off, thank you for considering contributing to ECLYPSA AI! It's contributors like you who make open-source software such a powerful tool for learning, building, and innovating.

The following is a set of guidelines and best practices for contributing to the ECLYPSA AI repository. Following these rules helps us keep the codebase clean, maintain high quality, and process your contributions quickly.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Code Style](#code-style)
- [Questions and Support](#questions-and-support)

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please treat all community members with respect, empathy, and professionalism regardless of background or experience level.

---

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the existing GitHub Issues to ensure the bug hasn't already been reported.

When creating an issue, please include as much detail as possible:

1. **Use a clear and descriptive title.**
2. **Describe the exact steps to reproduce the issue.**
3. **Provide your environment details** (Python/Node version, OS, framework versions, hardware specifications if relevant).
4. **Include expected vs. actual behavior.**
5. **Paste error logs and stack traces** using code blocks.

### Suggesting Enhancements

If you have an idea for a new feature, model integration, or pipeline optimization:

1. Check existing issues to see if the feature is already under discussion.
2. Open a new issue with the tag `enhancement`.
3. Explain **why** this feature would be useful and **how** you propose implementing it.
4. Include mockups, architecture diagrams, or pseudo-code if applicable.

### Submitting Pull Requests

1. **Fork the repository** and create your branch from `main`.
2. Ensure your code follows the repository's coding standards and passes all tests.
3. If you've added new features, include corresponding tests and update relevant documentation.
4. Reference any issue(s) your PR resolves (e.g., `Fixes #42`).
5. Wait for a maintainer to review your PR. Be open to feedback and necessary revisions.

---

## Development Workflow

1. **Fork and Clone:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/ECLYPSA-AI.git](https://github.com/YOUR-USERNAME/ECLYPSA-AI.git)
   cd ECLYPSA-AI

```
 2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/your-bug-fix
   
   ```
 3. **Install Dependencies:**
   Ensure you set up a virtual environment or isolated environment according to the project setup guide.
 4. **Run Tests:**
   Run the test suite locally before pushing your changes to ensure nothing is broken.
 5. **Commit and Push:**
   ```bash
   git add .
   git commit -m "feat: brief description of your change"
   git push origin feature/your-feature-name
   
   ```
## Style Guides
### Git Commit Messages
We follow Conventional Commits format to maintain a readable history:
 * feat: A new feature.
 * fix: A bug fix.
 * docs: Documentation changes.
 * style: Formatting changes that do not affect code logic (linting, whitespace).
 * refactor: Code changes that neither fix a bug nor add a feature.
 * test: Adding or updating tests.
 * chore: Updates to build tasks, package managers, or project configurations.
**Example:**
```
feat(pipeline): add support for streaming inference responses

```
### Code Style
 * Write clean, self-documenting code with clear variable and function names.
 * Add type hints where applicable.
 * Keep functions modular and focused on a single responsibility.
 * Document classes and complex functions with inline docstrings.
## Questions and Support
If you have questions about the codebase, architectural decisions, or setting up your development environment, feel free to start a discussion in the GitHub Discussions section or open an issue labeled question.
Thank you for helping build ECLYPSA AI!
```

```