"""
Synthetic FHIR R4 Patient and Clinical Alert Stream Generator.
Generates:
1. Patient Journey 1: Robert Chen (68M) - Stable MCC Routine Maintenance (Noise Elimination)
2. Patient Journey 2: Eleanor Vance (74F) - Acute Crashing MCC (Critical Preservation)
3. 100+ Realistic MCC Outpatient Encounters for benchmark experiments and confusion matrix analysis.
"""

from typing import List, Dict, Any, Tuple
import random
import uuid
import time
from .models import Patient, Observation, MedicationRequest, ClinicalAlert, AlertPriority, AlertCategory, AlertStatus

def get_patient_robert_chen() -> Tuple[Patient, List[ClinicalAlert]]:
    """Patient Journey 1: Robert Chen (68M) - Complex stable MCC, severe alert noise."""
    patient = Patient(
        id="PAT-ROBERTS-001",
        mrn="MRN-884920",
        name="Robert Chen",
        age=68,
        gender="Male",
        conditions=[
            "Type 2 Diabetes Mellitus (E11.9)",
            "Essential Hypertension (I10)",
            "Hyperlipidemia (E78.5)",
            "Mild Osteoarthritis (M19.9)"
        ],
        active_medications=[
            MedicationRequest(id="MED-1", medication_code="6809", medication_name="Metformin 1000mg oral tablet", category="BIGUANIDE", dose="1000mg", frequency="BID", started_at="2022-01-15"),
            MedicationRequest(id="MED-2", medication_code="29046", medication_name="Lisinopril 20mg oral tablet", category="ACE_INHIBITOR", dose="20mg", frequency="Daily", started_at="2023-04-10"),
            MedicationRequest(id="MED-3", medication_code="83367", medication_name="Atorvastatin 40mg oral tablet", category="STATIN", dose="40mg", frequency="Nightly", started_at="2021-11-20"),
            MedicationRequest(id="MED-4", medication_code="161", medication_name="Acetaminophen 500mg oral tablet", category="ANALGESIC", dose="500mg", frequency="PRN", started_at="2024-02-01")
        ],
        recent_observations=[
            Observation(id="OBS-1", code="HbA1c", display="Glycated Hemoglobin (HbA1c)", value=6.9, unit="%", timestamp="2026-06-10T09:00:00Z", reference_range="4.0 - 5.6 %"),
            Observation(id="OBS-2", code="K+", display="Serum Potassium", value=4.6, unit="mEq/L", timestamp="2026-09-01T08:30:00Z", reference_range="3.5 - 5.0 mEq/L"),
            Observation(id="OBS-3", code="Creatinine", display="Serum Creatinine", value=1.05, unit="mg/dL", timestamp="2026-09-01T08:30:00Z", reference_range="0.7 - 1.3 mg/dL"),
            Observation(id="OBS-4", code="eGFR", display="eGFR CKD-EPI", value=78.0, unit="mL/min/1.73m2", timestamp="2026-09-01T08:30:00Z", reference_range="> 60 mL/min/1.73m2"),
            Observation(id="OBS-5", code="BP_Systolic", display="Systolic Blood Pressure", value=136.0, unit="mmHg", timestamp="2026-09-04T08:45:00Z", reference_range="< 130 mmHg"),
            Observation(id="OBS-6", code="BP_Diastolic", display="Diastolic Blood Pressure", value=84.0, unit="mmHg", timestamp="2026-09-04T08:45:00Z", reference_range="< 80 mmHg")
        ],
        encounter_type="Outpatient 6-Month Chronic Disease Follow-up"
    )

    alerts = [
        ClinicalAlert(
            id="ALT-RC-01",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.LOW,
            title="Duplicate Lab Order: HbA1c",
            description="HbA1c already drawn 85 days ago (Result: 6.9%). Retesting within 90 days has low yield under stable control.",
            trigger_rule="BPA_DUP_LAB_HBA1C",
            timestamp="2026-09-04T09:01:00Z"
        ),
        ClinicalAlert(
            id="ALT-RC-02",
            patient_id=patient.id,
            category=AlertCategory.DRUG_INTERACTION,
            raw_priority=AlertPriority.LOW,
            title="Drug Precaution: Atorvastatin + Metformin",
            description="Potential risk of increased muscle weakness or metabolic alteration. Monitor patient closely.",
            trigger_rule="BPA_DRUG_INT_STATIN_MET",
            timestamp="2026-09-04T09:01:02Z"
        ),
        ClinicalAlert(
            id="ALT-RC-03",
            patient_id=patient.id,
            category=AlertCategory.LAB_ABNORMALITY,
            raw_priority=AlertPriority.MEDIUM,
            title="Elevated Blood Pressure: 136/84 mmHg",
            description="In-office blood pressure 136/84 mmHg exceeds ADA/ACC guideline threshold (<130/80 mmHg). Consider intensification.",
            trigger_rule="BPA_VITALS_BP_ABOVE_TARGET",
            timestamp="2026-09-04T09:01:05Z"
        ),
        ClinicalAlert(
            id="ALT-RC-04",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.MEDIUM,
            title="Diabetic Foot Exam Overdue",
            description="Comprehensive visual and monofilament foot sensory evaluation not documented in past 12 months.",
            trigger_rule="BPA_PREV_FOOT_EXAM_DUE",
            timestamp="2026-09-04T09:01:08Z"
        ),
        ClinicalAlert(
            id="ALT-RC-05",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.MEDIUM,
            title="Diabetic Nephropathy: Microalbuminuria Screening Due",
            description="Annual urine albumin-to-creatinine ratio (uACR) screening is due per ADA Standards of Care.",
            trigger_rule="BPA_PREV_UACR_DUE",
            timestamp="2026-09-04T09:01:10Z"
        ),
        ClinicalAlert(
            id="ALT-RC-06",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.LOW,
            title="Immunization Reminder: Pneumococcal Conjugate (PCV20)",
            description="Patient aged >= 65 with diabetes qualifies for PCV20 vaccination reminder.",
            trigger_rule="BPA_IMMUN_PCV20",
            timestamp="2026-09-04T09:01:12Z"
        ),
        ClinicalAlert(
            id="ALT-RC-07",
            patient_id=patient.id,
            category=AlertCategory.DOSING_GUIDELINE,
            raw_priority=AlertPriority.LOW,
            title="Prescription Refill Reminder: Lisinopril 20mg",
            description="Last filled 28 days ago. 2 refills remaining on active pharmacy profile.",
            trigger_rule="BPA_REFILL_PROMPT",
            timestamp="2026-09-04T09:01:15Z"
        )
    ]
    return patient, alerts

