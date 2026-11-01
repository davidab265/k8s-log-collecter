# Contributing to Kubernetes Log Collector for Loki

Thank you for your interest in contributing! We welcome bug reports, feature requests, documentation improvements, and code contributions.

---

## Code of Conduct

We are committed to providing a welcoming, inclusive, and harassment-free environment for everyone. Please be respectful, constructive, and kind in all interactions.

---

## Ways to Contribute

- **Report a Bug**: Open an issue describing what happened, steps to reproduce, and your environment.
- **Suggest an Enhancement**: Open an issue detailing the use case and why it's useful.
- **Submit a Pull Request**: Fix a bug, add a feature, or improve docs / tests.

---

## Development Setup

### Prerequisites

- **Python**: 3.10 or newer
- **kubectl** access to a Kubernetes cluster (or `minikube` / `kind`) for end-to-end testing

### Clone & Install

```bash
git clone https://github.com/davidab265/k8s-log-collecter.git
cd k8s-log-collecter

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Locally

```bash
export LOKI_URL="http://localhost:3100/loki/api/v1/push"
export NAMESPACE="default"
export INTERVAL="30"
export CONTAINER_NAMES="app"
python k8s_to_loki.py
```

---

## Testing

Verify the script compiles and the image builds before opening a PR:

```bash
python -m py_compile k8s_to_loki.py
docker build -t k8s-log-collector:test .
```

---

## Pull Request Guidelines

1. **Branch Naming**: Use descriptive names like `fix/timestamp-parsing`, `feat/retry-backoff`, `docs/rbac-guide`.
2. **Commit Messages**: Follow standard conventional commits when possible (`feat: ...`, `fix: ...`, `docs: ...`).
3. **Keep PRs Focused**: One bug or feature per PR.
4. **No Cluster-Specific Values**: Don't commit internal registry URLs, namespaces, or cluster endpoints — keep manifests generic.

---

## Security Vulnerabilities

If you discover a security vulnerability, please **do not** open a public issue. See [SECURITY.md](./SECURITY.md) for instructions on confidential reporting.

---

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](./LICENSE).
