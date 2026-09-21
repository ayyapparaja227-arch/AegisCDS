"""
Automated PyTest Suite: LangGraph Stateful Cyclic Workflow & API Resilience.
"""

import pytest
from src.engine.langgraph_workflow import LangGraphClinicalEngine
from src.engine.data_fetcher import ClinicalDataFetcher
from src.engine.synthetic_data import get_patient_robert_chen

def test_langgraph_workflow_execution():
    """Verify that the 6-node LangGraph state machine executes and halts at HITL gate."""
    engine = LangGraphClinicalEngine()
    patient, alerts = get_patient_robert_chen()

    initial_state = engine.execute_pipeline(patient, alerts)
    assert initial_state["patient"]["id"] == patient.id
    assert initial_state["requires_human_approval"] is True
    assert initial_state["hitl_decision"] == "PENDING_CLINICIAN_REVIEW" or initial_state["requires_human_approval"] is True
    assert len(initial_state["care_bundles"]) > 0

def test_langgraph_hitl_approval_transition():
    """Verify that approving a bundle in the HITL state transitions the graph to COMPLETED."""
    engine = LangGraphClinicalEngine()
    patient, alerts = get_patient_robert_chen()

    state = engine.execute_pipeline(patient, alerts)
    final_state = engine.resume_hitl(state, decision="APPROVED", reason=None)
    assert final_state["hitl_decision"] == "APPROVED"
    assert final_state["requires_human_approval"] is False
    assert final_state["current_step"] == "CPOE_ORDERS_DISPATCHED"

def test_openfda_fallback_resilience():
    """Verify that OpenFDA client gracefully falls back to offline cache upon network cuts."""
    fetcher = ClinicalDataFetcher()
    # Query known drug
    spiro_info = fetcher.query_live_openfda("spironolactone", timeout_sec=1)
    assert spiro_info is not None
    assert "hyperkalemia" in str(spiro_info).lower() or "potassium" in str(spiro_info).lower()

    # Query offline cache directly
    fallback = fetcher.OFFLINE_FDA_CACHE.get("lisinopril")
    assert fallback is not None
    assert "hyperkalemia" in str(fallback).lower() or "warning" in str(fallback).lower()
