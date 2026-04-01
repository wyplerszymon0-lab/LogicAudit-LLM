import pandas as pd
from src.auditor import FinancialAuditor
from src.llm_bridge import LLMBridge

def run_benchmark():
    CSV_PATH = "data/transactions.csv"
    PROMPT = "Calculate Adjusted Net Profit (ANP) using FIFO, 0.5% TT, 40% Loyalty discount, 7% Time Decay (>6 txns), and 2% Success Tax (>50 net)."

    auditor = FinancialAuditor(CSV_PATH)
    ground_truth = auditor.run_fifo_audit()
    
    with open(CSV_PATH, 'r') as f:
        csv_data = f.read()
    
    bridge = LLMBridge()
    llm_result = bridge.get_llm_calculation(PROMPT, csv_data)
    
    error = abs(ground_truth - llm_result)
    score = max(0.0, 1.0 - (error / 100.0))

    print(f"GT: {ground_truth} | LLM: {llm_result} | Score: {round(score, 3)}")

if __name__ == "__main__":
    run_benchmark()
