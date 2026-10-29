# Remaining Work Plan – AegisCDS (75 % → 100 %)

## 1. High‑Level Goal
Bring the project from the **75 % milestone (v2.8.0‑Enterprise)** to **100 % (v3.0.0‑Enterprise)** while satisfying the final deliverables required for the IE28 Growth Project:
- Full functional parity with the roadmap.
- Complete test coverage (≥ 90 %).
- Production‑ready CI/CD pipeline.
- FDA SaMD regulatory package.
- Documentation and hand‑over material.

---
## 2. Remaining Features & Milestones
| # | Feature | Description | Owner | Est. Effort | Status |
|---|---------|-------------|-------|-------------|--------|
| 1 | **ABDM (Ayushman Bharat Digital Mission) Connector** | Implement sandbox API client, token management, and consent‑flow integration. | Backend Engineer | 4 days | Not started |
| 2 | **Online Reinforcement Learning (RL) Loop** | Capture HITL override feedback, update model weights in‑service, store incremental learning dataset. | ML Engineer | 5 days | Not started |
| 3 | **Multi‑Department Routing** | Extend `department_router.py` to support Nursing, Lab, Pharmacy queues; add config‑driven routing matrix. | Backend Engineer | 3 days | In progress (router scaffold present) |
| 4 | **FDA SaMD Regulatory Compliance Package** | Generate Design History File (DHF), Software‑as‑Medical‑Device (SaMD) risk analysis, and 510(k) style summary. | Regulatory Lead | 4 days | Not started |
| 5 | **Dockerfile & Containerisation** | Multi‑stage Docker build, health‑check, volume mounting for SQLite. | DevOps Engineer | 2 days | Not started |
| 6 | **GitHub Actions CI/CD** | Lint → Unit Tests → Security Scan → Build Docker image → Deploy to GitHub Packages. | DevOps Engineer | 3 days | Not started |
| 7 | **Enhanced UI – Department Dashboard** | New tab “Dept. Dashboard” showing per‑department alert statistics & manual override logs. | Front‑end Engineer | 4 days | Not started |
| 8 | **Comprehensive Documentation** | User Guide, API spec, Architecture diagram, Deployment guide, Test matrix. | Docs Engineer | 3 days | Partial (arch & user guide exist) |
| 9 | **Performance & Load Testing** | Simulate 10 k concurrent EHR events, measure latency, memory, DB I/O. | QA Engineer | 2 days | Not started |
|10| **Final Benchmark Studio Enhancements** | Add CSV export, automatic scoring report, versioned result archive. | Backend Engineer | 2 days | Not started |

---
## 3. Detailed Implementation Steps
### 3.1 ABDM Connector (`abdm_connector.py`)
1. Create client class using `requests` with base URL `https://sandbox.abdm.gov.in/api/v1/`.
2. Implement:
   - `authenticate(self, client_id, client_secret)` → OAuth2 client‑credentials flow.
   - `generate_consent(self, patient_abha_id)` → POST `/consent/create`.
   - `fetch_patient_data(self, abha_id)` → GET `/patient/{abha_id}`.
3. Add caching layer (`functools.lru_cache`) for static lookup tables.
4. Write unit tests under `tests/test_abdm_connector.py` (mock `requests`).
5. Wire the connector into Stage‑1 Temporal Gate – if a patient lacks a valid consent, raise a `ConsentRequired` alert.

### 3.2 Online Reinforcement Learning (`active_learning_engine.py`)
1. Define `FeedbackRecord` dataclass storing `event_id`, `timestamp`, `override_action`, `justification`.
2. Store records in a new SQLite table `rl_feedback`.
3. Implement incremental update function that calls `model.partial_fit` on the new sample.
4. Trigger the update via a background daemon (`python -m aegis.active_learning_daemon`).
5. Add health‑check endpoint `/api/v1/rl/status`.
6. Tests: simulate override streams and verify model AUC improves > 0.02 after 500 samples.

### 3.3 Multi‑Department Router (`department_router.py`)
- Extend existing stub with a routing map, e.g.:
```python
ROUTE_MAP = {
    "physician": ["alert", "bundle"],
    "nurse": ["vital_check", "med_admin"],
    "lab": ["stat_order", "result_review"],
    "pharmacy": ["order_dispense", "dose_adjust"]
}
```
- Add `route(event)` method returning the appropriate queue and enqueue via Redis (or in‑memory list for now).
- Add tests `tests/test_department_router.py` covering each path.

