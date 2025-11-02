import gradio as gr
from src.tax_engine import compute_company_income_tax

def tax_interface(profit, allowance, loss):
    try:
        profit = float(profit)
        allowance = float(allowance)
        loss = float(loss)

        result = compute_company_income_tax(profit, allowance, loss)

        # Extract values correctly from nested structure
        line_items = result.get("line_items", {})
        adjusted = line_items.get("adjusted_profit", "N/A")
        taxable = line_items.get("taxable_profit", "N/A")
        cit = result.get("tax_payable", "N/A")

        # Format numbers for display
        adjusted = f"{adjusted:,.2f}" if isinstance(adjusted, (int, float)) else adjusted
        taxable = f"{taxable:,.2f}" if isinstance(taxable, (int, float)) else taxable
        cit = f"{cit:,.2f}" if isinstance(cit, (int, float)) else cit

        return f"""
        ✅ **Adjusted Profit:** {adjusted}
        ✅ **Taxable Profit:** {taxable}
        💰 **Company Income Tax (30%):** {cit}
        """
    except Exception as e:
        return f"❌ Error: {e}"

ui = gr.Interface(
    fn=tax_interface,
    inputs=[
        gr.Number(label="Profit Before Tax"),
        gr.Number(label="Capital Allowance"),
        gr.Number(label="Loss Brought Forward")
    ],
    outputs="markdown",
    title="🧮 Sentient Tax Engine",
    description="Compute Nigerian Company Income Tax (CIT) easily with Sentient Tax."
)

if __name__ == "__main__":
    ui.launch()
