from src.tax_engine import compute_company_income_tax

def test_basic():
    out = compute_company_income_tax(10000000, capital_allowance=2000000, loss_bf=1000000, statutory_rate=0.30)
    assert out["line_items"]["adjusted_profit"] == 7000000
    assert out["tax_payable"] == 2100000.0
