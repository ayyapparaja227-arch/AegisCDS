#!/usr/bin/env python3
"""Active Learning Daemon
Runs indefinitely, listening for clinician override feedback events and updating
the online learning engine weights.
In a production system this would be driven by a message queue (e.g., Redis,
Kafka). For this sandbox implementation we simulate a simple polling loop that
checks a SQLite table `rl_feedback` every 30 seconds.
"""
import time
import logging
from src.engine.active_learning_engine import ActiveOnlineLearningEngine
from src.engine.database import ClinicalDatabase

logging.basicConfig(level=logging.INFO, format="[RL Daemon] %(asctime)s %(levelname)s %(message)s")

def main() -> None:
    db = ClinicalDatabase()
    engine = ActiveOnlineLearningEngine(db)
    logging.info("Active Learning Daemon started – polling rl_feedback table.")
    last_processed_id = 0
    while True:
        rows = db.fetch_new_rl_feedback(since_id=last_processed_id)
        for row in rows:
            engine.process_clinician_feedback(
                override_id=row["override_id"],
                patient_id=row["patient_id"],
                bundle_id=row["bundle_id"],
                override_reason=row["override_reason"],
                clinical_justification=row.get("clinical_justification", ""),
            )
            last_processed_id = max(last_processed_id, row["id"])
            logging.info(f"Processed override {row['override_id']}, updated weights.")
        time.sleep(30)

if __name__ == "__main__":
    main()

