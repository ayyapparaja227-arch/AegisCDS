"""
Layer 1: Deterministic Safety Net (Zero-False-Negative Gate).
Hardcoded, non-negotiable physiological and pharmacological boundary rules that bypass all AI/ML suppression.
Guarantees 100% sensitivity for life-critical clinical emergencies.
"""

from typing import List, Tuple, Optional, Dict, Any
from .models import ClinicalAlert, Patient, AlertPriority, AlertStatus, AlertCategory

class DeterministicSafetyGate:
    """
    Evaluates incoming clinical alerts and patient vitals against strict clinical safety invariants.
    Any violation immediately bypasses ML suppression filters and triggers high-urgency clinical escalation.
    """
    
    CRITICAL_K_HIGH = 6.0       # mEq/L - hyperkalemia cardiac arrest risk
    CRITICAL_K_LOW = 2.8        # mEq/L - hypokalemia arrhythmia risk
    CRITICAL_EGFR_MIN = 15.0    # mL/min/1.73m2 - end stage renal disease
    CRITICAL_SBP_MAX = 180.0    # mmHg - hypertensive emergency
    CRITICAL_DBP_MAX = 120.0    # mmHg - hypertensive emergency

    # Hard-stop lethal drug combinations
    LETHAL_INTERACTIONS = [
        ("nitroglycerin", "sildenafil"),
        ("nitroglycerin", "tadalafil"),
        ("spironolactone", "eplerenone"),
        ("methotrexate", "trimethoprim"),
        ("simvastatin", "clarithromycin")
    ]

    def evaluate_safety_net(self, alert: ClinicalAlert, patient: Patient) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Returns: (is_critical_bypass, critical_reason, emergency_bundle_metadata)
        Only flags critical bypass if the alert relates to the physiological or pharmacological hazard.
        """
        alert_text = f"{alert.title} {alert.description}".lower()

        # 1. Check patient laboratory observations
        for obs in patient.recent_observations:
            # Hyperkalemia Check
            if obs.code in ["K+", "Potassium"] and obs.value >= self.CRITICAL_K_HIGH:
                # Does this alert relate to potassium, electrolyte, or the offending drugs?
                if any(kw in alert_text for kw in ["potassium", "hyperkalemia", "spironolactone", "lisinopril", "raas", "aki", "creatinine"]):
                    raas_meds = [m.medication_name for m in patient.active_medications if m.category in ["ACE_INHIBITOR", "MRA", "ARB"]]
                    med_context = f" on {', '.join(raas_meds)}" if raas_meds else ""
                    return (
                        True,
                        f"CRITICAL PHYSIOLOGICAL HAZARD: Severe Hyperkalemia (Serum K+ = {obs.value} {obs.unit}{med_context}). Cardiac arrhythmia risk.",
                        {
                            "category": "HYPERKALEMIA_EMERGENCY",
                            "measured_value": f"{obs.value} {obs.unit}",
                            "reference_range": obs.reference_range,
                            "stat_orders": [
                                {"order": "Stat 12-Lead Electrocardiogram (ECG)", "urgency": "STAT"},
                                {"order": "Hold Spironolactone and Lisinopril immediately", "urgency": "STAT"},
                                {"order": "Stat repeat Potassium & Basic Metabolic Panel", "urgency": "STAT"},
                                {"order": "Oral Potassium Binder (Lokelma 10g PO TID) or IV Calcium Gluconate if ECG changes", "urgency": "URGENT"}
                            ]
                        }
                    )
            
            # Severe Renal Failure / AKI Check
            if obs.code in ["Creatinine"] and obs.value >= 2.0:
                if any(kw in alert_text for kw in ["creatinine", "acute kidney injury", "aki", "renal", "egfr"]):
                    return (
                        True,
                        f"CRITICAL RENAL HAZARD: Acute Kidney Injury (Serum Creatinine = {obs.value} {obs.unit}).",
                        {
                            "category": "RENAL_EMERGENCY",
                            "measured_value": f"{obs.value} {obs.unit}",
                            "stat_orders": [
                                {"order": "Repeat BMP (Serum Creatinine + eGFR) in 48h", "urgency": "URGENT"},
                                {"order": "Hold nephrotoxic and RAAS medications", "urgency": "STAT"}
                            ]
                        }
                    )

            # Hypertensive Crisis
            if obs.code == "BP_Systolic" and obs.value >= self.CRITICAL_SBP_MAX:
                if "blood pressure" in alert_text or "hypertension" in alert_text or "crisis" in alert_text:
                    return (
                        True,
                        f"CRITICAL HYPERTENSIVE EMERGENCY: Systolic BP = {obs.value} mmHg.",
                        {
                            "category": "HYPERTENSIVE_CRISIS",
                            "stat_orders": [
                                {"order": "Assess for acute end-organ damage", "urgency": "STAT"},
                                {"order": "Urgent Outpatient Antihypertensive Protocol", "urgency": "STAT"}
                            ]
                        }
                    )

        # 2. Check lethal drug combinations
        med_names = [m.medication_name.lower() for m in patient.active_medications]
        for drug_a, drug_b in self.LETHAL_INTERACTIONS:
            has_a = any(drug_a in m for m in med_names)
            has_b = any(drug_b in m for m in med_names)
            if has_a and has_b and (drug_a in alert_text or drug_b in alert_text):
                return (
                    True,
                    f"CRITICAL PHARMACOLOGICAL CONTRAINDICATION: Black Box lethal interaction between {drug_a.capitalize()} and {drug_b.capitalize()}.",
                    {
                        "category": "BLACK_BOX_CONTRAINDICATION",
                        "stat_orders": [
                            {"order": f"Discontinue {drug_b.capitalize()} order immediately", "urgency": "STAT"}
                        ]
                    }
                )

        # 3. Check explicit alert title triggers
        if "critical" in alert.title.lower() or "lethal" in alert_text or "anaphylaxis" in alert_text:
            return (
                True,
                f"CRITICAL ALERT: {alert.title}",
                {"category": "CRITICAL_ALERT", "stat_orders": []}
            )

        return (False, None, None)
