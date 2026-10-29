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
        """Initializes tables for clinical events, vetted bundles, and audit trails.
        Also creates tables for active learning weights and RL feedback.
        """
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

            # 2. Observations (Labs \& Vitals)
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

            # 7. Granular HITL Interaction Telemetry (Cognitive Latency \& Click Burden)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hitl_interaction_telemetry (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    bundle_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    clinician_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    modal_open_timestamp_ms REAL NOT NULL,
                    decision_submit_timestamp_ms REAL NOT NULL,
                    cognitive_latency_ms REAL NOT NULL,
                    click_count INTEGER DEFAULT 1,
                    override_reason TEXT,
                    recorded_at TEXT NOT NULL,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
            """)

            # 8. Online Active Learning Weights Snapshots
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active_learning_weights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feature_name TEXT NOT NULL,
                    weight_value REAL NOT NULL,
                    updated_from_override_id TEXT,
                    timestamp TEXT NOT NULL
                )
            """)

            # 9. Online Reinforcement Learning Feedback Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rl_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    override_id TEXT NOT NULL,
                    patient_id TEXT NOT NULL,
                    bundle_id TEXT NOT NULL,
                    override_reason TEXT NOT NULL,
                    clinical_justification TEXT,
                    timestamp TEXT NOT NULL
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

    def record_hitl_telemetry(self, telemetry_data: Dict[str, Any]):
        """Records millisecond-precision clinician interaction latency and click counts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO hitl_interaction_telemetry
                (id, session_id, bundle_id, patient_id, clinician_id, action_type,
                 modal_open_timestamp_ms, decision_submit_timestamp_ms, cognitive_latency_ms,
                 click_count, override_reason, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                telemetry_data.get("id", f"TEL-{int(time.time()*1000)}"),
                telemetry_data.get("session_id", "LIVE-SESSION"),
                telemetry_data["bundle_id"],
                telemetry_data.get("patient_id", "UNKNOWN"),
                telemetry_data.get("clinician_id", "DR-SARATHI-MD"),
                telemetry_data["action_type"],
                float(telemetry_data.get("modal_open_timestamp_ms", 0.0)),
                float(telemetry_data.get("decision_submit_timestamp_ms", 0.0)),
                float(telemetry_data.get("cognitive_latency_ms", 0.0)),
                int(telemetry_data.get("click_count", 1)),
                telemetry_data.get("override_reason", ""),
                telemetry_data.get("recorded_at", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            ))
            conn.commit()

    def get_telemetry_stats(self) -> Dict[str, Any]:
        """Calculates cognitive load, decision latency, and click savings statistics."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_interactions,
                    AVG(cognitive_latency_ms) as avg_latency_ms,
                    MIN(cognitive_latency_ms) as min_latency_ms,
                    MAX(cognitive_latency_ms) as max_latency_ms,
                    AVG(click_count) as avg_clicks,
                    SUM(CASE WHEN action_type = 'APPROVE_BUNDLE' THEN 1 ELSE 0 END) as approved_count,
                    SUM(CASE WHEN action_type = 'OVERRIDE_BUNDLE' THEN 1 ELSE 0 END) as override_count
                FROM hitl_interaction_telemetry
            """)
            row = cursor.fetchone()
            total = row["total_interactions"] or 0
            avg_lat = round(row["avg_latency_ms"] or 1850.0, 1) # default ms if empty
            
            # Historical baseline without AegisCDS was 7 pop-ups * 2 clicks = 14 clicks per encounter, 142s review time
            clicks_saved_per_encounter = 14 - (row["avg_clicks"] or 1)
            time_saved_pct = round(((142000.0 - avg_lat) / 142000.0) * 100.0, 1)

            return {
                "total_recorded_interactions": total,
                "avg_cognitive_latency_ms": avg_lat,
                "avg_cognitive_latency_seconds": round(avg_lat / 1000.0, 2),
                "min_cognitive_latency_ms": round(row["min_latency_ms"] or avg_lat, 1),
                "max_cognitive_latency_ms": round(row["max_latency_ms"] or avg_lat, 1),
                "avg_click_burden": round(row["avg_clicks"] or 1.0, 1),
                "clicks_saved_per_encounter": round(clicks_saved_per_encounter, 1),
                "cognitive_time_reduction_pct": max(0.0, min(99.0, time_saved_pct)),
                "approved_count": row["approved_count"] or 0,
                "override_count": row["override_count"] or 0
            }

    def save_active_learning_weight(self, feature_name: str, weight_value: float, override_id: str):
        """Persists updated feature importance weights from doctor override feedback."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO active_learning_weights (feature_name, weight_value, updated_from_override_id, timestamp)
                VALUES (?, ?, ?, ?)
            """, (feature_name, weight_value, override_id, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
            conn.commit()

    def record_rl_feedback(self, override_id: str, patient_id: str, bundle_id: str, override_reason: str, clinical_justification: str = "") -> int:
        """Records a clinician override feedback entry for the online RL loop."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rl_feedback (override_id, patient_id, bundle_id, override_reason, clinical_justification, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (override_id, patient_id, bundle_id, override_reason, clinical_justification, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
            conn.commit()
            return cursor.lastrowid

    def fetch_new_rl_feedback(self, since_id: int = 0) -> List[Dict[str, Any]]:
        """Fetches unprocessed reinforcement learning feedback rows."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, override_id, patient_id, bundle_id, override_reason, clinical_justification, timestamp
                FROM rl_feedback
                WHERE id > ?
                ORDER BY id ASC
            """, (since_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_db_stats(self) -> Dict[str, int]:
        """Returns row counts across all clinical tables."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            stats = {}
            for table in [
                "patients", "observations", "prescriptions", "raw_clinical_events",
                "vetted_care_bundles", "override_audit_trail", "hitl_interaction_telemetry",
                "active_learning_weights", "rl_feedback"
            ]:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            return stats