### 3.4 FDA SaMD Package
1. **Design History File (DHF)** – markdown `regulatory/DHF.md` summarising intended use, risk class (Class II), verification & validation results.
2. **Risk Management** – follow IEC 62304; produce `regulatory/risk_analysis.xlsx`.
3. **Labeling & IEC 82304‑1** – create `regulatory/SaMD_Label.pdf`.
4. Add a Makefile target `make regulatory-package` to zip everything.

### 3.5 Dockerfile
```Dockerfile
# ---- Builder ----
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry export -f requirements.txt --output requirements.txt
COPY . .
RUN pip install -r requirements.txt

# ---- Runtime ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "-m", "src.server"]
```
- Add `.dockerignore` for `__pycache__`, `.git`, `tests/`.

### 3.6 GitHub Actions CI/CD (`.github/workflows/ci.yml`)
Jobs:
- **lint** – `ruff check && mypy`.
- **test** – `pytest -q --cov=src`.
- **security** – `bandit -r src`.
- **build** – build Docker image and push to GitHub Packages (requires `GH_TOKEN`).
- **deploy** – manual approval to a test Kubernetes cluster.

### 3.7 UI – Department Dashboard
1. Add React component `DeptDashboard.jsx` under `frontend/src/components/`.
2. Create endpoint `/api/v1/department/stats` returning JSON counters.
3. Display a bar chart (recharts) and a table of recent overrides.
4. Update navigation menu to include the new tab.
5. Write Cypress E2E test `cypress/integration/dept_dashboard_spec.js`.

### 3.8 Documentation
- Update mermaid architecture diagram with ABDM and RL blocks.
- Generate API reference with `mkdocstrings`.
- Write Deployment Guide (Docker Compose + Helm).
- Add “Online Learning” chapter to User Guide.
- Publish all docs via GitHub Pages (GitHub Action).

### 3.9 Performance & Load Testing
- Use `locust` script `load_test.py` targeting `/api/v1/alert/ingest`.
- Run 100 users ramp‑up over 2 min, hold 5 min.
- Capture average latency (< 200 ms) and CPU < 70 %.
- Save results to `performance/report_$(date +%F).md`.

### 3.10 Benchmark Studio CSV Export
- Extend `benchmark_runner.py` to `df.to_csv('benchmark_results.csv', index=False)`.
- Add UI button “Export CSV” on the Benchmark tab.

---
## 4. Timeline (10 working days total)
| Day | Activity |
|-----|----------|
| 1‑2 | ABDM connector implementation + unit tests |
| 3‑4 | Online RL engine + daemon, integrate with HITL flow |
| 5   | Complete multi‑department router and its tests |
| 6   | Dockerfile, CI workflow, initial pipeline run |
| 7   | UI Department Dashboard + UI tests |
| 8   | Regulatory SaMD package (DHF, risk analysis) |
| 9   | Performance/load testing, benchmark CSV export |
|10   | Documentation polish, repo clean‑up, tag `v3.0.0‑Enterprise` |

---
## 5. Acceptance Criteria (Project 100 % Complete)
1. All roadmap items implemented and passing their test suites.
2. CI pipeline green on every push (lint, security, tests, Docker build).
3. Docker image runs locally (`docker compose up`) with health‑check at `http://localhost:8080/health`.
4. Regulatory package archived and signed off by the project supervisor.
5. User documentation published on GitHub Pages and linked from the README.
6. Demo video (≤ 5 min) showing end‑to‑end flow: patient data ingestion → ABDM consent → multi‑dept routing → RL‑updated model → final order dispatch.

---
## 6. Immediate Scaffold Commands (sandbox‑safe)
```bash
# Create new Python modules
mkdir -p src/engine
touch src/engine/abdm_connector.py src/engine/active_learning_engine.py

# Add Dockerfile (copy from example if you have one)
cp Dockerfile.example Dockerfile

# Add CI workflow template
mkdir -p .github/workflows
cp ci_template.yml .github/workflows/ci.yml
```
After scaffolding, fill each file with the snippets above, write corresponding tests, commit, and push.

---
*End of Remaining Work Plan*

