import pandas as pd
from collections import deque

class FinancialAuditor:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        
    def run_fifo_audit(self) -> float:
        portfolios = {}
        counts = {}
        net_states = {}
        total_gross_profit = 0
        total_fees = 0

        for _, row in self.df.iterrows():
            p_id = row['portfolio_id']
            txn_id = row['txn_id']
            val = row['quantity'] * row['unit_price']
            
            counts[p_id] = counts.get(p_id, 0) + 1
            fee_rate = 0.005 * (0.6 if counts[p_id] >= 5 else 1.0)
            current_fee = val * fee_rate
            
            net_states[p_id] = net_states.get(p_id, 0) - current_fee
            total_fees += current_fee

            if row['type'] == 1:
                if p_id not in portfolios: portfolios[p_id] = deque()
                for _ in range(int(row['quantity'])):
                    portfolios[p_id].append((row['unit_price'], txn_id))
            else:
                success_tax = net_states.get(p_id, 0) > 50.0
                txn_profit = 0
                for _ in range(int(row['quantity'])):
                    buy_p, buy_id = portfolios[p_id].popleft()
                    unit_p = (row['unit_price'] - buy_p)
                    if (txn_id - buy_id) > 6: unit_p *= 0.93
                    if success_tax: unit_p *= 0.98
                    txn_profit += unit_p
                
                total_gross_profit += txn_profit
                net_states[p_id] += txn_profit

        return round(total_gross_profit - total_fees, 2)
