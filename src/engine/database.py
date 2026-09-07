"""
Embedded Persistent Clinical Database for AegisCDS.
Stores FHIR Patients, Observations, Prescriptions, Raw Clinical Events,
Vetted Care Bundles, and the Medico-Legal Clinician Override Audit Trail.
Uses SQLite with thread-safe connection pooling and automatic schema initialization.
"""

import sqlite3
import json
import os
import time
from typing import List, Dict, Any, Optional

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
DB_PATH = os.path.join(DB_DIR, "aegis_clinic.db")

class ClinicalDatabase:
    """Manages SQLite storage for the outpatient MCC event vetting pipeline."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self):
        """Initializes tables for clinical events, vetted bundles, and audit trails."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Patients Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    mrn TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    conditions_json TEXT NOT NULL,
                    encounter_type TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            # 2. Observations (Labs & Vitals)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS observations (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    code TEXT NOT NULL,
                    display TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    reference_range TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            # 3. Prescriptions (Active Medications)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    medication_code TEXT,
                    medication_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    dose TEXT,
                    frequency TEXT,
                    started_at TEXT,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            # 4. Raw Clinical Events Stream
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw_clinical_events (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    raw_payload_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            # 5. Vetted Care Bundles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vetted_care_bundles (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    category_summary TEXT,
                    consolidated_alert_ids_json TEXT NOT NULL,
                    clinical_rationale TEXT NOT NULL,
                    evidence_citation TEXT NOT NULL,
                    suggested_orders_json TEXT NOT NULL,
                    vetting_stage_reached TEXT NOT NULL,
                    is_critical_bypass INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'AWAITING_HUMAN_APPROVAL',
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            # 6. Override Audit Trail
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS override_audit_trail (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    bundle_or_alert_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    clinician_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    override_reason TEXT,
                    clinical_justification TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            conn.commit()

    def insert_patient(self, patient_data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO patients (id, mrn, name, age, gender, conditions_json, encounter_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                patient_data["id"],
                patient_data["mrn"],
                patient_data["name"],
                patient_data["age"],
                patient_data["gender"],
                json.dumps(patient_data["conditions"]),
                patient_data.get("encounter_type", "Outpatient Consultation"),
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            ))
            conn.commit()

    def insert_observation(self, patient_id: str, obs_data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO observations (id, patient_id, code, display, value, unit, reference_range, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                obs_data["id"],
                patient_id,
                obs_data["code"],
                obs_data["display"],
                obs_data["value"],
                obs_data["unit"],
                obs_data.get("reference_range", ""),
                obs_data["timestamp"]
            ))
            conn.commit()

    def insert_prescription(self, patient_id: str, med_data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO prescriptions (id, patient_id, medication_code, medication_name, category, dose, frequency, started_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                med_data["id"],
                patient_id,
                med_data.get("medication_code", ""),
                med_data["medication_name"],
                med_data.get("category", "GENERAL"),
                med_data.get("dose", ""),
                med_data.get("frequency", ""),
                med_data.get("started_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())),
                med_data.get("status", "active")
            ))
            conn.commit()

    def record_raw_event(self, event_id: str, patient_id: str, event_type: str, title: str, payload: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO raw_clinical_events (id, patient_id, event_type, title, raw_payload_json, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                patient_id,
                event_type,
                title,
                json.dumps(payload),
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            ))
            conn.commit()

    def record_vetted_bundle(self, bundle: Dict[str, Any], vetting_stage: str, is_critical_bypass: bool = False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO vetted_care_bundles 
                (id, patient_id, title, priority, category_summary, consolidated_alert_ids_json, clinical_rationale, evidence_citation, suggested_orders_json, vetting_stage_reached, is_critical_bypass, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                bundle["id"],
                bundle["patient_id"],
                bundle["title"],
                bundle["priority"],
                bundle.get("category_summary", ""),
                json.dumps(bundle.get("consolidated_alert_ids", [])),
                bundle["clinical_rationale"],
                bundle["evidence_citation"],
                json.dumps(bundle.get("suggested_orders", [])),
                vetting_stage,
                1 if is_critical_bypass else 0,
                bundle.get("status", "AWAITING_HUMAN_APPROVAL"),
                bundle.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            ))
            conn.commit()

    def record_audit_override(self, audit_data: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO override_audit_trail 
                (id, session_id, bundle_or_alert_id, patient_id, clinician_id, action, override_reason, clinical_justification, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                audit_data["id"],
                audit_data.get("session_id", "N/A"),
                audit_data["bundle_or_alert_id"],
                audit_data["patient_id"],
                audit_data.get("clinician_id", "DR-SARATHI-MD"),
                audit_data["action"],
                audit_data.get("override_reason", ""),
                audit_data.get("clinical_justification", ""),
                audit_data.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            ))
            conn.commit()

    def get_db_stats(self) -> Dict[str, int]:
        """Returns row counts across all clinical tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            stats = {}
            for table in ["patients", "observations", "prescriptions", "raw_clinical_events", "vetted_care_bundles", "override_audit_trail"]:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            return stats
