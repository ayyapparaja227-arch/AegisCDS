"""
Automated PyTest Suite: Active Online Learning & ABDM Connector.
"""

import pytest
from src.engine.active_learning_engine import ActiveOnlineLearningEngine
from src.engine.abdm_connector import ABDMConnector
from src.engine.department_router import DepartmentRouter
from src.engine.models import ClinicalAlert, AlertPriority, AlertCategory

def test_active_online_learning_update():
    """Verify that doctor override updates feature importance penalty online."""
    engine = ActiveOnlineLearningEngine()
    initial_w = engine.current_weights["prior_override_penalty"]

    res = engine.process_clinician_feedback(
        override_id="OVR-TEST-01",
        patient_id="P-01",
        bundle_id="BND-01",
        override_reason="Patient stable on chronic statin-metformin for 3 years.",
        clinical_justification="No signs of myopathy or liver enzyme elevation."
    )

    assert res["status"] == "ONLINE_WEIGHTS_UPDATED"
    assert res["current_weights"]["prior_override_penalty"] > initial_w

def test_abdm_abha_verification():
    """Verify Indian ABHA ID validation and consent token generation."""
    abdm = ABDMConnector()
    res = abdm.verify_abha_id("91-4829-1029-4820")
    assert res["status"] == "VERIFIED"
    assert res["patient_name"] == "Robert Chen"
    assert "Tamil Nadu" in res["state"]
    assert res["consent_token"].startswith("ABDM-CONSENT")

def test_department_router():
    """Verify routing of nursing vs physician alerts."""
    router = DepartmentRouter()
    nursing_alert = ClinicalAlert(
        id="ALT-NURSE",
        patient_id="P-01",
        category=AlertCategory.PREVENTIVE_CARE if hasattr(AlertCategory, "PREVENTIVE_CARE") else AlertCategory.MONITORING_DUE,
        raw_priority=AlertPriority.LOW,
        title="Annual Diabetic Retinal Eye Exam Overdue",
        description="Patient due for dilated eye exam.",
        trigger_rule="RULE_EYE_EXAM",
        timestamp="2026-09-21T10:00:00Z"
    )
    assert router.route_alert(nursing_alert) == "NURSING"

    physician_alert = ClinicalAlert(
        id="ALT-DOC",
        patient_id="P-01",
        category=AlertCategory.DRUG_INTERACTION,
        raw_priority=AlertPriority.CRITICAL,
        title="Severe Hyperkalemia Safety Gate Violation",
        description="Serum K+ 6.2 mEq/L.",
        trigger_rule="RULE_K_EMERGENCY",
        timestamp="2026-09-21T10:00:00Z"
    )
    assert router.route_alert(physician_alert) == "PHYSICIAN"
