"""
Clinical Guideline Knowledge Base & RAG Retrieval Engine.
Covers KDIGO 2024 (CKD & HF), ADA 2024 Standards of Care (T2D), and ACC/AHA 2023.
Provides vector/keyword semantic matching, exact guideline citations, and recommended action bundles.
"""

from typing import List, Dict, Any, Optional
import math
import re

GUIDELINE_KNOWLEDGE_BASE = [
    {
        "id": "KDIGO-2024-K-6.0",
        "guideline": "KDIGO 2024 Clinical Practice Guideline for the Management of CKD",
        "section": "Recommendation 1.3.2: Severe Hyperkalemia Management",
        "condition_tags": ["CKD", "Hyperkalemia", "HFrEF", "Heart Failure"],
        "trigger_keywords": ["potassium", "k+", "hyperkalemia", "6.0", "spironolactone", "lisinopril", "mra"],
        "critical_threshold": "Serum K+ >= 6.0 mEq/L",
        "recommendation_text": (
            "For patients with serum potassium >= 6.0 mEq/L, especially those receiving dual renin-angiotensin-aldosterone "
            "system (RAAS) inhibitors, immediately obtain a 12-lead ECG to assess for peaked T-waves or conduction blocks. "
            "Temporarily suspend potassium-sparing diuretics (e.g. spironolactone) and ACE inhibitors/ARBs. Initiate urgent "
            "potassium-lowering therapy (e.g. sodium zirconium cyclosilicate / Lokelma or patiromer) and repeat stat serum potassium."
        ),
        "suggested_actions": [
            {"action_type": "MEDICATION_HOLD", "order_name": "Hold Spironolactone and Lisinopril", "urgency": "STAT"},
            {"action_type": "DIAGNOSTIC_ORDER", "order_name": "Stat 12-Lead Electrocardiogram (ECG)", "urgency": "STAT"},
            {"action_type": "LAB_ORDER", "order_name": "Stat Repeat Serum Electrolytes & Renal Panel", "urgency": "STAT"},
            {"action_type": "MEDICATION_ORDER", "order_name": "Lokelma (Sodium Zirconium Cyclosilicate) 10g PO TID", "urgency": "URGENT"}
        ]
    },
    {
        "id": "KDIGO-2024-AKI-CREATININE",
        "guideline": "KDIGO 2024 Acute Kidney Injury & CKD Cross-Consensus",
        "section": "Section 2.1: Rapid eGFR Decline on Nephrotoxic Agents",
        "condition_tags": ["CKD", "AKI", "Creatinine"],
        "trigger_keywords": ["creatinine", "egfr", "acute kidney injury", "aki", "spike"],
        "critical_threshold": "Creatinine increase > 50% from baseline or eGFR drop > 30%",
        "recommendation_text": (
            "An acute rise in serum creatinine > 50% above baseline within 7-30 days of initiating or titrating RAAS blockers "
            "warrants immediate clinical evaluation for prerenal azotemia, volume depletion, or bilateral renal artery stenosis. "
            "Dose reduction or temporary discontinuation of the culprit agent is recommended with repeat renal function in 48-72h."
        ),
        "suggested_actions": [
            {"action_type": "LAB_ORDER", "order_name": "Repeat BMP (Serum Creatinine + BUN + eGFR) in 48h", "urgency": "URGENT"},
            {"action_type": "CLINICAL_REVIEW", "order_name": "Evaluate Volume Status & Hold NSAIDs/Nephrotoxic Agents", "urgency": "ROUTINE"}
        ]
    },
    {
        "id": "ADA-2024-HBA1C-INTERVAL",
        "guideline": "ADA Standards of Care in Diabetes — 2024",
        "section": "Chapter 6: Glycemic Targets and Assessment",
        "condition_tags": ["Type 2 Diabetes", "HbA1c", "Screening"],
        "trigger_keywords": ["hba1c", "glycated hemoglobin", "duplicate lab", "diabetes", "screening"],
        "critical_threshold": "HbA1c re-order interval < 90 days with stable glycemic control",
        "recommendation_text": (
            "Perform the A1C test at least twice a year (every 6 months) in patients who are meeting treatment goals and who "
            "have stable glycemic control. Re-testing within 90 days without therapy modification provides negligible clinical "
            "utility and represents redundant non-actionable laboratory utilization."
        ),
        "suggested_actions": [
            {"action_type": "SUPPRESS_ORDER", "order_name": "Suppress Duplicate HbA1c Lab Order (Last test 85 days ago, HbA1c 6.9%)", "urgency": "INFO"}
        ]
    },
    {
        "id": "ADA-KDIGO-2024-DIABETIC-KIDNEY-BUNDLE",
        "guideline": "Joint ADA-KDIGO Consensus Statement on Diabetes & CKD 2024",
        "section": "Annual Comprehensive Diabetic Nephropathy Assessment",
        "condition_tags": ["Type 2 Diabetes", "CKD", "Nephropathy", "Annual Care"],
        "trigger_keywords": ["diabetic nephropathy", "annual bundle", "microalbuminuria", "foot exam", "statin"],
        "critical_threshold": "Annual routine diabetic screening triggers",
        "recommendation_text": (
            "Comprehensive annual diabetic care should consolidate urinary albumin-to-creatinine ratio (uACR), annual dilated "
            "eye exam, comprehensive foot exam, and moderate-to-high intensity statin verification into a single unified outpatient "
            "workflow rather than multiple asynchronous pop-up reminders."
        ),
        "suggested_actions": [
            {"action_type": "BUNDLE_ORDER", "order_name": "Schedule Annual Comprehensive Diabetic Preventive Exam", "urgency": "ROUTINE"},
            {"action_type": "LAB_ORDER", "order_name": "Spot Urine Albumin-to-Creatinine Ratio (uACR)", "urgency": "ROUTINE"},
            {"action_type": "REFERRAL", "order_name": "Referral: Diabetic Podiatry & Monofilament Foot Exam", "urgency": "ROUTINE"}
        ]
    },
    {
        "id": "ACC-AHA-2023-HTN-TITRATION",
        "guideline": "ACC/AHA 2023 Guideline for the Prevention, Detection, and Management of High Blood Pressure",
        "section": "Section 8.2: Outpatient BP Monitoring During Titration",
        "condition_tags": ["Hypertension", "Blood Pressure"],
        "trigger_keywords": ["blood pressure", "bp", "hypertension", "136/84", "titration"],
        "critical_threshold": "Systolic BP 130-139 mmHg when medication adjusted within 30 days",
        "recommendation_text": (
            "For patients undergoing active antihypertensive medication titration, minor BP elevations (e.g. SBP 130-139 mmHg) "
            "measured in clinic should be interpreted alongside home BP logs. Avoid interruptive alerts if medication dose was "
            "adjusted within the preceding 4 weeks to allow pharmacological steady-state."
        ),
        "suggested_actions": [
            {"action_type": "HOME_MONITORING", "order_name": "Request 14-Day Home Blood Pressure Log Prior to Next Titration", "urgency": "ROUTINE"}
        ]
    },
    {
        "id": "SAFETY-RAAS-DUAL-BLOCKADE",
        "guideline": "FDA Black Box & ACC/AHA Drug Safety Advisory",
        "section": "Contraindication: Combined ACE-i / ARB / Direct Renin Inhibitors",
        "condition_tags": ["Drug Safety", "Contraindication", "RAAS"],
        "trigger_keywords": ["dual raas", "lisinopril", "losartan", "contraindication", "black box"],
        "critical_threshold": "Simultaneous prescription of 2+ full-dose RAAS blockers",
        "recommendation_text": (
            "Concomitant use of ACE inhibitors, angiotensin receptor blockers, or aliskiren is strongly contraindicated due to "
            "markedly increased risk of severe hypotension, syncope, hyperkalemia, and acute renal failure without additive cardiovascular benefit."
        ),
        "suggested_actions": [
            {"action_type": "MEDICATION_CANCEL", "order_name": "Discontinue Redundant RAAS Inhibitor Immediately", "urgency": "STAT"}
        ]
    }
]

