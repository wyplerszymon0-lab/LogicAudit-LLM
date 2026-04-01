import pytest
import pandas as pd
from src.auditor import FinancialAuditor

@pytest.fixture
def sample_csv(tmp_path):
    d = tmp_path / "test_data"
    d.mkdir()
    file_path = d / "test.csv"
    data = {
        'txn_id': [1, 2],
        'portfolio_id': [100, 100],
        'type': [1, 2],
        'quantity': [10, 10],
        'unit_price': [100, 150]
    }
    pd.DataFrame(data).to_csv(file_path, index=False)
    return str(file_path)

def test_basic_logic(sample_csv):
    auditor = FinancialAuditor(sample_csv)
    assert auditor.run_fifo_audit() == 487.5

def test_loyalty_logic(tmp_path):
    f = tmp_path / "loyalty.csv"
    data = {
        'txn_id': [1, 2, 3, 4, 5],
        'portfolio_id': [1, 1, 1, 1, 1],
        'type': [1, 1, 1, 1, 1],
        'quantity': [1, 1, 1, 1, 1],
        'unit_price': [100, 100, 100, 100, 100]
    }
    pd.DataFrame(data).to_csv(f, index=False)
    auditor = FinancialAuditor(str(f))
    assert auditor.run_fifo_audit() == -2.3
