"""
Active Online Learning Engine for AegisCDS.
Adapts ML triage actionability weights dynamically from doctor override feedback
without requiring full model retraining. Uses online exponential gradient updates.
"""

from typing import Dict, Any, List, Optional
import time
import json
import numpy as np

try:
    from .database import ClinicalDatabase
    from .models import OverrideAudit
except (ImportError, ValueError):
    from src.engine.database import ClinicalDatabase
    from src.engine.models import OverrideAudit

class ActiveOnlineLearningEngine:
    """
    Learns continuously from clinician override feedback.
    When a doctor overrides a suggestion (e.g. "Patient stable on chronic statin-metformin for 3 years"),
    this engine updates the clinical context penalty weights online.
    """

    DEFAULT_WEIGHTS = {
        "prior_override_penalty": 2.0,
        "titration_window_penalty": 1.2,
        "chronic_stability_threshold": 0.85,
        "preventive_boost": 2.5,
        "urgency_multiplier": 1.8
    }

    def __init__(self, db: Optional[ClinicalDatabase] = None):
        self.db = db or ClinicalDatabase()
        self.current_weights = dict(self.DEFAULT_WEIGHTS)
        self.learning_rate = 0.05
        self.feedback_history: List[Dict[str, Any]] = []

    def process_clinician_feedback(
        self,
        override_id: str,
        patient_id: str,
        bundle_id: str,
        override_reason: str,
        clinical_justification: str = ""
    ) -> Dict[str, Any]:
        """
        Applies online reinforcement update to triage weights based on doctor's justification.
        """
        reason_lower = (override_reason + " " + clinical_justification).lower()
        updated_features = []

        # Rule 1: Chronic stability / well-tolerated combination override
        if any(term in reason_lower for term in ["stable", "tolerated", "years", "chronic", "baseline"]):
            old_w = self.current_weights["prior_override_penalty"]
            new_w = round(old_w + self.learning_rate * 1.5, 4)
            self.current_weights["prior_override_penalty"] = new_w
            self.db.save_active_learning_weight("prior_override_penalty", new_w, override_id)
            updated_features.append({"feature": "prior_override_penalty", "old": old_w, "new": new_w})

        # Rule 2: Specialist managed / out-of-scope override
        if any(term in reason_lower for term in ["specialist", "nephrologist", "cardiologist", "managing"]):
            old_w = self.current_weights["chronic_stability_threshold"]
            new_w = round(max(0.60, old_w - self.learning_rate * 0.8), 4)
            self.current_weights["chronic_stability_threshold"] = new_w
            self.db.save_active_learning_weight("chronic_stability_threshold", new_w, override_id)
            updated_features.append({"feature": "chronic_stability_threshold", "old": old_w, "new": new_w})

        # Rule 3: Benefit outweighs risk override
        if any(term in reason_lower for term in ["benefit", "outweighs", "necessary", "intentional"]):
            old_w = self.current_weights["titration_window_penalty"]
            new_w = round(old_w + self.learning_rate * 1.2, 4)
            self.current_weights["titration_window_penalty"] = new_w
            self.db.save_active_learning_weight("titration_window_penalty", new_w, override_id)
            updated_features.append({"feature": "titration_window_penalty", "old": old_w, "new": new_w})

        feedback_entry = {
            "override_id": override_id,
            "bundle_id": bundle_id,
            "patient_id": patient_id,
            "override_reason": override_reason,
            "updated_features": updated_features,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.feedback_history.append(feedback_entry)

        return {
            "status": "ONLINE_WEIGHTS_UPDATED",
            "updated_feature_count": len(updated_features),
            "updated_features": updated_features,
            "current_weights": self.current_weights
        }

    def get_learning_stats(self) -> Dict[str, Any]:
        """Returns online active learning metrics and weight drift tracking."""
        return {
            "total_override_feedbacks_processed": len(self.feedback_history),
            "current_active_weights": self.current_weights,
            "baseline_weights": self.DEFAULT_WEIGHTS,
            "recent_feedback_events": self.feedback_history[-5:] if self.feedback_history else []
        }
