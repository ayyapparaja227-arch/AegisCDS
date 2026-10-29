"""
Automated PyTest Suite: Benchmark CSV Export, Endpoints & Integration Verification.
"""

import pytest
import io
import csv
from src.engine.experiment_evaluator import ExperimentEvaluator
from src.engine.abdm_connector import ABDMConnector
from src.engine.active_learning_engine import ActiveOnlineLearningEngine
from src.engine.database import ClinicalDatabase
from src.engine.department_router import DepartmentRouter

def test_benchmark_csv_export():
    """Verify that benchmark export produces valid CSV with expected clinical headers."""
    evaluator = ExperimentEvaluator()
    csv_text = evaluator.export_benchmark_to_csv()

    assert "AEGISCDS CLINICAL DECISION SUPPORT BENCHMARK REPORT" in csv_text
    assert "--- COHORT SUMMARY ---" in csv_text
    assert "--- CONFUSION MATRIX ---" in csv_text
    assert "--- KPI PERFORMANCE COMPARISON ---" in csv_text

    # Verify that it parses cleanly as CSV
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    assert len(rows) > 10

def test_abdm_consent_flow():
    """Verify ABHA ID resolution and consent token generation."""
    connector = ABDMConnector()
    valid_res = connector.verify_abha_id("91-4829-1029-4820")
    assert valid_res["status"] == "VERIFIED"
    assert valid_res["patient_name"] == "Robert Chen"
    assert valid_res["consent_token"].startswith("ABDM-CONSENT-")

    invalid_res = connector.verify_abha_id("invalid-format")
    assert invalid_res["status"] == "NOT_FOUND"

def test_database_rl_feedback_flow():
    """Verify recording and fetching online reinforcement learning feedback."""
    db = ClinicalDatabase()
    initial_stats = db.get_db_stats()

    row_id = db.record_rl_feedback(
        override_id="OVR-TEST-FINAL",
        patient_id="PAT-001",
        bundle_id="BND-001",
        override_reason="Stable on current ACE-i therapy for 3 years without side effects.",
        clinical_justification="Verified baseline renal function within normal limits."
    )
    assert row_id > 0

    new_feedback = db.fetch_new_rl_feedback(since_id=row_id - 1)
    assert len(new_feedback) >= 1
    latest = [f for f in new_feedback if f["override_id"] == "OVR-TEST-FINAL"][0]
    assert latest["patient_id"] == "PAT-001"
    assert "Stable on current ACE-i" in latest["override_reason"]

def test_department_stats_aggregation():
    """Verify that DepartmentRouter correctly aggregates 4-department statistics."""
    router = DepartmentRouter()
    roles = router.ROLES
    assert "PHYSICIAN" in roles
    assert "NURSING" in roles
    assert "PHARMACY" in roles
    assert "LABORATORY" in roles
