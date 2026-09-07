# Clinical Risk Register & Failure Mode and Effects Analysis (FMEA)

---

## 1. Clinical Risk Governance Overview
Deploying automated clinical decision support (CDS) in outpatient clinics treating high-acuity Multiple Chronic Conditions (MCC) presents severe clinical, pharmacological, and medico-legal risks. This document articulates the **Failure Mode and Effects Analysis (FMEA)**, evaluating potential failure hazards, root causes, clinical severity, and automated software safeguards.

---

## 2. Quantitative Risk Matrix

| Risk ID | Hazard / Operational Failure Mode | Clinical Severity (1–5) | Likelihood (1–5) | Pre-Mitigation RPN | Root Cause | Automated Software Safeguard | Post-Mitigation RPN | Status |
|---|---|---|---|---|---|---|---|---|
| **RSK-01** | **False Negative Suppression of Critical Electrolyte Crisis** | **5 (Catastrophic)** | 2 (Low) | **10** | ML classifier misinterprets an acute potassium spike as routine due to stable baseline labs. | **Layer 1 Deterministic Gate:** Hard-coded physiological boundaries ($K^+ \ge 6.0$, eGFR $< 15$) bypass ML models unconditionally. | **2 (Controlled)** | **MITIGATED** |
| **RSK-02** | **Telemetry Latency & Stale Data Trap** | **4 (Critical)** | 4 (Frequent) | **16** | Outpatient clinic record lacks external urgent care lab drawn 6 hours earlier, evaluating against 45-day-old normal baseline. | **Recency Data-Gap Guardrail:** Mandatory block on high-risk drug initiation if renal telemetry is $>14$ days stale; generates actionable *Data Gap Order*. | **4 (Controlled)** | **MITIGATED** |
| **RSK-03** | **Over-Consolidation & Semantic Masking** | **4 (Critical)** | 3 (Moderate) | **12** | Clustering algorithm absorbs an acute rising lab trend into a routine preventive care bundle title. | **Priority Hard-Floor Isolation:** High/Critical alerts are strictly barred from merging into routine maintenance bundles. | **3 (Controlled)** | **MITIGATED** |
| **RSK-04** | **Generative AI / SLM Hallucination or Formulary Drift** | **4 (Critical)** | 2 (Low) | **8** | LLM suggests non-guideline dosing or contraindicated triple-blockade. | **Grounded RAG Verification & Deterministic Fallback:** Output constrained to certified KDIGO/ADA vectors; non-matching outputs rejected. | **2 (Controlled)** | **MITIGATED** |
| **RSK-05** | **Autonomous Order Dispatch without Physician Consent** | **5 (Catastrophic)** | 1 (Rare) | **5** | System automatically executes medication holds or orders without human sign-off. | **LangGraph HITL Checkpoint Interlock:** State machine halts execution until explicit physician signature or override is captured. | **1 (Controlled)** | **MITIGATED** |
| **RSK-06** | **Unstructured Blanket Override Muscle Memory** | **3 (Moderate)** | 5 (Very High)| **15** | Clinicians reflexively dismiss alerts without reading rationale. | **1-Click Structured Override Capture:** Replaces generic dismissals with defensible clinical rationale tags for audit tracking. | **3 (Controlled)** | **MITIGATED** |

---

## 3. Deep Dive on Primary Failure Modes

### 3.1 Failure Mode 1: The Stale Data Trap (Telemetry Latency)
- **Clinical Scenario:** Harold Jenkins (71M, HFrEF) is prescribed Spironolactone 25mg daily. The outpatient EHR record displays a normal Serum Potassium ($K^+ = 4.5\text{ mEq/L}$) from 45 days ago. Unknown to the clinic, the patient took an over-the-counter NSAID for knee pain 3 days ago, and his current potassium is spiking.
- **How Naive Systems Fail:** A standard machine learning model looks at the available lab ($4.5\text{ mEq/L}$) and suppresses safety warnings, asserting "patient is stable."
- **AegisCDS Defense:** The **Recency Data-Gap Gate** inspects the timestamp of renal observations. If a high-risk medication is initiated without a BMP within $\le 14$ days, the engine refuses to down-triage and triggers an actionable **Data Gap Alert**: *"Recent Renal Function Unavailable; Mandatory Lab Check Required Before Dispense"*.

### 3.2 Failure Mode 2: Over-Consolidation & Cognitive Masking
- **Clinical Scenario:** A patient with Type 2 Diabetes has a rising potassium of $5.7\text{ mEq/L}$ (mild hyperkalemia) alongside overdue diabetic foot, retinal, and microalbuminuria screenings.
- **How Naive Systems Fail:** A semantic clustering algorithm groups all 4 alerts into a single bundle labeled *"Routine Outpatient Diabetic Review"*. The busy clinician glances at the routine title, assumes it's all non-urgent preventive screening, and signs the bundle without noticing the emerging potassium trajectory.
- **AegisCDS Defense:** The engine enforces a **Priority Hard-Floor Invariant**. Any alert with priority $\ge$ HIGH or acute physiological delta is separated into an isolated hero banner and cannot be absorbed into routine maintenance bundles.

### 3.3 Failure Mode 3: Generative LLM Hallucination & Clinical Drift
- **Clinical Scenario:** An outpatient physician asks an AI assistant to suggest BP intensification for a diabetic patient already on Lisinopril and Losartan.
- **How Naive Systems Fail:** An ungrounded LLM produces plausible text suggesting the addition of Aliskiren (direct renin inhibitor), producing lethal triple-RAAS blockade.
- **AegisCDS Defense:** AegisCDS incorporates **Dual-Layer RAG Verification**:
  1. The LLM suggestion is checked against the deterministic contraindication table.
  2. The suggestion must match verified guideline vectors (ACC/AHA 2023, KDIGO 2024) with cosine similarity $\ge 0.88$.
  3. If a contraindication keyword or discrepancy is found, the generative text is instantly dropped, and the certified deterministic order set is rendered.