def get_patient_eleanor_vance() -> Tuple[Patient, List[ClinicalAlert]]:
    """Patient Journey 2: Eleanor Vance (74F) - Acute Crashing MCC with life-threatening hyperkalemia."""
    patient = Patient(
        id="PAT-ELEANOR-002",
        mrn="MRN-442190",
        name="Eleanor Vance",
        age=74,
        gender="Female",
        conditions=[
            "Heart Failure with Reduced Ejection Fraction (I50.22, NYHA Class III, EF 32%)",
            "Chronic Kidney Disease Stage 3b (N18.32)",
            "Essential Hypertension (I10)",
            "Coronary Artery Disease post-CABG (I25.10)"
        ],
        active_medications=[
            MedicationRequest(id="MED-EV-1", medication_code="29046", medication_name="Lisinopril 20mg oral tablet", category="ACE_INHIBITOR", dose="20mg", frequency="Daily", started_at="2023-01-10"),
            MedicationRequest(id="MED-EV-2", medication_code="9997", medication_name="Spironolactone 25mg oral tablet", category="MRA", dose="25mg", frequency="Daily", started_at="2026-08-30"), # Started 5 days ago!
            MedicationRequest(id="MED-EV-3", medication_code="4603", medication_name="Furosemide 40mg oral tablet", category="LOOP_DIURETIC", dose="40mg", frequency="Daily", started_at="2022-09-12"),
            MedicationRequest(id="MED-EV-4", medication_code="20352", medication_name="Carvedilol 12.5mg oral tablet", category="BETA_BLOCKER", dose="12.5mg", frequency="BID", started_at="2023-02-18")
        ],
        recent_observations=[
            Observation(id="OBS-EV-1", code="K+", display="Serum Potassium", value=6.2, unit="mEq/L", timestamp="2026-09-04T08:00:00Z", reference_range="3.5 - 5.0 mEq/L"), # CRITICAL! Rose from 4.8
            Observation(id="OBS-EV-2", code="Creatinine", display="Serum Creatinine", value=2.4, unit="mg/dL", timestamp="2026-09-04T08:00:00Z", reference_range="0.5 - 1.1 mg/dL"), # AKI! Rose from 1.6
            Observation(id="OBS-EV-3", code="eGFR", display="eGFR CKD-EPI", value=21.0, unit="mL/min/1.73m2", timestamp="2026-09-04T08:00:00Z", reference_range="> 60 mL/min/1.73m2"),
            Observation(id="OBS-EV-4", code="BP_Systolic", display="Systolic Blood Pressure", value=112.0, unit="mmHg", timestamp="2026-09-04T08:30:00Z", reference_range="< 130 mmHg"),
            Observation(id="OBS-EV-5", code="BP_Diastolic", display="Diastolic Blood Pressure", value=68.0, unit="mmHg", timestamp="2026-09-04T08:30:00Z", reference_range="< 80 mmHg")
        ],
        encounter_type="Outpatient Urgent Post-Medication Titration Visit"
    )

    alerts = [
        ClinicalAlert(
            id="ALT-EV-01",
            patient_id=patient.id,
            category=AlertCategory.LAB_ABNORMALITY,
            raw_priority=AlertPriority.CRITICAL,
            title="CRITICAL LAB: Serum Potassium 6.2 mEq/L",
            description="Serum potassium is 6.2 mEq/L (Critical High >= 6.0 mEq/L). Immediate risk of lethal ventricular arrhythmia and cardiac arrest.",
            trigger_rule="BPA_CRIT_LAB_HYPERKALEMIA",
            timestamp="2026-09-04T08:15:00Z"
        ),
        ClinicalAlert(
            id="ALT-EV-02",
            patient_id=patient.id,
            category=AlertCategory.LAB_ABNORMALITY,
            raw_priority=AlertPriority.HIGH,
            title="Acute Kidney Injury Alert: Creatinine 2.4 mg/dL",
            description="Serum Creatinine increased 50.0% from 1.6 mg/dL to 2.4 mg/dL over 5 days since Spironolactone initiation.",
            trigger_rule="BPA_LAB_AKI_CREATININE_SPIKE",
            timestamp="2026-09-04T08:15:02Z"
        ),
        ClinicalAlert(
            id="ALT-EV-03",
            patient_id=patient.id,
            category=AlertCategory.DRUG_INTERACTION,
            raw_priority=AlertPriority.HIGH,
            title="Severe Interaction: Dual Renin-Angiotensin Aldosterone Blockade",
            description="Concomitant Lisinopril (ACE-i) + Spironolactone (MRA) significantly elevates hyperkalemia and renal failure risk in CKD 3b.",
            trigger_rule="BPA_DRUG_INT_RAAS_MRA",
            timestamp="2026-09-04T08:15:05Z"
        ),
        ClinicalAlert(
            id="ALT-EV-04",
            patient_id=patient.id,
            category=AlertCategory.DRUG_INTERACTION,
            raw_priority=AlertPriority.LOW,
            title="Drug Interaction: Furosemide + Lisinopril",
            description="Concurrent administration may increase risk of first-dose postural hypotension. Monitor blood pressure.",
            trigger_rule="BPA_DRUG_INT_DIURETIC_ACE",
            timestamp="2026-09-04T08:15:08Z"
        ),
        ClinicalAlert(
            id="ALT-EV-05",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.LOW,
            title="Outpatient Daily Weight Log Reminder",
            description="Recommend daily morning weight monitoring for Heart Failure fluid retention.",
            trigger_rule="BPA_HF_WEIGHT_REMINDER",
            timestamp="2026-09-04T08:15:10Z"
        ),
        ClinicalAlert(
            id="ALT-EV-06",
            patient_id=patient.id,
            category=AlertCategory.DOSING_GUIDELINE,
            raw_priority=AlertPriority.LOW,
            title="Dietary Sodium Restriction Advisory",
            description="Reinforce 2000mg/day sodium restriction education for Stage C Heart Failure.",
            trigger_rule="BPA_HF_SODIUM_ED",
            timestamp="2026-09-04T08:15:12Z"
        )
    ]
    return patient, alerts

