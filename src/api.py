# src/api.py (important parts)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any
from src.tax_engine import compute_full_tax

app = FastAPI(title="Sentient Tax API")

class ComputePayload(BaseModel):
    # CIT fields (optional defaults)
    profit_before_tax: float
    capital_allowance: Optional[float] = 0.0
    loss_bf: Optional[float] = 0.0
    statutory_rate: Optional[float] = 0.30
    minimum_tax_rate: Optional[float] = 0.01
    add_other_levies: Optional[Dict[str, float]] = None
    opening_twdv: Optional[float] = 0.0
    additions: Optional[float] = 0.0
    disposals: Optional[float] = 0.0
    wear_and_tear_rate: Optional[float] = 0.20

    # PAYE section - optional
    paye: Optional[Dict[str, Any]] = None

@app.post("/compute")
def compute(payload: ComputePayload):
    cit_kwargs = {
        "profit_before_tax": payload.profit_before_tax,
        "capital_allowance": payload.capital_allowance,
        "loss_bf": payload.loss_bf,
        "statutory_rate": payload.statutory_rate,
        "minimum_tax_rate": payload.minimum_tax_rate,
        "add_other_levies": payload.add_other_levies,
        "opening_twdv": payload.opening_twdv,
        "additions": payload.additions,
        "disposals": payload.disposals,
        "wear_and_tear_rate": payload.wear_and_tear_rate
    }
    paye_kwargs = payload.paye if payload.paye else None
    result = compute_full_tax(cit_kwargs, paye_kwargs)
    return result
