import gradio as gr
from src.tax_engine import compute_company_income_tax

def run(profit, ca, loss, rate):
    result = compute_company_income_tax(profit, ca, loss, rate)
    explanation = f"Taxable profit: {result['line_items']['taxable_profit']}, Tax payable: {result['tax_payable']}"
    return result, explanation

demo = gr.Interface(
    fn=run,
    inputs=[
        gr.Number(label="Profit before tax", value=10000000),
        gr.Number(label="Capital allowance", value=0),
        gr.Number(label="Loss b/f", value=0),
        gr.Number(label="Statutory rate (decimal)", value=0.30)
    ],
    outputs=[gr.JSON(label="Computation"), gr.Textbox(label="Explanation")],
    title="Sentient Tax (MVP)"
)

if __name__ == "__main__":
    demo.launch()
