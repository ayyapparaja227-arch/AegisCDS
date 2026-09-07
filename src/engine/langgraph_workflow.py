"""
LangGraph Clinical State Machine for Outpatient MCC Alert Triage and Decision Support.
Implements a stateful, cyclic workflow with Deterministic Safety Gates, ML Actionability Scoring,
LangChain Clinical Guideline RAG, Care Bundling, and Human-in-the-Loop (HITL) review checkpoints.
"""

from typing import TypedDict, List, Dict, Any, Optional
import uuid
import time

from langgraph.graph import StateGraph, END
from .models import Patient, ClinicalAlert, CareBundle, AlertStatus, AlertPriority, to_dict
from .deterministic_safety_gate import DeterministicSafetyGate
from .ml_triage_classifier import MLTriageClassifier
from .guideline_rag import ClinicalGuidelineRAG

class ClinicalTriageState(TypedDict):
    """The shared state schema for the LangGraph clinical triage pipeline."""
    session_id: str
    patient: Dict[str, Any]
    incoming_alerts: List[Dict[str, Any]]
    
    # Layer 1 outputs
    critical_bypass_alerts: List[Dict[str, Any]]
    standard_alert_pool: List[Dict[str, Any]]
    
    # Layer 2 outputs
    scored_alerts: List[Dict[str, Any]]
    suppressed_alerts: List[Dict[str, Any]]
    actionable_alerts: List[Dict[str, Any]]
    
    # Layer 3 RAG & Bundling outputs
    guideline_citations: List[str]
    care_bundles: List[Dict[str, Any]]
    
    # Metrics
    alert_reduction_rate: float
    time_saved_sec: float
    
    # Human-in-the-Loop (HITL) Checkpoint State
    requires_human_approval: bool
    current_step: str
    hitl_decision: Optional[str]              # "PENDING", "APPROVED", "OVERRIDDEN", "MODIFIED"
    hitl_override_reason: Optional[str]
    hitl_timestamp: Optional[str]
    cpoe_dispatched_orders: List[Dict[str, Any]]

