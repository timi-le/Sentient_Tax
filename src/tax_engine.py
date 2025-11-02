# src/tax_engine.py
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class CITInputs:
    profit_before_tax: float
    capital_allowance: float = 0.0
    loss_bf: float = 0.0
    statutory_rate: float = 0.30
    minimum_tax_rate: float = 0.01
    add_other_levies: Dict[str, float] = None
    opening_twdv: float = 0.0
    additions: float = 0.0
    disposals: float = 0.0
    wear_and_tear_rate: float = 0.20
    currency: str = "NGN"

def compute_adjusted_profit(inputs: CITInputs) -> float:
    return round(inputs.profit_before_tax - inputs.capital_allowance - inputs.loss_bf, 2)

def compute_taxable_profit(adjusted_profit: float) -> float:
    return round(max(adjusted_profit, 0.0), 2)

def compute_standard_cit(taxable_profit: float, statutory_rate: float) -> float:
    return round(taxable_profit * statutory_rate, 2)

def compute_minimum_tax(inputs: CITInputs) -> float:
    return round(max(inputs.profit_before_tax * inputs.minimum_tax_rate, 0.0), 2)

def compute_twdv(inputs: CITInputs) -> Dict[str, float]:
    before = inputs.opening_twdv + inputs.additions - inputs.disposals
    wear = round(before * inputs.wear_and_tear_rate, 2)
    closing = round(before - wear, 2)
    return {
        "opening_twdv": round(inputs.opening_twdv, 2),
        "additions": round(inputs.additions, 2),
        "disposals": round(inputs.disposals, 2),
        "wear_and_tear_rate": inputs.wear_and_tear_rate,
        "wear_and_tear_charge": wear,
        "closing_twdv": closing,
    }

def compute_other_levies(taxable_profit: float, levies: Dict[str, float] = None) -> Dict[str, float]:
    if not levies:
        return {}
    out = {}
    for k, v in levies.items():
        if isinstance(v, (int, float)) and 0 < v < 1:
            out[k] = round(taxable_profit * v, 2)
        else:
            out[k] = round(float(v), 2)
    return out

# ---- PAYE/PIT helper ----
@dataclass
class PayeInputs:
    gross_pay: float
    # list of bands in shape [(threshold, rate), ...] must be ordered ascending thresholds
    bands: List[Dict[str, float]] = None
    personal_relief: float = 0.0  # general relief to subtract from tax

def compute_paye(p: PayeInputs) -> Dict[str, Any]:
    """
    Generic progressive PAYE computation:
    bands example:
      [
        {"threshold": 300000, "rate": 0.07},
        {"threshold": 600000, "rate": 0.11},
        {"threshold": 1100000, "rate": 0.15},
        {"threshold": 1600000, "rate": 0.19},
        {"threshold": 3200000, "rate": 0.21},
        {"threshold": float('inf'), "rate": 0.24}
      ]
    This function slices gross_pay into band segments and calculates tax.
    """
    gross = max(0.0, float(p.gross_pay))
    bands = p.bands or []
    tax = 0.0
    remaining = gross
    last_threshold = 0.0
    detail = []
    for band in bands:
        thresh = float(band["threshold"])
        rate = float(band["rate"])
        band_amount = 0.0
        if thresh == float("inf"):
            band_amount = max(0.0, remaining)
        else:
            segment = min(remaining, thresh - last_threshold)
            band_amount = max(0.0, segment)
        band_tax = round(band_amount * rate, 2)
        detail.append({"band_up_to": thresh, "rate": rate, "taxable_amount": round(band_amount,2), "band_tax": band_tax})
        tax += band_tax
        remaining -= band_amount
        last_threshold = thresh
        if remaining <= 0:
            break
    tax_after_relief = round(max(0.0, tax - p.personal_relief), 2)
    return {
        "gross_pay": round(gross,2),
        "tax_before_relief": round(tax,2),
        "personal_relief": round(p.personal_relief,2),
        "tax_payable": tax_after_relief,
        "bands_detail": detail
    }

# ---- Full CIT coordinator that also computes PAYE when provided ----
def compute_full_tax(cit_kwargs: Dict[str, Any], paye_kwargs: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    cit_kwargs -> fields for CITInputs
    paye_kwargs -> fields for PayeInputs (optional)
    Returns structured dict containing cit, twdv, levies and paye sections.
    """
    cit_inp = CITInputs(**cit_kwargs)
    adj = compute_adjusted_profit(cit_inp)
    taxable = compute_taxable_profit(adj)
    standard = compute_standard_cit(taxable, cit_inp.statutory_rate)
    minimum = compute_minimum_tax(cit_inp)
    payable_before_levies = max(standard, minimum)
    levies = compute_other_levies(taxable, cit_inp.add_other_levies)
    total_levies = round(sum(levies.values()) if levies else 0.0,2)
    total_payable = round(payable_before_levies + total_levies, 2)
    twdv = compute_twdv(cit_inp)

    res = {
        "inputs": asdict(cit_inp),
        "line_items": {
            "adjusted_profit": adj,
            "taxable_profit": taxable,
            "standard_cit": standard,
            "minimum_tax": minimum,
            "tax_payable_before_levies": payable_before_levies
        },
        "twdv": twdv,
        "levies": levies,
        "totals": {
            "total_levies": total_levies,
            "total_tax_payable": total_payable
        }
    }

    if paye_kwargs:
        paye_inp = PayeInputs(**paye_kwargs)
        paye_res = compute_paye(paye_inp)
        res["paye"] = paye_res

    return res
