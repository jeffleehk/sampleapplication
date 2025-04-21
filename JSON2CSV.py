from typing import List
from pydantic import BaseModel
import pandas as pd
import json
import os


class BankAccount(BaseModel):
    account_number: str
    balance: float
    owner: str


def read_bank_accounts_from_json(json_file_path: str) -> List[BankAccount]:
    accounts = []
    with open(json_file_path, "r") as f:
        for line in f:
            account = BankAccount(**json.loads(line))
            accounts.append(account)
    return accounts


def write_bank_accounts_to_csv(accounts: List[BankAccount], csv_file_path: str, chunk_size: int = 1000000):
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
    for i in range(0, len(accounts), chunk_size):
        chunk = accounts[i:i+chunk_size]
        df = pd.DataFrame([account.dict() for account in chunk])
        with open(csv_file_path, 'a') as f:
            df.to_csv(f, header=f.tell()==0, index=False)


if __name__ == "__main__":
    accounts = read_bank_accounts_from_json("bank_accounts.json")
    write_bank_accounts_to_csv(accounts, "bank_accounts.csv")