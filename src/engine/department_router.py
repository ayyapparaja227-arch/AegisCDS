"""
Multi-Department Role-Based Alert Router for AegisCDS.
Segments alerts into specialized role streams:
1. Physician (Medication decisions, diagnosis conflicts, hard safety gates)
2. Nursing (Vitals monitoring, preventive screening, vaccine gaps)
3. Pharmacy (DDI, dose adjustments, renal titration)
4. Laboratory (Critical lab panic values, missing telemetry orders)
"""

from typing import Dict, Any, List, Optional
try:
    from .models import ClinicalAlert, CareBundle, AlertCategory, AlertPriority
except (ImportError, ValueError):
    from src.engine.models import ClinicalAlert, CareBundle, AlertCategory, AlertPriority

class DepartmentRouter:
    """
    Routes alerts and care bundles to the appropriate clinical care team members.
    
    Clinical Justification:
    Alert fatigue is exacerbated when all notifications are dumped into the physician's inbox.
    By partitioning recommendations into role-specific streams (Physician, Nursing, Pharmacy, Laboratory),
    providers only see decisions relevant to their scope of practice.
    """

    ROLES = ["PHYSICIAN", "NURSING", "PHARMACY", "LABORATORY"]

    def route_alert(self, alert: ClinicalAlert) -> str:
        """
        Determines the target department for a single clinical alert.
        
        Routing Policy:
        - Critical Safety Invariants & Life Threats -> PHYSICIAN (Requires immediate medical evaluation)
        - Preventive Screening & Vitals Overdue     -> NURSING (Within outpatient nurse workflow)
        - STAT Blood Draws & Laboratory Orders      -> LABORATORY (Phlebotomy and lab triage)
        - Drug-Drug Interactions & Refill Titration -> PHARMACY (Clinical pharmacist review)
        - Default Fallback                          -> PHYSICIAN (Fail-safe clinical governance)
        
        Parameters:
            alert (ClinicalAlert): Incoming clinical alert model.
            
        Returns:
            str: One of 'PHYSICIAN', 'NURSING', 'PHARMACY', or 'LABORATORY'.
        """
        # Critical bypasses and hard safety alerts always go to the physician
        priority_val = getattr(alert, "raw_priority", getattr(alert, "priority", None))
        if priority_val in [AlertPriority.CRITICAL, AlertPriority.HIGH, "CRITICAL", "HIGH"] or "emergency" in alert.title.lower():
            return "PHYSICIAN"

        title_desc = f"{alert.title} {alert.description}".lower()

        # Nursing stream: preventive screenings, vaccinations, diabetic foot exams, eye exams
        if any(term in title_desc for term in ["foot exam", "eye exam", "retinal", "vaccine", "screening", "vital", "bp check"]):
            return "NURSING"

        # Laboratory stream: lab orders, stale labs, stat blood draw
        if any(term in title_desc for term in ["stat blood", "potassium test", "creatinine test", "repeat lab", "uacr"]):
            return "LABORATORY"

        # Pharmacy stream: drug interaction, refill, statin, titration
        if any(term in title_desc for term in ["drug interaction", "interaction", "refill", "statin", "contraindication", "dose"]):
            return "PHARMACY"

        return "PHYSICIAN"

    def route_care_bundle(self, bundle: CareBundle) -> Dict[str, Any]:
        """
        Categorizes bundle items across departments and determines the primary responsible role.
        
        Parameters:
            bundle (CareBundle): Synthesized multi-order care bundle.
            
        Returns:
            Dict[str, Any]: Routing breakdown with primary department and per-department order lists.
        """
        title_lower = (bundle.title + " " + bundle.clinical_rationale).lower()

        primary_role = "PHYSICIAN"
        if bundle.is_critical_bypass:
            primary_role = "PHYSICIAN"
        elif "preventive" in title_lower or "annual" in title_lower:
            primary_role = "NURSING"
        elif "interaction" in title_lower:
            primary_role = "PHARMACY"

        return {
            "bundle_id": bundle.id,
            "title": bundle.title,
            "primary_department": primary_role,
            "suggested_orders": bundle.suggested_orders,
            "department_breakdown": {
                "PHYSICIAN": [o for o in bundle.suggested_orders if any(k in o.lower() for k in ["stop", "prescribe", "ecg", "cardiology"])],
                "NURSING": [o for o in bundle.suggested_orders if any(k in o.lower() for k in ["exam", "screen", "vaccine", "schedule"])],
                "LABORATORY": [o for o in bundle.suggested_orders if any(k in o.lower() for k in ["lab", "blood", "test", "k+", "egfr", "repeat"])],
                "PHARMACY": [o for o in bundle.suggested_orders if any(k in o.lower() for k in ["lokelma", "dose", "statin", "medication", "dispense"])]
            }
        }
