"""
Ayushman Bharat Digital Mission (ABDM) FHIR Sandbox Connector for AegisCDS.
Enables Indian National Digital Health Ecosystem interoperability:
- ABHA (Ayushman Bharat Health Account) ID Verification & Resolution
- ABDM Milestone 1 (M1 - ABHA creation/linking)
- ABDM Milestone 2 (M2 - Discovery & Linking of Health Records)
- ABDM Milestone 3 (M3 - FHIR R4 Diagnostic Report & Prescription Health Document Exchange)
"""

from typing import Dict, Any, List, Optional
import uuid
import time
import re

try:
    from .models import Patient, Observation, MedicationRequest
except (ImportError, ValueError):
    from src.engine.models import Patient, Observation, MedicationRequest

class ABDMConnector:
    """
    Simulates ABDM Gateway and Health Information Provider (HIP) / User (HIU)
    interfaces for Indian outpatient clinics (e.g. Tamil Nadu ABDM Sandbox).
    """

    # Simulated National Health Authority (NHA) Registry of ABHA IDs
    SAMPLE_ABHA_REGISTRY = {
        "91-4829-1029-4820": {
            "abha_id": "91-4829-1029-4820",
            "abha_address": "robert.chen@abdm",
            "name": "Robert Chen",
            "gender": "M",
            "year_of_birth": 1958,
            "district": "Kancheepuram",
            "state": "Tamil Nadu",
            "hip_id": "TN-KANCHI-GH-001",
            "consent_status": "GRANTED",
            "chronic_conditions": ["Type 2 Diabetes Mellitus", "Essential Hypertension", "Dyslipidemia", "Osteoarthritis"]
        },
        "91-7392-8192-3019": {
            "abha_id": "91-7392-8192-3019",
            "abha_address": "eleanor.vance@abdm",
            "name": "Eleanor Vance",
            "gender": "F",
            "year_of_birth": 1952,
            "district": "Chennai",
            "state": "Tamil Nadu",
            "hip_id": "TN-CHENNAI-MMC-004",
            "consent_status": "GRANTED",
            "chronic_conditions": ["Heart Failure with Reduced Ejection Fraction", "Chronic Kidney Disease Stage 3b", "Hypertension"]
        }
    }

    def __init__(self):
        self.gateway_status = "ACTIVE_SANDBOX"
        self.facility_id = "TN-KANCHI-CLINIC-A01"
        self.nha_version = "ABDM-v3.0.0"

    def verify_abha_id(self, abha_identifier: str) -> Dict[str, Any]:
        """
        Validates ABHA Number (14-digit) or ABHA Address (@abdm).
        Returns verified patient demographics and HIP consent tokens.
        """
        clean_id = abha_identifier.strip()
        
        # Match from registry
        for abha_num, profile in self.SAMPLE_ABHA_REGISTRY.items():
            if clean_id == abha_num or clean_id.lower() == profile["abha_address"].lower() or clean_id.lower() in profile["name"].lower():
                return {
                    "status": "VERIFIED",
                    "abha_number": profile["abha_id"],
                    "abha_address": profile["abha_address"],
                    "patient_name": profile["name"],
                    "gender": profile["gender"],
                    "state": profile["state"],
                    "district": profile["district"],
                    "hip_facility": profile["hip_id"],
                    "consent_token": f"ABDM-CONSENT-{uuid.uuid4().hex[:12].upper()}",
                    "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "chronic_conditions": profile["chronic_conditions"]
                }

        # Generated valid fallback for any new ABHA format
        if re.match(r"^\d{2}-\d{4}-\d{4}-\d{4}$", clean_id) or "@" in clean_id:
            return {
                "status": "VERIFIED",
                "abha_number": clean_id if "@" not in clean_id else "91-9988-7766-5544",
                "abha_address": clean_id if "@" in clean_id else f"user_{clean_id[-4:]}@abdm",
                "patient_name": "Outpatient MCC Patient",
                "gender": "M",
                "state": "Tamil Nadu",
                "district": "Kancheepuram",
                "hip_facility": self.facility_id,
                "consent_token": f"ABDM-CONSENT-{uuid.uuid4().hex[:12].upper()}",
                "verified_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "chronic_conditions": ["Hypertension", "Type 2 Diabetes"]
            }

        return {
            "status": "NOT_FOUND",
            "error": f"ABHA identifier '{clean_id}' not found in NHA sandbox registry. Try 'robert.chen@abdm' or '91-4829-1029-4820'."
        }

    def export_abdm_fhir_bundle(self, patient: Patient, care_bundle_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an ABDM M3-compliant FHIR R4 Bundle for Health Document Exchange.
        """
        bundle_id = f"ABDM-BUNDLE-{uuid.uuid4().hex[:8]}"
        return {
            "resourceType": "Bundle",
            "id": bundle_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/CareContextBundle"]
            },
            "type": "document",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "entry": [
                {
                    "fullUrl": f"urn:uuid:patient-{patient.id}",
                    "resource": {
                        "resourceType": "Patient",
                        "id": patient.id,
                        "identifier": [
                            {"system": "https://healthid.ndhm.gov.in", "value": "91-4829-1029-4820"},
                            {"system": "https://hospital.org/mrn", "value": patient.mrn}
                        ],
                        "name": [{"text": patient.name}],
                        "gender": "male" if patient.gender.lower().startswith("m") else "female"
                    }
                },
                {
                    "fullUrl": f"urn:uuid:cds-{care_bundle_dict.get('id', 'BND-01')}",
                    "resource": {
                        "resourceType": "CarePlan",
                        "id": care_bundle_dict.get("id", "BND-01"),
                        "status": "active",
                        "intent": "plan",
                        "title": care_bundle_dict.get("title", "MCC Care Plan"),
                        "description": care_bundle_dict.get("clinical_rationale", ""),
                        "supportingInfo": [{"display": care_bundle_dict.get("evidence_citation", "")}]
                    }
                }
            ]
        }
