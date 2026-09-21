"""
Automated PyTest Suite: Operational Failure Mode Simulators.
Tests:
1. Stale Lab Latency (Missing telemetry / >14 days lab rejection)
2. Over-Consolidation Masking (Priority Hard-Floor emergency isolation)
3. LLM Hallucination / AI Drift (Guideline RAG verification & fallback)
"""

import pytest
from src.engine.edge_cases import EdgeCaseSimulator

def test_failure_mode_1_stale_lab():
    """Verify that a 45-day-old potassium test blocks prescription and orders a STAT lab."""
    sim = EdgeCaseSimulator()
    res = sim.simulate_stale_lab_latency()
    
    assert "mitigated" in res
    assert res["mitigated"]["clinical_harm_prevented"] is True
    assert res["mitigated"]["guardrail_engaged"] == "RECENCY_DATA_GAP_CIRCUIT_BREAKER"
    assert "STAT" in str(res["mitigated"]["generated_alert"]) or "Stat" in str(res["mitigated"]["generated_alert"])

def test_failure_mode_2_over_consolidation():
    """Verify that critical emergencies cannot be grouped into routine bundles."""
    sim = EdgeCaseSimulator()
    res = sim.simulate_over_consolidation_hazard()

    assert "mitigated" in res
    assert res["mitigated"]["clinical_harm_prevented"] is True
    assert res["mitigated"]["guardrail_engaged"] == "PRIORITY_HARD_FLOOR_SEGREGATION"
    assert len(res["mitigated"]["bundles_created"]) >= 2

def test_failure_mode_3_llm_hallucination():
    """Verify that unverified medical AI advice is rejected and falls back to guideline RAG."""
    sim = EdgeCaseSimulator()
    res = sim.simulate_model_hallucination_drift()

    assert "mitigated" in res
    assert res["mitigated"]["clinical_harm_prevented"] is True
    assert res["mitigated"]["guardrail_engaged"] == "GROUNDED_RAG_SYNTAX_VERIFIER_AND_FALLBACK"
    assert "SAFETY-RAAS-DUAL-BLOCKADE" in res["mitigated"]["diagnostic_log"]
