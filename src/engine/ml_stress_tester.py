"""
ML Stress-Tester & Calibration Hardening Module.
Evaluates CalibratedClassifierCV under severe class-imbalance scenarios
(e.g., 90:10, 95:5, 98:2 nuisance noise vs actionable alerts).
Calculates Brier Score, Expected Calibration Error (ECE), PR-AUC,
and verifies probability threshold stability under high alert volumes.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from sklearn.metrics import brier_score_loss, precision_recall_curve, auc, roc_auc_score
from sklearn.calibration import calibration_curve

try:
    from .ml_triage_classifier import MLTriageClassifier
except (ImportError, ValueError):
    from src.engine.ml_triage_classifier import MLTriageClassifier

class MLStressTester:
    """
    Stress-tests the CDS alert triage classifier across extreme class imbalance regimes
    and measures probability calibration stability.
    """

    def __init__(self, classifier: MLTriageClassifier = None):
        self.classifier = classifier or MLTriageClassifier()

    def generate_imbalanced_stream(
        self,
        n_samples: int = 2000,
        noise_ratio: float = 0.95,
        random_state: int = 101
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates a synthetic alert stream with controlled severe noise imbalance.
        noise_ratio = 0.95 means 95% nuisance/non-actionable alerts and 5% actionable alerts.
        """
        np.random.seed(random_state)
        n_noise = int(n_samples * noise_ratio)
        n_actionable = n_samples - n_noise

        # Generate Nuisance samples (y=0)
        noise_preventive = np.zeros(n_noise)
        noise_duplicate = np.random.choice([0, 1], size=n_noise, p=[0.2, 0.8])
        noise_age = np.random.randint(45, 80, size=n_noise)
        noise_conditions = np.random.randint(2, 5, size=n_noise)
        noise_meds = np.random.randint(4, 12, size=n_noise)
        noise_recency = np.random.exponential(scale=20, size=n_noise)
        noise_delta = np.random.normal(loc=1.0, scale=4.0, size=n_noise)
        noise_override_rate = np.random.uniform(0.80, 0.98, size=n_noise)
        noise_titration = np.zeros(n_noise)
        noise_urgency = np.random.choice([1, 2], size=n_noise, p=[0.75, 0.25])

        X_noise = np.column_stack([
            noise_preventive, noise_duplicate, noise_age, noise_conditions, noise_meds,
            noise_recency, noise_delta, noise_override_rate, noise_titration, noise_urgency
        ])
        y_noise = np.zeros(n_noise, dtype=int)

        # Generate Actionable samples (y=1)
        act_preventive = np.random.choice([0, 1], size=n_actionable, p=[0.4, 0.6])
        act_duplicate = np.zeros(n_actionable)
        act_age = np.random.randint(50, 88, size=n_actionable)
        act_conditions = np.random.randint(3, 6, size=n_actionable)
        act_meds = np.random.randint(5, 14, size=n_actionable)
        act_recency = np.random.exponential(scale=90, size=n_actionable)
        act_delta = np.random.normal(loc=18.0, scale=12.0, size=n_actionable)
        act_override_rate = np.random.uniform(0.10, 0.40, size=n_actionable)
        act_titration = np.random.choice([0, 1], size=n_actionable, p=[0.5, 0.5])
        act_urgency = np.random.choice([3, 4], size=n_actionable, p=[0.5, 0.5])

        X_act = np.column_stack([
            act_preventive, act_duplicate, act_age, act_conditions, act_meds,
            act_recency, act_delta, act_override_rate, act_titration, act_urgency
        ])
        y_act = np.ones(n_actionable, dtype=int)

        # Concatenate and shuffle
        X = np.vstack([X_noise, X_act])
        y = np.concatenate([y_noise, y_act])
        indices = np.random.permutation(n_samples)
        return X[indices], y[indices]

    def calculate_ece(self, y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
        """Calculates Expected Calibration Error (ECE)."""
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        n_samples = len(y_true)

        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]
            in_bin = (y_prob > bin_lower) & (y_prob <= bin_upper) if i > 0 else (y_prob >= bin_lower) & (y_prob <= bin_upper)
            bin_size = np.sum(in_bin)

            if bin_size > 0:
                bin_acc = np.mean(y_true[in_bin])
                bin_conf = np.mean(y_prob[in_bin])
                ece += (bin_size / n_samples) * np.abs(bin_acc - bin_conf)

        return float(ece)

    def run_stress_test(self, scenarios: List[float] = None) -> Dict[str, Any]:
        """
        Runs stress-testing across multiple class imbalance regimes:
        90:10 (0.90), 95:5 (0.95), 98:2 (0.98).
        """
        if scenarios is None:
            scenarios = [0.90, 0.95, 0.98]

        results = {
            "summary": "ML Calibration Stress Test under Severe Noise Imbalance",
            "model_type": "GradientBoostingClassifier with Sigmoidal Calibration",
            "scenarios": []
        }

        for noise_ratio in scenarios:
            X, y = self.generate_imbalanced_stream(n_samples=2500, noise_ratio=noise_ratio, random_state=42)
            y_probs = self.classifier.model.predict_proba(X)[:, 1]

            # Metrics
            brier = float(brier_score_loss(y, y_probs))
            ece = self.calculate_ece(y, y_probs, n_bins=10)
            precision_arr, recall_arr, _ = precision_recall_curve(y, y_probs)
            pr_auc = float(auc(recall_arr, precision_arr))
            roc_auc = float(roc_auc_score(y, y_probs))

            # Reliability curve
            prob_true, prob_pred = calibration_curve(y, y_probs, n_bins=8, strategy='uniform')

            # Threshold evaluation at 0.35
            y_pred_35 = (y_probs >= 0.35).astype(int)
            false_negatives = int(np.sum((y == 1) & (y_pred_35 == 0)))
            false_positives = int(np.sum((y == 0) & (y_pred_35 == 1)))
            true_positives = int(np.sum((y == 1) & (y_pred_35 == 1)))
            true_negatives = int(np.sum((y == 0) & (y_pred_35 == 0)))

            scenario_metric = {
                "noise_ratio": noise_ratio,
                "noise_percentage": f"{int(noise_ratio * 100)}% Noise : {int((1 - noise_ratio) * 100)}% Actionable",
                "total_samples": len(y),
                "actionable_count": int(np.sum(y == 1)),
                "noise_count": int(np.sum(y == 0)),
                "brier_score": round(brier, 4),
                "ece": round(ece, 4),
                "pr_auc": round(pr_auc, 4),
                "roc_auc": round(roc_auc, 4),
                "zero_fn_satisfied": (false_negatives == 0),
                "false_negatives": false_negatives,
                "false_positives": false_positives,
                "true_positives": true_positives,
                "true_negatives": true_negatives,
                "calibration_curve": {
                    "prob_pred": [round(float(p), 3) for p in prob_pred],
                    "prob_true": [round(float(p), 3) for p in prob_true]
                }
            }
            results["scenarios"].append(scenario_metric)

        return results

if __name__ == "__main__":
    tester = MLStressTester()
    res = tester.run_stress_test()
    import json
    print(json.dumps(res, indent=2))