class LangGraphClinicalEngine:
    """Encapsulates the LangGraph clinical workflow with HITL approval gates."""

    def __init__(self):
        self.safety_gate = DeterministicSafetyGate()
        self.ml_classifier = MLTriageClassifier()
        self.rag = ClinicalGuidelineRAG()
        self.graph = self._build_workflow_graph()

    def _build_workflow_graph(self):
        workflow = StateGraph(ClinicalTriageState)

        # Register Nodes
        workflow.add_node("safety_gate_node", self._safety_gate_node)
        workflow.add_node("ml_triage_node", self._ml_triage_node)
        workflow.add_node("rag_evidence_node", self._rag_evidence_node)
        workflow.add_node("bundle_synthesizer_node", self._bundle_synthesizer_node)
        workflow.add_node("hitl_checkpoint_node", self._hitl_checkpoint_node)

        # Set Entry Point
        workflow.set_entry_point("safety_gate_node")

        # Routing from Safety Gate
        workflow.add_edge("safety_gate_node", "ml_triage_node")
        workflow.add_edge("ml_triage_node", "rag_evidence_node")
        workflow.add_edge("rag_evidence_node", "bundle_synthesizer_node")
        workflow.add_edge("bundle_synthesizer_node", "hitl_checkpoint_node")
        workflow.add_edge("hitl_checkpoint_node", END)

        return workflow.compile()

    def _safety_gate_node(self, state: ClinicalTriageState) -> Dict[str, Any]:
        """Node 1: Executes Layer 1 Deterministic Safety Invariants."""
        patient_data = state["patient"]
        alerts_data = state["incoming_alerts"]
        
        # Reconstruct models for safety check
        from .models import Patient, ClinicalAlert, Observation, MedicationRequest, AlertCategory, AlertPriority
        patient = Patient(
            id=patient_data["id"],
            mrn=patient_data["mrn"],
            name=patient_data["name"],
            age=patient_data["age"],
            gender=patient_data["gender"],
            conditions=patient_data["conditions"],
            active_medications=[MedicationRequest(**m) for m in patient_data.get("active_medications", [])],
            recent_observations=[Observation(**o) for o in patient_data.get("recent_observations", [])]
        )

        critical_bypasses = []
        standard_pool = []

        for a_dict in alerts_data:
            alert = ClinicalAlert(
                id=a_dict["id"],
                patient_id=a_dict["patient_id"],
                category=AlertCategory(a_dict["category"]),
                raw_priority=AlertPriority(a_dict["raw_priority"]),
                title=a_dict["title"],
                description=a_dict["description"],
                trigger_rule=a_dict["trigger_rule"],
                timestamp=a_dict["timestamp"]
            )
            is_bypass, crit_reason, emerg_meta = self.safety_gate.evaluate_safety_net(alert, patient)
            if is_bypass:
                a_dict["is_critical_safety_bypass"] = True
                a_dict["status"] = "ACTIVE_CRITICAL"
                a_dict["raw_priority"] = "CRITICAL"
                a_dict["actionability_score"] = 1.0
                a_dict["clinical_trajectory_note"] = crit_reason
                if emerg_meta and "stat_orders" in emerg_meta:
                    a_dict["suggested_actions"] = [{"action_type": "STAT_ORDER", "order_name": o["order"], "urgency": o["urgency"]} for o in emerg_meta["stat_orders"]]
                critical_bypasses.append(a_dict)
            else:
                standard_pool.append(a_dict)

        return {
            "critical_bypass_alerts": critical_bypasses,
            "standard_alert_pool": standard_pool,
            "current_step": "SAFETY_GATE_COMPLETED"
        }

    def _ml_triage_node(self, state: ClinicalTriageState) -> Dict[str, Any]:
        """Node 2: Executes Layer 2 Calibrated ML Actionability Scoring & Nuisance Suppression."""
        patient_data = state["patient"]
        pool = state["standard_alert_pool"]

        from .models import Patient, ClinicalAlert, Observation, MedicationRequest, AlertCategory, AlertPriority
        patient = Patient(
            id=patient_data["id"],
            mrn=patient_data["mrn"],
            name=patient_data["name"],
            age=patient_data["age"],
            gender=patient_data["gender"],
            conditions=patient_data["conditions"],
            active_medications=[MedicationRequest(**m) for m in patient_data.get("active_medications", [])],
            recent_observations=[Observation(**o) for o in patient_data.get("recent_observations", [])]
        )

        suppressed = []
        actionable = []
        scored = []

        for a_dict in pool:
            alert = ClinicalAlert(
                id=a_dict["id"],
                patient_id=a_dict["patient_id"],
                category=AlertCategory(a_dict["category"]),
                raw_priority=AlertPriority(a_dict["raw_priority"]),
                title=a_dict["title"],
                description=a_dict["description"],
                trigger_rule=a_dict["trigger_rule"],
                timestamp=a_dict["timestamp"]
            )
            score, feat_weights = self.ml_classifier.predict_actionability(alert, patient)
            a_dict["actionability_score"] = round(score, 3)
            a_dict["feature_weights"] = feat_weights

            if score < 0.35:
                a_dict["is_suppressed"] = True
                a_dict["status"] = "SUPPRESSED_NON_ACTIONABLE"
                if "duplicate" in alert.title.lower():
                    a_dict["suppression_reason"] = "Suppressed: Redundant testing within stability window (ADA 2024 Chapter 6)."
                elif "statin" in alert.title.lower() and "metformin" in alert.title.lower():
                    a_dict["suppression_reason"] = "Suppressed: Chronic tolerated baseline combination (96% prior override rate)."
                elif "blood pressure" in alert.title.lower() and "136" in alert.description:
                    a_dict["suppression_reason"] = "Suppressed: SBP 136 mmHg during titration; home log indicated (ACC/AHA 2023)."
                else:
                    a_dict["suppression_reason"] = f"Suppressed: Low clinical utility score ({score}) on stable vitals."
                suppressed.append(a_dict)
            else:
                a_dict["is_suppressed"] = False
                a_dict["status"] = "ACTIVE_ACTIONABLE"
                actionable.append(a_dict)

            scored.append(a_dict)

        return {
            "scored_alerts": scored,
            "suppressed_alerts": suppressed,
            "actionable_alerts": actionable,
            "current_step": "ML_TRIAGE_COMPLETED"
        }

    def _rag_evidence_node(self, state: ClinicalTriageState) -> Dict[str, Any]:
        """Node 3: LangChain RAG Evidence Grounding over KDIGO, ADA, and ACC/AHA guidelines."""
        patient_conditions = state["patient"]["conditions"]
        all_active = state["critical_bypass_alerts"] + state["actionable_alerts"]
        citations = set()

        for a in all_active:
            guide = self.rag.retrieve_guideline_evidence(a["title"], a["description"], patient_conditions)
            if guide:
                a["guideline_source"] = f"{guide['guideline']} ({guide['section']})"
                a["guideline_evidence"] = guide["recommendation_text"]
                citations.add(f"{guide['guideline']} - {guide['section']}")
                if not a.get("suggested_actions"):
                    a["suggested_actions"] = guide.get("suggested_actions", [])

        return {
            "guideline_citations": list(citations),
            "current_step": "RAG_EVIDENCE_ATTACHED"
        }

    def _bundle_synthesizer_node(self, state: ClinicalTriageState) -> Dict[str, Any]:
        """Node 4: Synthesizes Care Bundles enforcing Priority Hard-Floor Segregation."""
        criticals = state["critical_bypass_alerts"]
        actionables = state["actionable_alerts"]
        patient_id = state["patient"]["id"]
        bundles = []

        # 1. Critical Care Bundle (Never merged with routine)
        if criticals:
            crit_orders = []
            seen = set()
            for c in criticals:
                for act in c.get("suggested_actions", []):
                    if act["order_name"] not in seen:
                        seen.add(act["order_name"])
                        crit_orders.append(act)

            bundles.append({
                "id": f"BUNDLE-CRIT-{uuid.uuid4().hex[:6]}",
                "patient_id": patient_id,
                "title": "EMERGENCY CLINICAL SAFETY INTERVENTION",
                "priority": "CRITICAL",
                "category_summary": "Severe Physiological Hazard: Hyperkalemia / AKI",
                "consolidated_alert_ids": [c["id"] for c in criticals],
                "clinical_rationale": "Per KDIGO 2024: Immediate cardiac assessment and suspension of nephrotoxic / RAAS agents required.",
                "evidence_citation": "KDIGO 2024 Clinical Practice Guideline for CKD Management (Rec 1.3.2)",
                "suggested_orders": crit_orders,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "AWAITING_HUMAN_APPROVAL"
            })

        # 2. Actionable Routine / Preventive Bundle
        if actionables:
            rout_orders = []
            seen = set()
            for a in actionables:
                for act in a.get("suggested_actions", []):
                    if act["order_name"] not in seen:
                        seen.add(act["order_name"])
                        rout_orders.append(act)

            bundles.append({
                "id": f"BUNDLE-MCC-{uuid.uuid4().hex[:6]}",
                "patient_id": patient_id,
                "title": "MCC Comprehensive Annual Preventive & Monitoring Bundle",
                "priority": "MEDIUM",
                "category_summary": "Consolidated Preventive Care & Annual Screenings",
                "consolidated_alert_ids": [a["id"] for a in actionables],
                "clinical_rationale": "Joint ADA-KDIGO 2024: Consolidated diabetic preventive exams reduce fragmentation and improve screening adherence.",
                "evidence_citation": "ADA Standards of Care in Diabetes (2024) | KDIGO CKD Consensus",
                "suggested_orders": rout_orders,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "AWAITING_HUMAN_APPROVAL"
            })

        raw_total = len(state["incoming_alerts"])
        bundle_total = len(bundles)
        reduction = round(((raw_total - bundle_total) / raw_total * 100.0), 1) if raw_total > 0 else 0.0
        time_saved = round(len(state["suppressed_alerts"]) * 20.0 + (raw_total - bundle_total) * 12.0, 1)

        return {
            "care_bundles": bundles,
            "alert_reduction_rate": reduction,
            "time_saved_sec": time_saved,
            "current_step": "CARE_BUNDLES_SYNTHESIZED"
        }

    def _hitl_checkpoint_node(self, state: ClinicalTriageState) -> Dict[str, Any]:
        """Node 5: Human-in-the-Loop (HITL) Checkpoint."""
        # Holds the execution in AWAITING_HUMAN_APPROVAL until clinician acts on frontend
        requires_approval = len(state["care_bundles"]) > 0
        return {
            "requires_human_approval": requires_approval,
            "hitl_decision": "PENDING_CLINICIAN_REVIEW",
            "current_step": "HITL_GATE_HOLDING"
        }

    def execute_pipeline(self, patient: Patient, alerts: List[ClinicalAlert]) -> ClinicalTriageState:
        """Runs the LangGraph pipeline from start to the HITL checkpoint."""
        initial_state: ClinicalTriageState = {
            "session_id": f"SESS-{uuid.uuid4().hex[:8]}",
            "patient": to_dict(patient),
            "incoming_alerts": [to_dict(a) for a in alerts],
            "critical_bypass_alerts": [],
            "standard_alert_pool": [],
            "scored_alerts": [],
            "suppressed_alerts": [],
            "actionable_alerts": [],
            "guideline_citations": [],
            "care_bundles": [],
            "alert_reduction_rate": 0.0,
            "time_saved_sec": 0.0,
            "requires_human_approval": True,
            "current_step": "INITIALIZED",
            "hitl_decision": "PENDING",
            "hitl_override_reason": None,
            "hitl_timestamp": None,
            "cpoe_dispatched_orders": []
        }
        return self.graph.invoke(initial_state)

    def resume_hitl(self, current_state: ClinicalTriageState, decision: str, reason: Optional[str] = None) -> ClinicalTriageState:
        """Resumes the graph after clinician approval or override in the HITL gate."""
        current_state["hitl_decision"] = decision
        current_state["hitl_override_reason"] = reason
        current_state["hitl_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        current_state["requires_human_approval"] = False
        
        if decision == "APPROVED":
            all_orders = []
            for b in current_state.get("care_bundles", []):
                all_orders.extend(b.get("suggested_orders", []))
            current_state["cpoe_dispatched_orders"] = all_orders
            current_state["current_step"] = "CPOE_ORDERS_DISPATCHED"
        else:
            current_state["cpoe_dispatched_orders"] = []
            current_state["current_step"] = f"CLINICIAN_{decision}_LOGGED"

        return current_state