def generate_benchmark_cohort(n_patients: int = 100) -> List[Tuple[Patient, List[ClinicalAlert]]]:
    """Generates a reproducible 100-patient outpatient cohort with MCC for macro benchmark experiments."""
    random.seed(1337)
    cohort = []

    # Inject the two canonical journeys
    cohort.append(get_patient_robert_chen())
    cohort.append(get_patient_eleanor_vance())

    condition_pool = [
        "Type 2 Diabetes Mellitus", "Essential Hypertension", "CKD Stage 3a", "CKD Stage 3b",
        "HFrEF", "HFpEF", "Hyperlipidemia", "Atrial Fibrillation", "COPD", "Coronary Artery Disease"
    ]

    for i in range(3, n_patients + 1):
        age = random.randint(52, 86)
        gender = random.choice(["Male", "Female"])
        n_conds = random.randint(2, 5)
        conds = random.sample(condition_pool, n_conds)

        # Baseline labs
        is_critical_case = (random.random() < 0.08) # 8% critical hyperkalemia / severe crisis cases
        k_val = round(random.uniform(6.1, 6.7), 1) if is_critical_case else round(random.uniform(3.7, 5.2), 1)
        cr_val = round(random.uniform(2.2, 3.8), 2) if is_critical_case else round(random.uniform(0.8, 1.5), 2)
        egfr_val = 18.0 if is_critical_case else round(random.uniform(45.0, 90.0), 1)
        sbp_val = round(random.uniform(118.0, 142.0), 0)

        patient = Patient(
            id=f"PAT-BENCH-{i:03d}",
            mrn=f"MRN-{random.randint(100000, 999999)}",
            name=f"Patient {i:03d}",
            age=age,
            gender=gender,
            conditions=conds,
            active_medications=[
                MedicationRequest(id=f"MED-{i}-1", medication_code="29046", medication_name="Lisinopril 20mg", category="ACE_INHIBITOR", dose="20mg", frequency="Daily", started_at="2023-01-01"),
                MedicationRequest(id=f"MED-{i}-2", medication_code="6809", medication_name="Metformin 1000mg", category="BIGUANIDE", dose="1000mg", frequency="BID", started_at="2022-05-01"),
                MedicationRequest(id=f"MED-{i}-3", medication_code="83367", medication_name="Atorvastatin 20mg", category="STATIN", dose="20mg", frequency="Daily", started_at="2021-08-01")
            ],
            recent_observations=[
                Observation(id=f"OBS-{i}-1", code="K+", display="Serum Potassium", value=k_val, unit="mEq/L", timestamp="2026-09-04T08:00:00Z", reference_range="3.5 - 5.0 mEq/L"),
                Observation(id=f"OBS-{i}-2", code="Creatinine", display="Serum Creatinine", value=cr_val, unit="mg/dL", timestamp="2026-09-04T08:00:00Z", reference_range="0.7 - 1.3 mg/dL"),
                Observation(id=f"OBS-{i}-3", code="eGFR", display="eGFR", value=egfr_val, unit="mL/min/1.73m2", timestamp="2026-09-04T08:00:00Z", reference_range="> 60 mL/min"),
                Observation(id=f"OBS-{i}-4", code="BP_Systolic", display="Systolic BP", value=sbp_val, unit="mmHg", timestamp="2026-09-04T08:00:00Z", reference_range="< 130 mmHg")
            ]
        )

        # Generate realistic alert barrage (4 to 8 alerts per encounter in baseline)
        alerts = []
        if is_critical_case:
            alerts.append(ClinicalAlert(
                id=f"ALT-B-{i}-CRIT",
                patient_id=patient.id,
                category=AlertCategory.LAB_ABNORMALITY,
                raw_priority=AlertPriority.CRITICAL,
                title=f"CRITICAL LAB: Serum Potassium {k_val} mEq/L",
                description=f"Severe hyperkalemia ({k_val} mEq/L) on ACE-inhibitor.",
                trigger_rule="BPA_CRIT_LAB_HYPERKALEMIA",
                timestamp="2026-09-04T08:00:00Z"
            ))

        # Add duplicate lab nuisance
        alerts.append(ClinicalAlert(
            id=f"ALT-B-{i}-DUP",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.LOW,
            title="Duplicate Lab Order: HbA1c",
            description="HbA1c already done 82 days ago. Redundant testing warning.",
            trigger_rule="BPA_DUP_LAB_HBA1C",
            timestamp="2026-09-04T08:01:00Z"
        ))

        # Add generic drug-drug nuisance
        alerts.append(ClinicalAlert(
            id=f"ALT-B-{i}-DRUG",
            patient_id=patient.id,
            category=AlertCategory.DRUG_INTERACTION,
            raw_priority=AlertPriority.LOW,
            title="Generic Precaution: Statin + Metformin",
            description="Routine precaution warning. Historical override rate 96%.",
            trigger_rule="BPA_DRUG_INT_STATIN_MET",
            timestamp="2026-09-04T08:01:02Z"
        ))

        # Add screening alerts
        alerts.append(ClinicalAlert(
            id=f"ALT-B-{i}-PREV1",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.MEDIUM,
            title="Diabetic Eye Dilated Exam Due",
            description="Annual retinal screening due per ADA guideline.",
            trigger_rule="BPA_PREV_RETINAL",
            timestamp="2026-09-04T08:01:04Z"
        ))

        alerts.append(ClinicalAlert(
            id=f"ALT-B-{i}-PREV2",
            patient_id=patient.id,
            category=AlertCategory.MONITORING_DUE,
            raw_priority=AlertPriority.MEDIUM,
            title="Microalbuminuria Screening Due",
            description="Annual urine albumin-to-creatinine ratio screening due.",
            trigger_rule="BPA_PREV_UACR",
            timestamp="2026-09-04T08:01:06Z"
        ))

        alerts.append(ClinicalAlert(
            id=f"ALT-B-{i}-REFILL",
            patient_id=patient.id,
            category=AlertCategory.DOSING_GUIDELINE,
            raw_priority=AlertPriority.LOW,
            title="Maintenance Refill Prompt",
            description="30-day refill available on active profile.",
            trigger_rule="BPA_REFILL_PROMPT",
            timestamp="2026-09-04T08:01:08Z"
        ))

        cohort.append((patient, alerts))

    return cohort