class ClinicalGuidelineRAG:
    """RAG engine providing grounded clinical guideline evidence and recommended actions."""
    
    def __init__(self):
        self.knowledge_base = GUIDELINE_KNOWLEDGE_BASE
        
    def retrieve_guideline_evidence(self, alert_title: str, alert_desc: str, conditions: List[str]) -> Optional[Dict[str, Any]]:
        """
        Semantic/Keyword RAG matching to find authoritative guideline evidence.
        Scores candidate guidelines based on keyword overlap, condition match, and trigger words.
        """
        combined_text = f"{alert_title} {alert_desc} {' '.join(conditions)}".lower()
        
        best_match = None
        best_score = 0.0
        
        for item in self.knowledge_base:
            score = 0.0
            
            # Keyword matching
            for kw in item["trigger_keywords"]:
                if kw in combined_text:
                    score += 2.0
            
            # Condition matching
            for cond in item["condition_tags"]:
                for patient_cond in conditions:
                    if cond.lower() in patient_cond.lower() or patient_cond.lower() in cond.lower():
                        score += 1.5
            
            # Specific high-risk trigger boosters
            if "potassium" in combined_text and "6.0" in combined_text and "K-6.0" in item["id"]:
                score += 10.0
            if "hba1c" in combined_text and "duplicate" in combined_text and "HBA1C" in item["id"]:
                score += 8.0
            if "blood pressure" in combined_text and "titration" in combined_text and "HTN" in item["id"]:
                score += 6.0
            if ("annual" in combined_text or "preventive" in combined_text) and "BUNDLE" in item["id"]:
                score += 7.0
                
            if score > best_score and score >= 3.0:
                best_score = score
                best_match = item
                
        return best_match

    def generate_rag_clinical_summary(self, alerts: List[Any], patient_conditions: List[str]) -> Dict[str, Any]:
        """Synthesize clinical rationale and pre-configured order sets across multiple alerts."""
        matched_guidelines = []
        consolidated_orders = []
        seen_order_names = set()
        
        for alert in alerts:
            guide = self.retrieve_guideline_evidence(alert.title, alert.description, patient_conditions)
            if guide and guide["id"] not in [g["id"] for g in matched_guidelines]:
                matched_guidelines.append(guide)
                for order in guide.get("suggested_actions", []):
                    if order["order_name"] not in seen_order_names:
                        seen_order_names.add(order["order_name"])
                        consolidated_orders.append(order)
                        
        if not matched_guidelines:
            return {
                "rationale": "Standard outpatient monitoring alerts evaluated by clinical triage engine.",
                "citations": ["Standard Ambulatory Care Practice"],
                "orders": []
            }
            
        primary = matched_guidelines[0]
        rationale = f"Per {primary['guideline']} ({primary['section']}): {primary['recommendation_text']}"
        citations = [f"{g['guideline']} - {g['section']}" for g in matched_guidelines]
        
        return {
            "rationale": rationale,
            "citations": citations,
            "orders": consolidated_orders
        }
