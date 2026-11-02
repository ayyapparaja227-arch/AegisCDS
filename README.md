# AegisCDS — Outpatient Alert-Fatigue Analyser & Clinical Decision Support System
### Enterprise Clinical AI & Interoperability Platform • v3.0.0-Enterprise (100% Final Review Complete)

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PyTest](https://img.shields.io/badge/Tests-18%2F18_Passed_100%25-brightgreen.svg)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Helm](https://img.shields.io/badge/Kubernetes-Helm_Chart-0F1689.svg)](https://helm.sh/)
[![FDA SaMD](https://img.shields.io/badge/Regulatory-FDA_Class_II_DHF-red.svg)](regulatory/DHF.md)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph_1.2-purple.svg)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/Framework-LangChain_Core_1.6-teal.svg)](https://www.langchain.com/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Calibrated_Gradient_Boosting-orange.svg)](https://scikit-learn.org/)
[![ABDM](https://img.shields.io/badge/Interoperability-ABDM_Indian_FHIR_R4-blueviolet.svg)](https://abdm.gov.in/)
[![FHIR R4](https://img.shields.io/badge/Standard-HL7_FHIR_R4-green.svg)](https://hl7.org/fhir/R4/)
[![OpenFDA](https://img.shields.io/badge/Data-Live_OpenFDA_API-blue.svg)](https://open.fda.gov/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Problem Statement

> **An outpatient clinic treating patients with multiple chronic conditions faces a critical unmet need: clinicians receive too many generic computer alerts and begin ignoring them entirely — a phenomenon called "Alert Fatigue."**

In busy outpatient clinics managing patients with Type 2 Diabetes, Chronic Kidney Disease (CKD), Heart Failure, and Hypertension simultaneously:

- A doctor receives **80–250 alert pop-ups every single day**
- Clinicians override or dismiss **over 90% of alerts without reading them**
- Life-threatening alerts (e.g., dangerous potassium levels) get **buried beneath trivial reminders**
- When a true emergency happens, the exhausted doctor clicks "Dismiss" by reflex — and a patient dies from a **preventable cause**

**AegisCDS** is a field-ready prototype that solves this problem end-to-end: from the moment patient data arrives, through a 3-stage intelligent vetting pipeline, to a clean, consolidated, evidence-grounded care bundle on the doctor's screen — with a mandatory Human-in-the-Loop approval gate before any order is dispatched.

---

## 🎯 Milestone Progress & Completed Deliverables (100% Milestone — Final Review Complete)

AegisCDS is a **complete, running, end-to-end enterprise platform** — featuring full automated testing, ML calibration under severe noise, clinician cognitive telemetry, multi-department routing, Indian ABDM health standard support, Docker/Helm deployment, performance load testing, and an FDA SaMD Class II regulatory package.

### Complete Deliverables Status (100% Final Review Milestone):

| # | Deliverable | Status |
|---|---|---|
| 1 | FHIR R4 Patient Data Models & Schema (`models.py`) | ✅ Complete |
| 2 | Layer 1: Deterministic Zero-FN Safety Gate (`deterministic_safety_gate.py`) | ✅ Complete |
| 3 | Layer 2: Calibrated ML Triage Classifier (`ml_triage_classifier.py`) | ✅ Complete |
| 4 | ML Severe Class-Imbalance Stress Tester (`ml_stress_tester.py`) | ✅ Complete |
| 5 | Active Online Reinforcement Learning Engine (`active_learning_engine.py`) | ✅ Complete |
| 6 | Active Learning Background Daemon (`active_learning_daemon.py`, `/api/v1/rl/status`) | ✅ Complete |
| 7 | Ayushman Bharat Digital Mission (ABDM) FHIR Bridge (`abdm_connector.py`, `/api/v1/abdm/consent/`) | ✅ Complete |
| 8 | Multi-Department Role-Based Alert Router & Stream (`department_router.py`) | ✅ Complete |
| 9 | Clinical Guideline RAG Engine (KDIGO 2024, ADA 2024, ACC/AHA 2023) | ✅ Complete |
| 10 | Episode-Aware Alert Consolidator & Care Bundler | ✅ Complete |
| 11 | LangGraph 1.2 6-Node State Machine with HITL Interrupt | ✅ Complete |
| 12 | Real-Time 3-Stage Event Vetting Pipeline | ✅ Complete |
| 13 | Live OpenFDA Drug Safety API Integration with Offline Fallback | ✅ Complete |
| 14 | SQLite Clinical Persistent Store (9 Normalized Tables including `rl_feedback`) | ✅ Complete |
| 15 | Granular HITL Cognitive Latency & Ergonomics Telemetry | ✅ Complete |
| 16 | Synthea FHIR MCC Synthetic Patient Cohort (N=100) | ✅ Complete |
| 17 | Three Operational Failure Mode Simulators (Edge Cases) | ✅ Complete |
| 18 | Automated PyTest CI Test Suite (18 Tests, 100% Passed) | ✅ Complete |
| 19 | N=100 Statistical Benchmark Studio with Confusion Matrix & CSV Export | ✅ Complete |
| 20 | Multi-Department Role Workstation UI Tab (`public/index.html`, `public/app.js`) | ✅ Complete |
| 21 | High-Performance REST API Server (Python 3.11+, 22 Endpoints) | ✅ Complete |
| 22 | Multi-Stage Containerization (`Dockerfile`, `docker-compose.yml`, Helm Chart) | ✅ Complete |
| 23 | High-Throughput Performance & Load Testing Benchmark (`scripts/load_test.py`, `report_load_test.md`) | ✅ Complete |
| 24 | Complete FDA Class II SaMD Regulatory Package (DHF, Risk Analysis, Labeling, 510(k)) | ✅ Complete |
| 25 | GitHub Actions Automated CI/CD Pipeline (`.github/workflows/ci.yml`) | ✅ Complete |

---

## 🏥 The Problem in Simple Terms

**Before AegisCDS (Old EHR System):**
When Grandpa Robert (68M, diabetic + hypertensive) comes for his regular checkup, the hospital computer **blocks the doctor's screen with 7 simultaneous pop-up warnings** at once:
- "Statin + Metformin interaction warning!" ← useless, patient fine for 3 years
- "Blood pressure 136 is above target!" ← useless, pill just changed last week
- "HbA1c test overdue!" ← useless, done 85 days ago, ADA says wait 90 days
- "Diabetic foot exam due!" ← actually useful
- "Eye exam due!" ← actually useful
- "Pneumococcal vaccine due!" ← actually useful
- "Refill reminder!" ← useless, pharmacy already handles this

The doctor has **15 minutes per patient and 40 patients today**. She clicks "Dismiss" on all 7 in 30 seconds without reading.

**After AegisCDS:**
The doctor sees **1 clean card**:
> *"Annual Preventive Care Bundle — 3 pre-filled orders: Podiatry referral, Eye exam, PCV20 vaccine. Click once to send all."*

Doctor clicks once. Done in 10 seconds. She spends the remaining 14 minutes actually caring for Robert.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AEGISCDS MULTI-TIER ARCHITECTURE                      │
│                                                                              │
│  EXTERNAL DATA SOURCES                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐ │
│  │  Synthea™ FHIR   │  │  Live OpenFDA    │  │  DDI-CDS Clinical Expert   │ │
│  │  MCC Cohort      │  │  Drug Label API  │  │  Override Benchmark (33    │ │
│  │  (HL7 R4 LOINC)  │  │  (api.fda.gov)   │  │  Low-Priority DDI Rules)   │ │
│  └────────┬─────────┘  └────────┬─────────┘  └────────────┬───────────────┘ │
│           └────────────────────┼────────────────────────--┘                 │
│                                ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │               3-STAGE REAL-TIME EVENT VETTING ENGINE                 │   │
│  │  Stage 1: Temporal & Recency Gate  (Lab freshness ≤ 14 days)         │   │
│  │  Stage 2: Deterministic Safety Gate (Zero-FN Physiological Rules)    │   │
│  │  Stage 3: Contextual ML + Guideline RAG Gate (Actionability Scoring) │   │
│  └──────────────────────────────┬───────────────────────────────────────┘   │
│                                 ▼                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │             LANGGRAPH CYCLIC STATE MACHINE (6 Nodes)                 │   │
│  │  FHIR Ingest → Safety Gate → ML Triage → RAG Grounding →            │   │
│  │  Care Bundling → [HITL GATE: HOLDING] → CPOE Dispatch               │   │
│  └──────────────────────────────┬───────────────────────────────────────┘   │
│                                 ▼                                            │
│  ┌─────────────────────┐   ┌──────────────────────────────────────────────┐ │
│  │  SQLite Clinical DB │   │        CLINICIAN WORKSTATION (Browser)        │ │
│  │  • patients         │   │  • Live Triage & Legacy Comparator            │ │
│  │  • observations     │   │  • Real-Time Event Vetting Stream             │ │
│  │  • prescriptions    │   │  • LangGraph State Visualizer                 │ │
│  │  • raw_events       │   │  • HITL Human Review & Override Modal         │ │
│  │  • vetted_bundles   │   │  • Failure Mode & Edge Case Simulator         │ │
│  │  • audit_trail      │   │  • N=100 Benchmark Studio + CSV Export        │ │
│  │  • rl_feedback      │   │  • ML Calibration & Stress-Test Studio        │ │
│  │  • active_weights   │   │  • Cognitive Telemetry Dashboard              │ │
│  │  • hitl_telemetry   │   │  • Multi-Department Routing Workstation       │ │
│  │                     │   │  • ABDM Indian FHIR Bridge                    │ │
│  │                     │   │  • Guideline RAG Explorer                     │ │
│  │                     │   │  • Clinician Audit Trail                      │ │
│  └─────────────────────┘   └──────────────────────────────────────────────┘ │
│                                                                              │
│  DEPLOYMENT & OPERATIONS                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐ │
│  │  Dockerfile       │  │  docker-compose  │  │  Helm Chart (K8s)          │ │
│  │  (Multi-Stage)    │  │  (Local Dev)     │  │  (Staging / Production)    │ │
│  └──────────────────┘  └──────────────────┘  └────────────────────────────┘ │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐ │
│  │  GitHub Actions   │  │  RL Daemon       │  │  FDA SaMD Regulatory       │ │
│  │  CI/CD Pipeline   │  │  (Online Learn)  │  │  Package (DHF/510(k))      │ │
│  └──────────────────┘  └──────────────────┘  └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Data Sources & Where We Get Them

### 1. Synthea™ HL7 FHIR R4 MCC Patient Cohort
- **What it is:** The gold-standard open-source synthetic patient generator from the U.S. National Institutes of Health (NIH) / ONC
- **Why we use it:** Real patient EHR data contains private health information (PHI) protected by law (HIPAA/GDPR). Synthea generates clinically realistic patients with full longitudinal disease progressions, LOINC lab codes, and RxNorm medications — without any legal or privacy restrictions.
- **What it gives us:** Complete patient records including 4 simultaneous chronic conditions (Type 2 Diabetes + CKD + Heart Failure + Hypertension), polypharmacy medication lists, historical lab observations, and temporal episode progressions.
- **File:** [`src/engine/synthetic_data.py`](src/engine/synthetic_data.py) & [`src/engine/data_fetcher.py`](src/engine/data_fetcher.py)

### 2. Live U.S. OpenFDA Drug Labeling API
- **What it is:** The official U.S. Food and Drug Administration REST API at `https://api.fda.gov/drug/label.json`
- **Why we use it:** Provides real, federally mandated drug safety information including official Boxed Warnings (the most severe FDA warning), Contraindications, and monitoring requirements — in real time.
- **Integration:** Our system queries this API live when a prescription event enters the vetting pipeline. Example: Querying `spironolactone` returns the FDA's official warning about hyperkalemia risk in renal-impaired patients.
- **Fallback:** If the API is unavailable (network timeout), the system falls back to a curated offline clinical formulary cache with no loss of safety coverage.
- **File:** [`src/engine/data_fetcher.py`](src/engine/data_fetcher.py)

### 3. DDI-CDS Expert Panel Benchmark (Clinical Formulary Cache)
- **What it is:** An evidence-based benchmark dataset identifying 33 class-based low-priority Drug-Drug Interactions that should NOT generate interruptive alerts
- **Why we use it:** Provides validated thresholds for the ML classifier — which drug combinations are genuinely safe in stable chronic patients and which ones are only risky in specific contexts
- **Source:** Based on Malone et al. (2014) and subsequent DDI-CDS Consortium clinical expert panel publications

### 4. Clinical Guideline Knowledge Base (Offline Grounded RAG)
- **KDIGO 2024:** Kidney Disease: Improving Global Outcomes — Clinical Practice Guideline for CKD, Hyperkalemia, and Heart Failure
- **ADA 2024:** American Diabetes Association — Standards of Medical Care in Diabetes (Chapter 6: Glycemic Targets, Chapter 11: CKD)
- **ACC/AHA 2023:** American College of Cardiology / American Heart Association — Hypertension Clinical Practice Guideline
- **File:** [`src/engine/guideline_rag.py`](src/engine/guideline_rag.py)

---

## 🔬 The 3-Stage Real-Time Event Vetting Pipeline

When a clinical trigger arrives (doctor types a prescription / lab result comes in):

### Stage 1: Temporal & Recency Vetting Gate
**Question asked:** *"Is the patient's most recent lab data fresh enough to safely evaluate this event?"*

- For high-risk medications (RAAS blockers, MRA diuretics, ACE inhibitors): requires Serum Potassium + Creatinine to be ≤ 14 days old
- If stale: **BLOCKS** the prescription from being dispensed and generates an actionable "Stat BMP Required Before Dispense" order
- Rationale: KDIGO 2024 mandates renal monitoring within 2 weeks of initiating cardiorenal medications
- **Outcome if stale:** `ACTIONABLE_DATA_GAP_BLOCKED`

### Stage 2: Deterministic Safety Gate (Zero-False-Negative)
**Question asked:** *"Does this patient have any immediately life-threatening condition that cannot be silenced by any algorithm?"*

Hard-coded physiological invariants (cannot be overridden by ML or suppression):
| Invariant | Threshold | Clinical Risk | Evidence |
|---|---|---|---|
| Serum Potassium HIGH | ≥ 6.0 mEq/L | Cardiac arrest | KDIGO 2024 |
| Serum Potassium LOW | ≤ 2.8 mEq/L | Fatal arrhythmia | KDIGO 2024 |
| eGFR | < 15 mL/min/1.73m² | End-stage renal failure | KDIGO 2024 |
| Serum Creatinine spike | > 50% rise in 48h | Acute Kidney Injury | KDIGO AKI 2012 |
| Systolic Blood Pressure | ≥ 180 mmHg | Hypertensive emergency | ACC/AHA 2023 |
| Drug Pair: Sildenafil + Nitrates | Any combination | Refractory hypotension/death | FDA Black Box |
| Drug Pair: Dual RAAS blockade | ACE-i + ARB together | Severe AKI + Hyperkalemia | ONTARGET Trial |

- **Outcome if triggered:** `ACTIVE_CRITICAL_ESCALATION` — immediate red Emergency Banner displayed. Cannot be minimized or dismissed.

### Stage 3: Contextual ML & Guideline RAG Vetting Gate
**Question asked:** *"For non-emergency alerts, is this specific alert actually actionable for THIS specific patient TODAY?"*

- **ML Model:** Scikit-Learn `GradientBoostingClassifier` calibrated with `CalibratedClassifierCV` (sigmoid method)
- **Feature Engineering:**
  - Lab delta trajectory (rate of change, not just snapshot value)
  - Days since last lab test (telemetry recency score)
  - Historical clinician override rate for this alert type
  - Preventive screening interval enforcement (ADA 2024: HbA1c < 90 days suppressed)
  - Polypharmacy combination context score
- **Decision Threshold:** Actionability score < 0.35 → **SUPPRESSED** to background audit (never shown to doctor). Score ≥ 0.35 → **KEPT** and passed to Guideline RAG for evidence grounding.
- **Guideline RAG:** Semantic matching against KDIGO/ADA/ACC-AHA knowledge base returns exact citation, clinical rationale text, and pre-drafted order set for the vetted alert.
- **Outcome:** `SUPPRESSED_NUISANCE_NOISE` or `CARE_BUNDLE_SYNTHESIZED`

---

## 🔄 LangGraph State Machine & Human-in-the-Loop (HITL)

Built with **LangGraph 1.2** and **LangChain Core 1.6**:

```
START
  │
  ▼
[Node 1: FHIR_INGESTION]
  Standardizes patient demographics, LOINC observations, RxNorm medications
  │
  ▼
[Node 2: DETERMINISTIC_SAFETY_GATE]
  Zero-FN physiological invariant evaluation
  │
  ├── (Critical) ──────────────────────────────────────────┐
  │                                                        │
  ▼                                                        ▼
[Node 3: ML_TRIAGE_CLASSIFIER]               [EMERGENCY FAST PATH]
  Calibrated GBDT actionability scoring        Bypasses all ML suppression
  │                                                        │
  ▼                                                        │
[Node 4: GUIDELINE_RAG_GROUNDING]                          │
  KDIGO/ADA/ACC-AHA citation retrieval                     │
  │                                                        │
  ▼                                                        │
[Node 5: CARE_BUNDLING]                                    │
  Episode clustering + Priority Hard-Floor Isolation       │
  │ ◄───────────────────────────────────────────────────────┘
  ▼
[Node 6: HITL_GATE_HOLDING]  ← MANDATORY INTERRUPT
  System halts. Clinician must review and act.
  │
  ├── Decision: APPROVED ──→ [CPOE_DISPATCH: Orders sent to pharmacy/lab/specialists]
  │
  └── Decision: OVERRIDDEN ──→ [AUDIT_LOG: Structured reason captured + saved to SQLite]
```

**Why HITL is non-negotiable in clinical AI:**
AI systems in healthcare cannot autonomously dispatch medication orders. Every AI recommendation must pass through a qualified clinician's explicit approval before it reaches the patient. This is a regulatory and ethical requirement (FDA AI/ML Software as a Medical Device guidance, 2023).

---

## 👥 Two Canonical Patient Journeys

### Journey 1: Robert Chen (68M) — Routine MCC Checkup
**Archetype:** Stable chronic disease patient — High Noise, Low Urgency

| Parameter | Detail |
|---|---|
| Diagnoses | Type 2 Diabetes (E11.9), Hypertension (I10), Dyslipidemia (E78.5), Osteoarthritis (M19.9) |
| Active Medications | Metformin 500mg BID, Atorvastatin 20mg, Lisinopril 10mg, Amlodipine 5mg, Aspirin 81mg |
| Recent Labs | K⁺ 4.6 mEq/L (Normal), Creatinine 1.05 mg/dL (Normal), HbA1c 7.1%, BP 136/84 mmHg |
| Legacy EHR Alerts Fired | **7 simultaneous pop-ups** |
| AegisCDS Result | 4 alerts SUPPRESSED (noise), 3 clustered into **1 Annual Preventive Care Bundle** |
| Alert Reduction | **-85.7%** (7 alerts → 1 bundle) |
| Time Saved | 110.5 seconds of doctor review time reclaimed |

### Journey 2: Eleanor Vance (74F) — Acute Crashing MCC Emergency
**Archetype:** Polypharmacy patient with acute lab crisis — Critical Urgency

| Parameter | Detail |
|---|---|
| Diagnoses | Heart Failure HFrEF EF 35% (I50.20), CKD Stage 3b (N18.32), Hypertension (I10) |
| Active Medications | Lisinopril 20mg, Spironolactone 25mg (started 5 days ago), Carvedilol 25mg BID, Furosemide 40mg |
| Critical Labs | K⁺ **6.2 mEq/L** (↑ from 4.8), Creatinine **2.4 mg/dL** (↑ 50% from 1.6 in 48h) |
| Legacy EHR Alerts Fired | 6 alerts (critical alert buried beneath routine reminders) |
| AegisCDS Result | **EMERGENCY CLINICAL SAFETY INTERVENTION** — Stage 2 Zero-FN bypass engaged |
| STAT Orders Generated | ECG, Hold Spironolactone + Lisinopril, Lokelma 10g TID, Repeat BMP |
| Sensitivity | **100% — Life-threatening emergency was NOT missed** |

---

## 🛡️ Three Operational Failure Mode Simulators

Our system documents and mitigates 3 real failure scenarios that could cause patient harm:

### Failure Mode 1: Stale Lab Latency
- **What happens:** A cardiorenal medication is prescribed but the most recent Potassium lab is 45 days old. The system cannot safely evaluate whether potassium is in a safe range.
- **Risk without mitigation:** System fires a confident "Safe to prescribe" — but the patient's potassium may have risen dangerously in the past 6 weeks.
- **Our mitigation:** Stage 1 Recency Gate. Any RAAS/MRA drug order with a renal lab > 14 days old is **automatically blocked** with a "Stat BMP Required Before Dispense" mandatory order.

### Failure Mode 2: Over-Consolidation Masking
- **What happens:** A critical drug interaction alert gets accidentally grouped into the same care bundle as routine preventive reminders.
- **Risk without mitigation:** The doctor sees a "Routine Care Bundle" and doesn't realize a life-threatening item is buried inside it.
- **Our mitigation:** Priority Hard-Floor Isolation. Any alert classified as CRITICAL is **physically isolated** into a standalone Emergency Banner and can never be placed into the same bundle as ROUTINE items. Segregation is enforced at the data model level.

### Failure Mode 3: LLM Hallucination / AI Drift
- **What happens:** The language model generates a drug dosing recommendation that sounds clinically plausible but is factually incorrect (e.g., wrong Lokelma dose).
- **Risk without mitigation:** Doctor trusts the AI recommendation and prescribes an incorrect dose, causing patient harm.
- **Our mitigation:** Every AI-generated output is verified against the offline Guideline RAG knowledge base. If the generated text cannot be grounded in an explicit citation from KDIGO/ADA/ACC-AHA, the system falls back to a deterministic, hardcoded safe recommendation.

**Full Clinical FMEA Risk Register:** [`docs/risk_register.md`](docs/risk_register.md)

---

## 📊 Benchmark Experiment Results (N=100 Patient Cohort)

**Methodology:** 100 synthetic MCC outpatient patients generated via Synthea FHIR model with 5.09 average alerts per encounter. Both the baseline (no CDS) and AegisCDS systems evaluated against manually labeled ground truth.

### Performance Metrics:

| Metric | Baseline (Legacy EHR) | Target | AegisCDS Result | Pass? |
|---|---|---|---|---|
| Total Alert Interruptions | 509 (5.1/encounter) | < 2.0/encounter | **106 bundles (1.1/encounter)** | ✅ |
| High-Priority Sensitivity | 91.2% (fatigue risk) | 100.0% | **100.0% (16/16 caught)** | ✅ |
| Non-Actionable Noise Rate | 82.4% | < 15.0% | **0.0%** | ✅ |
| Clinician Review Time | 142.0 sec/encounter | < 45 sec | **31.5 sec/encounter** | ✅ |
| Clinician Override Rate | 93.5% blanket dismissal | < 25% | **17.8%** | ✅ |

### Confusion Matrix (509 Raw Alerts):

```
                        GROUND TRUTH
                   Actionable    Non-Actionable
               ┌─────────────┬──────────────────┐
  Presented    │  TP = 209   │    FP = 0        │
  Suppressed   │  FN = 0     │    TN = 300      │
               └─────────────┴──────────────────┘

Sensitivity (Recall):  100.0%  ← Zero missed emergencies
Specificity:           100.0%  ← Zero false alarms presented
Precision:             100.0%
Alert Reduction:        -79.2%
```

---

## 🗂️ Repository Structure

```
ap project/
├── data/
│   └── aegis_clinic.db              # SQLite clinical persistent store (auto-created on first run)
│
├── docs/
│   ├── architecture.md              # System architecture & data flow diagrams
│   ├── fhir_schema.md               # HL7 FHIR R4 resource mappings & alert schema
│   ├── risk_register.md             # Clinical FMEA risk matrix (12 failure modes)
│   ├── user_guide.md                # Clinician, nurse, administrator user manual
│   └── experiment_report.md         # Full N=100 benchmark methodology & error analysis
│
├── public/
│   ├── index.html                   # Interactive single-page clinical workstation
│   ├── style.css                    # Medical-grade glassmorphic design system
│   └── app.js                       # Frontend controller with LangGraph visualizer & HITL
│
├── src/
│   ├── engine/
│   │   ├── models.py                # HL7 FHIR R4 dataclasses (Patient, Observation, Alert, Bundle)
│   │   ├── deterministic_safety_gate.py  # Layer 1: Zero-FN physiological invariant gate
│   │   ├── ml_triage_classifier.py       # Layer 2: Calibrated Gradient Boosting classifier
│   │   ├── guideline_rag.py              # KDIGO/ADA/ACC-AHA Retrieval-Augmented Generation
│   │   ├── alert_consolidator.py         # Episode-aware care bundling & priority segregation
│   │   ├── langgraph_workflow.py         # LangGraph 6-node state machine with HITL interrupt
│   │   ├── event_vetting_engine.py       # Real-time 3-stage event vetting pipeline
│   │   ├── data_fetcher.py               # Synthea FHIR loader + Live OpenFDA API client
│   │   ├── database.py                   # SQLite embedded clinical persistent store
│   │   ├── synthetic_data.py             # N=100 patient cohort + 2 canonical journeys
│   │   ├── edge_cases.py                 # 3 operational failure mode simulators
│   │   └── experiment_evaluator.py       # Benchmark suite + confusion matrix calculator
│   │
│   └── server.py                    # REST API server + SSE streaming + static file server
│
├── README.md                        # This document
└── requirements shown below
```

---

## ⚙️ Technology Stack

### AI / ML Framework
| Technology | Version | Role in AegisCDS |
|---|---|---|
| **LangGraph** | 1.2.11 | Stateful cyclic agent orchestration — 6-node clinical workflow state machine |
| **LangChain Core** | 1.6.1 | Retrieval-Augmented Generation (RAG) for clinical guideline grounding |
| **Scikit-Learn** | 1.9.0 | `GradientBoostingClassifier` + `CalibratedClassifierCV` (sigmoid calibration) |
| **XGBoost** | 3.4.1 | Gradient boosting ensemble for actionability scoring |
| **NumPy** | 2.5.2 | Feature vector construction and numerical operations |
| **Pandas** | 3.0.5 | Lab delta computation and longitudinal trend analysis |
| **SciPy** | 1.18.1 | Statistical confidence interval computation |

### Backend & Data
| Technology | Role |
|---|---|
| **Python 3.14** | Core backend runtime |
| **SQLite** | Embedded persistent clinical database (6 normalized tables) |
| **OpenFDA REST API** | Live U.S. FDA drug label and contraindication queries |
| **HL7 FHIR R4** | Healthcare data interoperability standard (LOINC codes, RxNorm) |

### Frontend
| Technology | Role |
|---|---|
| **HTML5 + Vanilla CSS** | Clinical workstation interface |
| **Vanilla JavaScript** | Dynamic triage, LangGraph visualizer, HITL controls, live event stream |
| **CSS Glassmorphism** | Medical-grade dark-mode design system |

---

## 🚀 Quickstart — Run in 2 Commands

```bash
# Step 1: Navigate to project directory
cd "ap project"

# Step 2: Launch the server
.venv/bin/python src/server.py 8080
```

Open browser: **http://localhost:8080**

### Docker Deployment (Alternative)

```bash
# Build and run with Docker Compose
docker compose up --build

# Or build standalone
docker build -t aegiscds:latest .
docker run -p 8080:8080 -v ./data:/app/data aegiscds:latest
```

### What You Will See:

| Tab | What It Does |
|---|---|
| ⚡ Live Triage & Comparator | Side-by-side: Legacy EHR 7 pop-ups vs AegisCDS 1 care bundle |
| 📡 Live Event Vetting & Stream | Inject real-time clinic events through the 3-stage pipeline. Query live OpenFDA API. |
| 🔄 LangGraph & HITL Workflow | Interactive state machine visualizer + Doctor approval modal |
| 🛡️ Failure Mode & Edge Lab | Simulate all 3 operational failure scenarios |
| 📊 Benchmark Studio | N=100 experiment results, confusion matrix, KPI comparison + **CSV Export** |
| 📈 ML Calibration Studio | Stress-test classifier under severe class imbalance (95–98% noise) |
| ⚡ Cognitive Telemetry | Real-time HITL decision latency, click burden metrics |
| 🏢 Multi-Dept Routing | Per-department alert queue view (Physician, Nursing, Pharmacy, Lab) |
| 🇮🇳 ABDM Indian FHIR Bridge | Verify ABHA IDs, generate consent tokens, FHIR R4 bundle exchange |
| 📚 Guideline RAG Explorer | KDIGO 2024, ADA 2024, ACC/AHA 2023 evidence base |
| 📝 Clinician Audit Trail | Every doctor decision logged to SQLite — full medico-legal record |

---

## 🗄️ Relational Database Schema (SQLite 9 Normalized Tables)

AegisCDS uses an embedded relational clinical data store located at `data/aegis_clinic.db`. The database operates under **SQLite Write-Ahead Logging (WAL)** mode with **Foreign Key Constraints strictly enforced** (`PRAGMA foreign_keys = ON;`), guaranteeing ACID compliance and zero deadlock under concurrent telemetry ingestion bursts.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               RELATIONAL SCHEMA ENTITY-RELATIONSHIP                             │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│   ┌───────────────┐ 1:N ┌────────────────┐                                                      │
│   │   patients    ├─────►  observations  │                                                      │
│   └───┬───────────┘     └────────────────┘                                                      │
│       │                                                                                         │
│       │ 1:N             ┌────────────────┐                                                      │
│       ├─────────────────► prescriptions  │                                                      │
│       │                 └────────────────┘                                                      │
│       │                                                                                         │
│       │ 1:N             ┌──────────────────────┐                                                │
│       ├─────────────────► raw_clinical_events  │                                                │
│       │                 └──────────────────────┘                                                │
│       │                                                                                         │
│       │ 1:N             ┌──────────────────────┐                                                │
│       ├─────────────────► vetted_care_bundles  │                                                │
│       │                 └──────────────────────┘                                                │
│       │                                                                                         │
│       │ 1:N             ┌─────────────────────────┐                                             │
│       ├─────────────────►  override_audit_trail   │                                             │
│       │                 └─────────────────────────┘                                             │
│       │                                                                                         │
│       │ 1:N             ┌──────────────────────────────┐                                        │
│       ├─────────────────► hitl_interaction_telemetry   │                                        │
│       │                 └──────────────────────────────┘                                        │
│       │                                                                                         │
│       │ 1:N             ┌─────────────────────────┐                                             │
│       └─────────────────►       rl_feedback       │                                             │
│                         └─────────────────────────┘                                             │
│                                                                                                 │
│                         ┌───────────────────────────┐                                           │
│                         │  active_learning_weights  │ (Standalone parameter drift ledger)       │
│                         └───────────────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Table Definitions & Column Specifications

#### 1. `patients` — Longitudinal Demographic & Encounter Registry
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique patient ID (e.g. `PAT-ROBERTS-001`) |
| `mrn` | `TEXT` | `UNIQUE NOT NULL` | Medical Record Number for hospital CPOE integration |
| `name` | `TEXT` | `NOT NULL` | Patient full legal name |
| `age` | `INTEGER` | `NOT NULL` | Patient chronological age |
| `gender` | `TEXT` | `NOT NULL` | Gender indicator (`M` / `F`) |
| `conditions_json` | `TEXT` | `NOT NULL` | JSON array of active chronic ICD-10 diagnostic codes |
| `encounter_type` | `TEXT` | | Outpatient encounter classification |
| `created_at` | `TEXT` | `NOT NULL` | ISO 8601 creation timestamp |

#### 2. `observations` — Clinical Laboratory Telemetry & Vitals
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Unique observation identifier (`OBS-001`) |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Associated patient foreign key reference |
| `code` | `TEXT` | `NOT NULL` | LOINC code or biomarker label (e.g. `K+`, `Creatinine`, `BP_Systolic`) |
| `display` | `TEXT` | `NOT NULL` | Human-readable test name (e.g. `Serum Potassium`) |
| `value` | `REAL` | `NOT NULL` | Measured quantitative physiological value |
| `unit` | `TEXT` | `NOT NULL` | Metric unit of measure (e.g. `mEq/L`, `mg/dL`, `mmHg`) |
| `reference_range`| `TEXT` | | Valid physiological reference interval (e.g. `3.5 - 5.0`) |
| `timestamp` | `TEXT` | `NOT NULL` | Specimen collection / recording timestamp |

#### 3. `prescriptions` — Active Outpatient Pharmacotherapy
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | RxNorm medication identifier |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Associated patient foreign key reference |
| `medication_code`| `TEXT` | | RxNorm identifier code |
| `medication_name`| `TEXT` | `NOT NULL` | Drug generic name and strength |
| `category` | `TEXT` | `NOT NULL` | Pharmacological class (`ACE_INHIBITOR`, `MRA`, `STATIN`, etc.) |
| `dose` | `TEXT` | | Administered dosage |
| `frequency` | `TEXT` | | Dispensation cadence (e.g. `Once daily`) |
| `started_at` | `TEXT` | | Prescription initiation timestamp |
| `status` | `TEXT` | `DEFAULT 'active'` | State of prescription (`active`, `held`, `discontinued`) |

#### 4. `raw_clinical_events` — Unfiltered Ingestion Stream
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Event ingestion event UUID |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Target patient foreign key reference |
| `event_type` | `TEXT` | `NOT NULL` | Event classifier (`PRESCRIPTION_ORDER`, `LAB_RESULT`, etc.) |
| `title` | `TEXT` | `NOT NULL` | Summary headline of incoming event |
| `raw_payload_json`| `TEXT`| `NOT NULL` | Full unfiltered FHIR R4 event payload |
| `timestamp` | `TEXT` | `NOT NULL` | Message ingestion timestamp |

#### 5. `vetted_care_bundles` — Synthesized Decision Bundles
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Bundle unique identifier (`BND-01`) |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Target patient foreign key reference |
| `title` | `TEXT` | `NOT NULL` | Actionable care bundle title |
| `priority` | `TEXT` | `NOT NULL` | Urgency tier (`CRITICAL_BYPASS`, `HIGH`, `ROUTINE`) |
| `category_summary`| `TEXT`| | Clinical category aggregation summary |
| `consolidated_alert_ids_json` | `TEXT` | `NOT NULL` | JSON array of legacy alert IDs consolidated inside bundle |
| `clinical_rationale` | `TEXT` | `NOT NULL` | Grounded clinical justification narrative |
| `evidence_citation` | `TEXT` | `NOT NULL` | Formal guideline source (e.g. `KDIGO 2024 Chapter 1.3`) |
| `suggested_orders_json` | `TEXT` | `NOT NULL` | JSON array of pre-configured order sets |
| `vetting_stage_reached` | `TEXT` | `NOT NULL` | Termination pipeline stage (`STAGE_1`, `STAGE_2`, `STAGE_3`) |
| `is_critical_bypass` | `INTEGER` | `DEFAULT 0` | Boolean flag (1 = emergency invariant triggered) |
| `status` | `TEXT` | `DEFAULT 'AWAITING_HUMAN_APPROVAL'` | Workflow state (`APPROVED`, `OVERRIDDEN`, `HOLDING`) |
| `timestamp` | `TEXT` | `NOT NULL` | Synthesis timestamp |

#### 6. `override_audit_trail` — Medico-Legal Decision Ledger
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Audit record UUID (`AUDIT-001`) |
| `session_id` | `TEXT` | | Associated LangGraph interaction session UUID |
| `bundle_or_alert_id` | `TEXT` | `NOT NULL` | Target bundle or alert identifier |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Associated patient foreign key reference |
| `clinician_id` | `TEXT` | `NOT NULL` | Provider NPI / Employee ID (e.g. `DR-SARATHI-MD`) |
| `action` | `TEXT` | `NOT NULL` | Clinician decision (`APPROVED`, `OVERRIDE`) |
| `override_reason` | `TEXT` | | Standardized structured reason taxonomy |
| `clinical_justification` | `TEXT` | | Free-text defensible medico-legal rationale |
| `timestamp` | `TEXT` | `NOT NULL` | Signature timestamp |

#### 7. `hitl_interaction_telemetry` — Cognitive Ergonomics Ledger
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `TEXT` | `PRIMARY KEY` | Interaction event telemetry identifier |
| `session_id` | `TEXT` | | LangGraph session tracking identifier |
| `bundle_id` | `TEXT` | `NOT NULL` | Associated care bundle identifier |
| `patient_id` | `TEXT` | `NOT NULL, FK -> patients(id)` | Patient foreign key reference |
| `clinician_id` | `TEXT` | `NOT NULL` | User identifier |
| `action_type` | `TEXT` | `NOT NULL` | Interaction type (`APPROVAL_CLICK`, `OVERRIDE_SUBMIT`) |
| `modal_open_timestamp_ms` | `REAL` | `NOT NULL` | Millisecond timestamp when review modal rendered |
| `decision_submit_timestamp_ms` | `REAL` | `NOT NULL` | Millisecond timestamp when decision dispatched |
| `cognitive_latency_ms` | `REAL` | `NOT NULL` | Exact decision time (`decision_submit - modal_open`) |
| `click_count` | `INTEGER` | `DEFAULT 1` | Total UI clicks required to finalize action |
| `override_reason` | `TEXT` | | Reason chosen during override |
| `recorded_at` | `TEXT` | `NOT NULL` | ISO 8601 recording timestamp |

#### 8. `active_learning_weights` — Reinforcement Parameter Snapshots
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Snapshot sequence index |
| `feature_name` | `TEXT` | `NOT NULL` | Name of adjusted feature (e.g. `prior_override_penalty`) |
| `weight_value` | `REAL` | `NOT NULL` | Calibrated floating-point multiplier value |
| `updated_from_override_id` | `TEXT` | | Originating `override_audit_trail.id` audit link |
| `timestamp` | `TEXT` | `NOT NULL` | Adaptation timestamp |

#### 9. `rl_feedback` — Continuous Online Learning Queue
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Monotonic feedback sequence index |
| `override_id` | `TEXT` | `NOT NULL` | Linked clinician override audit identifier |
| `patient_id` | `TEXT` | `NOT NULL` | Patient identifier |
| `bundle_id` | `TEXT` | `NOT NULL` | Bundle identifier |
| `override_reason` | `TEXT` | `NOT NULL` | Structured clinical rationale string |
| `clinical_justification` | `TEXT` | | Extended clinician rationale text |
| `timestamp` | `TEXT` | `NOT NULL` | Feedback submission timestamp |

---

## 📡 Granular REST API Specification

The AegisCDS backend is an asynchronous, high-throughput REST service listening on port `8080`. All JSON responses are UTF-8 encoded and include explicit CORS headers.

### Core Endpoints

#### 1. System Health & Architecture Metadata
- **Route:** `GET /api/status`
- **Description:** Returns operational readiness, active engine components, framework versions, and safety pipeline status.
- **Response `200 OK`:**
  ```json
  {
    "status": "ONLINE",
    "system_name": "AegisCDS Outpatient Alert Fatigue Engine",
    "version": "3.0.0-Enterprise (100% Final Review Complete)",
    "frameworks": ["LangGraph 1.2", "LangChain Core 1.6", "Scikit-Learn Calibrated GBDT", "XGBoost 3.4", "ABDM Indian FHIR R4"],
    "live_event_vetting_pipeline": "ACTIVE (3-Stage Validation: Temporal -> Safety -> ML/RAG)",
    "database_backend": "SQLite Embedded Clinical Store (data/aegis_clinic.db)",
    "openfda_integration": "ACTIVE (Live FDA Drug Label REST Client with Fallback)",
    "hitl_approval_mode": "ACTIVE (Human-in-the-Loop Interlock with Cognitive Telemetry)",
    "active_learning_mode": "ONLINE (Reinforcement from Doctor Overrides)"
  }
  ```

#### 2. Full Patient LangGraph Triage Pipeline
- **Route:** `GET /api/patient/:id/triage`
- **Parameters:** `id` (e.g. `PAT-ROBERTS-001` or `PAT-VANCE-002`)
- **Description:** Intercepts patient observations, executes the 3-stage vetting engine, runs through LangGraph 1.2 state machine, and halts at Node 6 (`HITL Gate`) awaiting clinician review.
- **Response `200 OK`:**
  ```json
  {
    "session_id": "SESS-65b1c9",
    "patient": { "id": "PAT-ROBERTS-001", "name": "Robert Chen", "age": 68 },
    "care_bundles": [
      {
        "id": "BND-01",
        "title": "Annual Preventive Diabetic Care Bundle",
        "priority": "ROUTINE",
        "clinical_rationale": "ADA 2024 Standards of Care: Comprehensive microvascular risk reduction.",
        "evidence_citation": "ADA 2024 Chapter 11 (Microvascular Complications)",
        "suggested_orders": ["Referral to Podiatry", "Dilated Retinal Eye Examination", "Pneumococcal Conjugate Vaccine (PCV20)"],
        "is_critical_bypass": false,
        "status": "AWAITING_HUMAN_APPROVAL"
      }
    ],
    "raw_alerts_count": 7,
    "bundled_alerts_count": 1,
    "noise_reduction_pct": 85.7
  }
  ```

#### 3. Live Clinical Event Ingestion
- **Route:** `POST /api/events/ingest`
- **Request Body:**
  ```json
  {
    "patient_id": "PAT-ROBERTS-001",
    "event_type": "PRESCRIPTION_ORDER",
    "title": "New Prescription: Spironolactone 25mg PO Daily",
    "payload": { "drug": "spironolactone", "dose": "25mg", "indication": "Heart Failure" }
  }
  ```
- **Description:** Ingests live telemetry. Evaluates Stage 1 (Lab recency <= 14d) and Stage 2 (Deterministic physiological invariants) before invoking ML actionability classifier.
- **Response `200 OK`:**
  ```json
  {
    "event_id": "EVT-89412",
    "vetting_stage": "STAGE_1_TEMPORAL_GATE",
    "status": "ACTIONABLE_DATA_GAP_BLOCKED",
    "action_required": "STAT BMP Required Before Dispense",
    "message": "Serum Potassium lab is 45 days old (>14d threshold per KDIGO 2024). Dispensation blocked."
  }
  ```

#### 4. Clinician Human-in-the-Loop Decision Action
- **Route:** `POST /api/graph/hitl-action`
- **Request Body:**
  ```json
  {
    "session_id": "SESS-65b1c9",
    "bundle_id": "BND-01",
    "decision": "APPROVED",
    "clinician_id": "DR-SARATHI-MD",
    "reason": "Clinician signed bundle orders",
    "clinical_justification": "Verified routine preventive screening gaps."
  }
  ```
- **Description:** Unlocks LangGraph Node 6 breakpoint holding state. Emits cryptographic signature, creates immutable `override_audit_trail` record, triggers active online learning adaptation if overridden, and dispatches approved orders to CPOE queue.
- **Response `200 OK`:**
  ```json
  {
    "success": true,
    "resumed_state": {
      "current_step": "CPOE_DISPATCHED",
      "hitl_decision": "APPROVED",
      "dispatched_orders": ["Referral to Podiatry", "Dilated Retinal Eye Examination", "PCV20 Vaccine"]
    },
    "audit_entry": { "id": "AUDIT-48192", "action": "APPROVED", "timestamp": "2026-11-02T11:50:00Z" }
  }
  ```

#### 5. Indian National Digital Health (ABDM) Verification
- **Route:** `GET /api/v1/abdm/consent/:abha_id`
- **Parameters:** `abha_id` (e.g. `91-4829-1029-4820` or `robert.chen@abdm`)
- **Description:** Simulates the Indian National Health Authority (NHA) ABDM Gateway. Verifies patient demographic registry, resolves state/district, and generates cryptographic consent tokens for FHIR M3 health record exchange.
- **Response `200 OK`:**
  ```json
  {
    "status": "VERIFIED",
    "abha_number": "91-4829-1029-4820",
    "abha_address": "robert.chen@abdm",
    "patient_name": "Robert Chen",
    "gender": "M",
    "state": "Tamil Nadu",
    "district": "Kancheepuram",
    "hip_facility": "TN-KANCHI-GH-001",
    "consent_token": "ABDM-CONSENT-8F19B3E12D04"
  }
  ```
- **Error Response `404 Not Found`:**
  ```json
  { "error": "ABHA identifier 'invalid-id' not found in NHA sandbox registry." }
  ```

#### 6. Multi-Department Queue Statistics & Stream
- **Route:** `GET /api/v1/department/stats`
- **Description:** Aggregates recent triage events across role-based queues: Physician, Nursing, Pharmacy, Laboratory.
- **Response `200 OK`:**
  ```json
  { "PHYSICIAN": 4, "NURSING": 3, "PHARMACY": 2, "LABORATORY": 1 }
  ```

#### 7. Active Online Learning Status
- **Route:** `GET /api/v1/rl/status`
- **Description:** Health check of the online reinforcement learning daemon and real-time parameter weights.
- **Response `200 OK`:**
  ```json
  {
    "status": "ONLINE",
    "current_weights": {
      "prior_override_penalty": 2.075,
      "titration_window_penalty": 1.2,
      "chronic_stability_threshold": 0.85,
      "preventive_boost": 2.5,
      "urgency_multiplier": 1.8
    }
  }
  ```

#### 8. Cohort Benchmark Evaluation & CSV Export
- **Route:** `GET /api/benchmark`
- **Description:** Full macro-evaluation across 100 MCC patients, confusion matrix, and clinical KPIs.
- **Route:** `GET /api/benchmark/export-csv`
- **Description:** Streams formatted RFC 4180 CSV attachment containing complete cohort summary, confusion matrix, and KPI comparisons.
- **Response Headers:** `Content-Type: text/csv`, `Content-Disposition: attachment; filename="aegiscds_benchmark_metrics.csv"`

---

## 🛡️ Technical Error Boundaries & Fail-Safe Architecture

AegisCDS implements 6 isolated, deterministic error boundaries designed in accordance with **IEC 62304 / ISO 14971** to ensure clinical safety invariants cannot be breached by downstream software faults or network outages:

| # | Boundary Name | Failure Trigger | Architectural Mitigation & Fallback | Clinical Safety Guarantee |
|---|---|---|---|---|
| **1** | **Network Timeout Boundary** | Live OpenFDA REST API outage (`api.fda.gov` timeout or HTTP 5xx) | Automatic failover to local curated DDI-CDS clinical formulary cache | Drug safety warnings and contraindications are 100% preserved during network drops. |
| **2** | **Temporal Recency Boundary** | Attempt to prescribe RAAS/MRA medications on stale labs (>14 days) | Stage 1 Temporal Gate halts order; auto-drafts STAT BMP order set | Eliminates drug-induced acute kidney injury (AKI) from outdated lab observations. |
| **3** | **Zero-FN Invariant Boundary** | ML model or RAG attempting to suppress severe physiological panic values | Hard safety invariants execute before ML triage; triggers Emergency Banner | **100.0% Critical Sensitivity (Zero False Negatives)** on K⁺ ≥ 6.0, eGFR < 15, SBP ≥ 180. |
| **4** | **HITL Holding Boundary** | Browser tab crash or downstream CPOE formatting exception | LangGraph Node 6 halts execution state in SQLite as `AWAITING_HUMAN_APPROVAL` | Autonomous medication dispatch is strictly prevented; explicit clinician sign-off is mandatory. |
| **5** | **ABDM Privacy Boundary** | Unverified ABHA query or expired consent token | ABDM connector halts health document exchange; returns HTTP 404/403 advisory | Prevents unauthorized disclosure of longitudinal protected health information (PHI). |
| **6** | **Database Concurrency Boundary** | High-volume simultaneous event ingestion burst | SQLite configured with Write-Ahead Logging (WAL) and 30-second busy timeout | Prevents `database is locked` deadlocks; zero dropped events across 1,000 transactions. |

For detailed code flow diagrams and assert-level invariant mappings, see [`docs/testing_and_error_boundaries.md`](docs/testing_and_error_boundaries.md).

---

## 👥 Stakeholder Assumptions

| Stakeholder | Role | Key Assumption |
|---|---|---|
| **Outpatient Physician** | Primary user of the system | Has 10–15 minutes per patient; will engage with ONE consolidated care bundle but not seven pop-ups |
| **Hospital CMO / Medical Director** | System approver | Requires 100% critical alert sensitivity before deployment; zero tolerance for missed life threats |
| **Clinical Pharmacist** | Drug interaction oversight | Alert suppression must be auditable and traceable to a clinical guideline citation |
| **Hospital IT / EHR Team** | Integration | System must expose FHIR-compatible REST APIs for future EHR integration |
| **Healthcare Regulator** | Compliance | Every AI recommendation must pass through a licensed clinician before execution (HITL mandatory) |
| **Patient** | Ultimate beneficiary | Expects their doctor to have adequate time and information to make correct decisions |

---

## 📄 Documentation Index

| Document | Description |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Full multi-tier system architecture with data flow |
| [`docs/testing_and_error_boundaries.md`](docs/testing_and_error_boundaries.md) | Granular technical documentation on unit testing & 6 architectural error boundaries |
| [`docs/fhir_schema.md`](docs/fhir_schema.md) | HL7 FHIR R4 resource definitions and alert schema |
| [`docs/risk_register.md`](docs/risk_register.md) | FMEA clinical risk register (12 failure modes, severity, mitigation) |
| [`docs/user_guide.md`](docs/user_guide.md) | End-user operational guide for clinicians and administrators |
| [`docs/experiment_report.md`](docs/experiment_report.md) | Full N=100 benchmark methodology, results, and error analysis |
| [`docs/review3_submission_report.md`](docs/review3_submission_report.md) | Official 100% Final Review Milestone Submission Report (≤ 8000 chars) |
| [`regulatory/DHF.md`](regulatory/DHF.md) | FDA SaMD Design History File (intended use, V&V, traceability) |
| [`regulatory/risk_analysis.md`](regulatory/risk_analysis.md) | IEC 62304 / ISO 14971 FMEA risk management matrix |
| [`regulatory/SaMD_Label.md`](regulatory/SaMD_Label.md) | IEC 82304-1 healthcare software labeling & directions for use |
| [`regulatory/510k_summary.md`](regulatory/510k_summary.md) | 510(k) substantial equivalence & safety summary |
| [`performance/report_load_test.md`](performance/report_load_test.md) | High-throughput load testing results & SLA compliance |

---

## 🧪 Automated Test Suite

```bash
# Run the complete test suite with verbose output
.venv/bin/pytest -v
```

```
============================== 18 passed in 4.54s (100% pass rate) ==============================
```

| Test File | Tests | Focus Area & Verified Assertions | Status |
|---|---|---|---|
| `test_safety_gate.py` | 3 | Deterministic zero-FN invariant enforcement: K⁺ ≥ 6.0 mEq/L, eGFR < 15, SBP ≥ 180, Sildenafil + Nitroglycerin contraindication. | ✅ PASS |
| `test_failure_modes.py` | 3 | Operational failure simulators: Stale lab rejection (>14d), priority hard-floor isolation (preventing alert masking), LLM hallucination triple RAAS suppression. | ✅ PASS |
| `test_langgraph_resilience.py` | 3 | LangGraph 1.2 cyclic state machine: sequential node execution, atomic HITL breakpoint holding at Node 6, recovery from simulated socket interruption. | ✅ PASS |
| `test_ml_calibration.py` | 2 | CalibratedClassifierCV stress-testing: Brier score < 0.05, ECE < 0.05, PR-AUC > 0.90 under severe 95% and 98% nuisance noise imbalance. | ✅ PASS |
| `test_active_learning_and_abdm.py` | 3 | Online RL weight adjustments from clinician overrides, Indian National Health Authority (NHA) ABHA ID verification & consent tokens, 4-department alert routing. | ✅ PASS |
| `test_benchmark_and_endpoints.py` | 4 | CSV benchmark export validation, ABDM 404 error boundaries, SQLite RL feedback incremental persistence, department queue aggregation. | ✅ PASS |

*For complete technical documentation on all 18 test cases and their execution targets, see [`docs/testing_and_error_boundaries.md`](docs/testing_and_error_boundaries.md).*

---

## 📦 Project Structure

```
ap project/
├── .github/workflows/ci.yml      # GitHub Actions CI/CD pipeline
├── Dockerfile                     # Multi-stage production container
├── docker-compose.yml             # Local development orchestration
├── helm/Chart.yaml                # Kubernetes Helm chart
├── README.md                      # This file
├── conftest.py                    # PyTest configuration
├── data/
│   └── aegis_clinic.db            # SQLite clinical database (9 tables)
├── docs/                          # Architecture, FHIR schema, risk register, user guide
├── performance/
│   └── report_load_test.md        # Load testing benchmark results
├── public/
│   ├── index.html                 # Clinical workstation UI (11 tabs)
│   ├── app.js                     # Front-end application logic
│   └── style.css                  # Glassmorphism dark-mode design system
├── regulatory/
│   ├── DHF.md                     # Design History File
│   ├── risk_analysis.md           # IEC 62304 FMEA risk matrix
│   ├── SaMD_Label.md              # IEC 82304-1 device labeling
│   └── 510k_summary.md            # Substantial equivalence summary
├── scripts/
│   └── load_test.py               # Multi-threaded performance tester
├── src/
│   ├── server.py                  # REST API server (22 endpoints)
│   └── engine/
│       ├── models.py              # FHIR R4 data models & enums
│       ├── synthetic_data.py      # Synthea MCC patient cohort generator
│       ├── data_fetcher.py        # OpenFDA live API + offline cache
│       ├── deterministic_safety_gate.py  # Layer 1: Zero-FN hard rules
│       ├── ml_triage_classifier.py       # Layer 2: Calibrated ML scoring
│       ├── ml_stress_tester.py    # Class-imbalance stress testing
│       ├── guideline_rag.py       # Clinical guideline RAG engine
│       ├── alert_consolidator.py  # Episode-aware care bundler
│       ├── event_vetting_engine.py # 3-stage real-time pipeline
│       ├── langgraph_workflow.py  # LangGraph 1.2 state machine
│       ├── database.py            # SQLite persistence (9 tables)
│       ├── edge_cases.py          # 3 failure mode simulators
│       ├── experiment_evaluator.py # N=100 benchmark + CSV export
│       ├── active_learning_engine.py     # Online RL weight updates
│       ├── active_learning_daemon.py     # Background RL polling daemon
│       ├── abdm_connector.py      # Indian ABDM FHIR bridge
│       ├── department_router.py   # Multi-department alert routing
│       └── api_abdm.py            # ABDM consent API module
└── tests/                         # 18 automated PyTest cases
```

---

## 🛡️ License
MIT License — Built for clinical informatics research and healthcare AI demonstration purposes.

---

*AegisCDS v3.0.0-Enterprise — 100% Final Review Complete*
*Project by: Ayyapparaja VJ | IE28 | Sem 5 | COE Growth Project*
