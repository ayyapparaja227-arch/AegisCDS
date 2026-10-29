# IEC 82304-1 Healthcare Software Labeling & Directions for Use

## 1. Device Identification
- **Proprietary Name:** AegisCDS (Clinical Decision Support Platform)
- **Version:** v3.0.0-Enterprise (100% Release Candidate)
- **Manufacturer:** Aegis Health Systems Informatics / COE Growth Project
- **Target Platform:** Python 3.11+ / Docker Container / HL7 FHIR R4 Compliant EHR Systems
- **Regulatory Classification:** FDA Class II SaMD (Clinical Decision Support Software under 21 CFR 880.6310) / IEC 62304 Class B

## 2. Intended Use Statement
AegisCDS is intended for use by qualified healthcare practitioners (physicians, nurse practitioners, clinical pharmacists) in outpatient clinical environments managing adult patients with multiple chronic conditions (Type 2 Diabetes Mellitus, Essential Hypertension, Chronic Kidney Disease, Heart Failure). The system analyzes real-time electronic health record (EHR) laboratory results, vital signs, and medication lists to:
1. Detect physiological safety emergencies and present immediate non-silenceable emergency banners.
2. Filter nuisance drug-drug interaction warnings and duplicate reminders.
3. Synthesize evidence-grounded care bundles with pre-drafted order sets aligned with international clinical practice guidelines (KDIGO 2024, ADA 2024, ACC/AHA 2023).

## 3. Contraindications & Limitations
- **Not for Neonatal/Pediatric Use:** Algorithms and guideline RAG parameters are calibrated exclusively for adult patients (age >= 18).
- **Not Autonomous:** AegisCDS is NOT an autonomous order-entry system. All proposed care bundles, drug holds, and diagnostic tests require clinician verification and approval.
- **Offline Cache Advisory:** In the event of network disruption to the live OpenFDA API, the system falls back to the local cached formulary. Clinicians are notified via UI indicator.
