import argparse
from src.tax_engine import compute_company_income_tax

def main():
    parser = argparse.ArgumentParser(description="Sentient Tax - Compute Company Income Tax")
    parser.add_argument("--profit", type=float, required=True, help="Profit before tax")
    parser.add_argument("--allowance", type=float, required=True, help="Capital allowance")
    parser.add_argument("--loss", type=float, required=True, help="Loss brought forward")

    args = parser.parse_args()
    result = compute_company_income_tax(args.profit, args.allowance, args.loss)
    
    print("\n=== Sentient Tax Result ===")
    for k, v in result.items():
        if isinstance(v, (int, float)): # if it's a number, format with commas
            print(f"{k}: {v:,}")

        else: # if it's something else (like a text or dict)
            print (f"{k}: {v}")

if __name__ == "__main__":
    main()
