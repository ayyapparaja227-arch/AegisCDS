# AegisCDS Clinician & Administrator User Guide

---

## 1. Introduction & Clinical Purpose
AegisCDS is designed to alleviate cognitive overload in outpatient clinics managing patients with Multiple Chronic Conditions (MCC). Instead of bombarding you with 7 to 10 disjointed modal pop-ups during every consultation, AegisCDS filters non-actionable nuisance alerts and presents unified, evidence-grounded **Care Bundles** with pre-configured orders ready for a single-click signature.

---

## 2. Navigating the Workstation

### 2.1 Top Global Header
- **Active MCC Encounter Switcher:** Toggle between patient journeys:
  - **Robert Chen (68M):** Complex stable MCC (T2D, HTN, Dyslipidemia) exhibiting high baseline alert noise.
  - **Eleanor Vance (74F):** Acute Crashing MCC (HFrEF, CKD 3b) exhibiting critical hyperkalemia ($K^+ = 6.2\text{ mEq/L}$) and AKI.
- **System Telemetry Indicators:** Real-time operational status of the LangGraph agent, Layer 1 Deterministic Gate, and Human-in-the-Loop interlock.
- **Theme Toggle (🌙 / ☀️):** Switch between Dark and Medical Light modes based on clinic lighting preferences.

### 2.2 Patient Context Banner
Displays real-time demographics, active ICD-10 conditions, and recent laboratory telemetry (Potassium, Creatinine, eGFR, Blood Pressure). Values exceeding critical safety thresholds pulse in red.

---

## 3. Core Clinical Workflows

### 3.1 Live Triage & Comparator View
- **Left Column (Legacy EHR Baseline):** Displays the raw Best Practice Advisories (BPAs) that legacy EHRs generate for the patient. Notice the repetitive warnings, duplicate lab notifications, and generic precautions.
- **Right Column (AegisCDS Care Bundles):**
  - **Emergency Hero Banner (Red):** Displayed immediately if a life-critical physiological condition exists (e.g. Eleanor Vance). Provides the KDIGO guideline rationale and emergency orders (`Stat ECG`, `Hold Spironolactone/Lisinopril`, `Lokelma 10g TID`).
  - **Consolidated Care Bundles (Green/Blue):** Bundles related routine and preventive care into a cohesive action set (e.g., foot exam referral + microalbuminuria lab + PCV20 vaccine for Robert Chen).
  - **Suppressed Nuisance Drawer:** Click *"View Suppressed Nuisance Alerts"* to inspect alerts that were safely silenced, along with their clinical justification (e.g. *"Duplicate test within 90-day stability window"*).

### 3.2 Human-in-the-Loop (HITL) Review Gate
All proposed care bundles require physician review before entering the hospital order queue:
1. Navigate to the **LangGraph & HITL Workflow** tab.
2. Review the pre-drafted orders in the checklist.
3. **To Accept:** Click **"✓ Sign & Dispatch Bundle to EHR CPOE"**. All orders are immediately dispatched to the hospital order queue.
4. **To Override:** Click **"⚠️ Clinical Override"**. Select a structured clinical reason:
   - `[Specialist Already Managing]`
   - `[Patient Aware & Home Monitoring Arranged]`
   - `[Benefit Outweighs Risk - Documented]`
   - `[Recent External Lab Confirmed Stable]`
   - `[Titration In Progress - Steady State Awaited]`
5. Add an optional encounter note and click **"Submit Structured Override"**.

### 3.3 Failure Mode & Edge Case Lab
Interactive tool for clinical governance and informatics committees:
- **Test Case 1:** Simulates 45-day-old stale laboratory data and demonstrates the **Recency Data-Gap Guardrail**.
- **Test Case 2:** Simulates aggressive clustering and demonstrates how **Priority Hard-Floor Isolation** prevents acute potassium from being hidden in routine checkup bundles.
- **Test Case 3:** Simulates generative AI hallucination and demonstrates the **Grounded RAG Verification & Fallback Circuit Breaker**.

### 3.4 Benchmark Studio & Audit Trail
- **Benchmark Studio:** Real-time metrics across the 100-patient outpatient cohort, showing alert reduction percentage, 100% critical sensitivity, and the empirical confusion matrix.
- **Clinician Audit Trail:** Chronological, immutable log of all physician actions, overrides, and timestamps for clinical risk management and quality improvement reviews.
