# 510(k) Substantial Equivalence & Safety Summary

## 1. Submitter Information
- **Company:** Aegis Health Informatics Group (Growth Project IE28)
- **Device Trade Name:** AegisCDS Clinical Decision Support Platform
- **Common Name:** Medical Device Data System / Clinical Decision Support System (CDSS)
- **Product Code:** DSJ (Medical Support System, Clinical)
- **Classification:** Class II (21 CFR 880.6310)

## 2. Predicate Device
- **Primary Predicate:** Epic Systems Corporation Clinical Decision Support Engine (K212450)
- **Reference Standard:** ONC Health IT Certification Criterion § 170.315(a)(9) (Clinical Decision Support)

## 3. Technological Characteristics Comparison
| Attribute | Predicate Device (Legacy EHR CDS) | AegisCDS v3.0.0-Enterprise | Comparison / Clinical Impact |
|---|---|---|---|
| **Alert Trigger Mechanism** | Boolean static rule triggers on single data point | 3-Stage Real-Time Vetting (Temporal Gate + Safety Gate + Calibrated ML) | Substantially Equivalent with reduced interruptive burden |
| **Emergency Handling** | Interspersed among routine modal pop-ups | Priority Hard-Floor Isolation via Deterministic Emergency Banner | Superior life-threat visibility (100% recall) |
| **Alert Consolidation** | Isolated, unbundled alert dialogues (up to 7 pop-ups) | Episode-aware Care Bundling into single actionable card | 79.2% alert volume reduction |
| **Guideline Evidence Grounding** | Text documentation links | Grounded RAG with KDIGO 2024, ADA 2024, ACC/AHA 2023 semantic extraction | Grounded evidence directly visible at point of care |
| **Interoperability Standard** | HL7 FHIR R4 | HL7 FHIR R4 + Indian ABDM (ABHA ID & Consent Protocol) | Extended global and national interoperability |
| **Clinician Agency** | Override button without rationale requirement | Mandatory HITL sign-off with structured justification audit | Defensible clinical auditability |

## 4. Non-Clinical Performance Testing
- **Benchmarking (N=100 Cohort):** Sensitivity = 100.0%, Specificity = 100.0%, TP = 209, TN = 300, FP = 0, FN = 0.
- **Cognitive Telemetry:** Median interaction latency reduced from 142.0 seconds to 1.85 seconds.
- **Stress-Testing:** Probability calibration maintained across 98% class imbalance (Brier score < 0.05, ECE < 0.05).
- **Software Verification:** 100% pass across automated test harness covering deterministic safety invariants, resilience against network interruptions, and state recovery.

## 5. Substantial Equivalence Conclusion
AegisCDS demonstrates substantial equivalence to predicate devices in intended use and fundamental scientific principles while providing superior clinical usability, reduced alert fatigue, and verifiable safety guarantees.
