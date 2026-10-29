import fastapi
from fastapi import APIRouter, HTTPException
from src.engine.abdm_connector import ABDMConnector

router = APIRouter()

@router.get("/api/v1/abdm/consent/{abha_id}")
async def get_consent(abha_id: str):
    """Verify an ABHA ID and return a consent token.
    Returns a JSON payload with patient details and a temporary consent token.
    """
    connector = ABDMConnector()
    result = connector.verify_abha_id(abha_id)
    if result.get("status") != "VERIFIED":
        raise HTTPException(status_code=404, detail=result.get("error", "ABHA not found"))
    return result

