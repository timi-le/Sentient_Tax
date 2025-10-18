def compute_company_income_tax(profit_before_tax, capital_allowance=0.0, loss_bf=0.0, statutory_rate=0.30):
    """
    Returns dict with traceable values.
    """
    adjusted_profit = profit_before_tax - capital_allowance - loss_bf
    taxable = max(adjusted_profit, 0.0)
    tax = round(taxable * statutory_rate, 2)
    return {
        "inputs": {
            "profit_before_tax": profit_before_tax,
            "capital_allowance": capital_allowance,
            "loss_bf": loss_bf,
            "statutory_rate": statutory_rate
        },
        "line_items": {
            "adjusted_profit": round(adjusted_profit, 2),
            "taxable_profit": round(taxable, 2),
            "tax_before_reliefs": tax
        },
        "tax_payable": tax
    }
