"""
Automated PyTest Suite: ML Calibration & Stress-Testing under Class Imbalance.
"""

import pytest
from src.engine.ml_stress_tester import MLStressTester
from src.engine.ml_triage_classifier import MLTriageClassifier

def test_ml_calibration_brier_score():
    """Verify that Brier score remains low (<0.05) and ECE is tight (<0.05) under 95% noise."""
    tester = MLStressTester()
    res = tester.run_stress_test(scenarios=[0.95])
    scenario = res["scenarios"][0]

    assert scenario["brier_score"] < 0.05
    assert scenario["ece"] < 0.05
    assert scenario["pr_auc"] > 0.90
    assert scenario["roc_auc"] > 0.95

def test_extreme_98_percent_imbalance():
    """Verify stability under extreme 98% nuisance noise imbalance."""
    tester = MLStressTester()
    res = tester.run_stress_test(scenarios=[0.98])
    scenario = res["scenarios"][0]

    assert scenario["brier_score"] < 0.05
    assert scenario["true_positives"] > 0
    assert scenario["true_negatives"] > 2000
