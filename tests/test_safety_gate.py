"""
Automated PyTest Suite: Safety Gate & Zero-False-Negative Physiological Invariants.
"""

import pytest
from src.engine.deterministic_safety_gate import DeterministicSafetyGate
from src.engine.models import Patient, Observation, MedicationRequest

def test_hyperkalemia_emergency_trigger():
    """Verify that serum potassium >= 6.0 mEq/L triggers an immediate Emergency Bypass."""
    gate = DeterministicSafetyGate()
    patient = Patient(
        id="P-TEST-01",
        mrn="MRN-TEST-01",
        name="Test Patient Hyperkalemia",
        age=70,
        gender="Male",
        conditions=["Heart Failure", "Chronic Kidney Disease"],
        active_medications=[
            MedicationRequest(
                id="MED-SPIRO",
                medication_code="10093",
                medication_name="Spironolactone 25mg",
                category="MRA",
                dose="25mg",
                frequency="Daily",
                started_at="2026-09-01"
            )
        ],
        recent_observations=[
            Observation(
                id="OBS-K",
                code="K+",
                display="Potassium [Moles/volume] in Blood",
                value=6.3,
                unit="mEq/L",
                timestamp="2026-09-21T10:00:00Z",
                reference_range="3.5 - 5.0 mEq/L"
            )
        ]
    )

    alerts = gate.evaluate(patient)
    assert len(alerts) > 0
    emergency_alert = next((a for a in alerts if "Hyperkalemia" in a.title or "Potassium" in a.title), None)
    assert emergency_alert is not None
    assert emergency_alert.raw_priority.value in ["CRITICAL", "HIGH"]
    assert emergency_alert.is_critical_safety_bypass is True

def test_hypertensive_crisis_trigger():
    """Verify that Systolic BP >= 180 mmHg triggers hard safety invariant."""
    gate = DeterministicSafetyGate()
    patient = Patient(
        id="P-TEST-02",
        mrn="MRN-TEST-02",
        name="Test Patient BP Crisis",
        age=65,
        gender="Female",
        conditions=["Essential Hypertension"],
        active_medications=[],
        recent_observations=[
            Observation(
                id="OBS-BP",
                code="BP_Systolic",
                display="Systolic blood pressure",
                value=195.0,
                unit="mmHg",
                timestamp="2026-09-21T10:00:00Z",
                reference_range="< 130 mmHg"
            )
        ]
    )

    alerts = gate.evaluate(patient)
    bp_alert = next((a for a in alerts if any(kw in a.title.lower() for kw in ["hypertensive", "blood pressure", "hypertension"])), None)
    assert bp_alert is not None
    assert bp_alert.raw_priority.value in ["CRITICAL", "HIGH"]

def test_normal_patient_no_false_emergency():
    """Verify that a stable patient with normal labs does not trigger false emergency bypass."""
    gate = DeterministicSafetyGate()
    patient = Patient(
        id="P-TEST-03",
        mrn="MRN-TEST-03",
        name="Stable Patient",
        age=60,
        gender="Male",
        conditions=["Type 2 Diabetes"],
        active_medications=[],
        recent_observations=[
            Observation(
                id="OBS-K",
                code="K+",
                display="Potassium",
                value=4.4,
                unit="mEq/L",
                timestamp="2026-09-21T10:00:00Z",
                reference_range="3.5 - 5.0 mEq/L"
            ),
            Observation(
                id="OBS-BP",
                code="BP_Systolic",
                display="Systolic BP",
                value=124.0,
                unit="mmHg",
                timestamp="2026-09-21T10:00:00Z",
                reference_range="< 130 mmHg"
            )
        ]
    )

    alerts = gate.evaluate(patient)
    critical_alerts = [a for a in alerts if a.raw_priority.value == "CRITICAL"]
    assert len(critical_alerts) == 0
