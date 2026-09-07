"""
FHIR R4 Data Models and Core Types for Outpatient MCC Clinical Decision Support.
Defines Patient, Observation, MedicationRequest, ClinicalAlert, CareBundle, and OverrideAudit.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import json
import uuid
import time

class AlertPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AlertCategory(str, Enum):
    DRUG_INTERACTION = "DRUG_INTERACTION"
    LAB_ABNORMALITY = "LAB_ABNORMALITY"
    MONITORING_DUE = "MONITORING_DUE"
    CONTRAINDICATION = "CONTRAINDICATION"
    DOSING_GUIDELINE = "DOSING_GUIDELINE"

class AlertStatus(str, Enum):
    RAW = "RAW"
    SUPPRESSED_NON_ACTIONABLE = "SUPPRESSED_NON_ACTIONABLE"
    CONSOLIDATED = "CONSOLIDATED"
    ACTIVE_CRITICAL = "ACTIVE_CRITICAL"
    ACTIVE_ACTIONABLE = "ACTIVE_ACTIONABLE"

@dataclass
class Observation:
    id: str
    code: str                  # e.g., "K+", "Creatinine", "eGFR", "HbA1c", "BP_Systolic", "BP_Diastolic"
    display: str               # Human readable label
    value: float
    unit: str
    timestamp: str             # ISO timestamp
    reference_range: str       # e.g., "3.5 - 5.0 mEq/L"
    status: str = "final"

@dataclass
class MedicationRequest:
    id: str
    medication_code: str       # RxNorm or generic code
    medication_name: str       # e.g., "Lisinopril 20mg daily"
    category: str              # e.g., "ACE_INHIBITOR", "MRA", "STATIN", "BIGUANIDE", "SGLT2i"
    dose: str
    frequency: str
    started_at: str
    status: str = "active"     # active, stopped, suspended

@dataclass
class Patient:
    id: str
    mrn: str
    name: str
    age: int
    gender: str
    conditions: List[str]      # e.g., ["Type 2 Diabetes", "CKD Stage 3b", "HFrEF", "Hypertension"]
    active_medications: List[MedicationRequest]
    recent_observations: List[Observation]
    encounter_type: str = "Outpatient Routine Follow-up"
    clinic_name: str = "St. Jude Outpatient MCC Clinic"

@dataclass
class ClinicalAlert:
    id: str
    patient_id: str
    category: AlertCategory
    raw_priority: AlertPriority
    title: str
    description: str
    trigger_rule: str
    timestamp: str
    
    # Layer 1 & 2 Engine Annotations
    status: AlertStatus = AlertStatus.RAW
    is_critical_safety_bypass: bool = False
    actionability_score: float = 0.0          # 0.0 to 1.0 (ML Calibrated)
    is_suppressed: bool = False
    suppression_reason: Optional[str] = None
    
    # Consolidation
    bundle_id: Optional[str] = None
    bundle_title: Optional[str] = None
    
    # Explainable Evidence
    guideline_source: Optional[str] = None     # e.g., "KDIGO 2024 Rec 1.3.2"
    guideline_evidence: Optional[str] = None   # Direct clinical guidance excerpt
    clinical_trajectory_note: Optional[str] = None
    
    # Actionable Order Set
    suggested_actions: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class CareBundle:
    id: str
    patient_id: str
    title: str
    priority: AlertPriority
    category_summary: str
    consolidated_alert_ids: List[str]
    clinical_rationale: str
    evidence_citation: str
    suggested_orders: List[Dict[str, str]]
    timestamp: str
    is_reviewed: bool = False
    review_status: Optional[str] = None # "ACCEPTED", "OVERRIDDEN", "PENDING"

@dataclass
class OverrideAudit:
    id: str
    alert_or_bundle_id: str
    patient_id: str
    clinician_id: str
    timestamp: str
    action: str                        # "ACCEPTED", "OVERRIDDEN", "SNOOZED"
    override_reason: Optional[str] = None
    clinical_justification: Optional[str] = None

def to_dict(obj: Any) -> Any:
    """Recursively convert dataclass to dictionary with Enum handling."""
    if hasattr(obj, "__dataclass_fields__"):
        result = {}
        for key in obj.__dataclass_fields__:
            val = getattr(obj, key)
            result[key] = to_dict(val)
        return result
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list):
        return [to_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    return obj
