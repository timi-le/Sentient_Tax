from fastapi import FastAPI
from src.tax_engine import compute_company_income_tax

app = FastAPI(title="Sentient Tax API")

@app.get("/compute")
def compute(profit_before_tax: float, capital_allowance: float, loss_bf: float):
    result = compute_company_income_tax(profit_before_tax, capital_allowance, loss_bf)
    return result
