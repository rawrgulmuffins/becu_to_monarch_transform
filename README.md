# becu_to_monarch_transform
Python script used to turn BECU CSV transactions into a CSV that Monarch.com can import

# Example Run
```
python format_bank_statements.py --transaction-file-name ~/Downloads/2022_12_11.csv --account-name "BECU Credit Card"
```

# Arguments
```
Usage: format_bank_statements.py [OPTIONS]

Options:
  --transaction-file-name FILENAME
                                  [required]
  --account-name TEXT             [required]
  --output-file FILENAME          [default: monarch_transactions.csv]
  --help                          Show this message and exit.
```

# Example Input File
```
"Date","No.","Description","Debit","Credit"
"8/16/2022","","Interest Charge on Purchases","","0.00"
"8/16/2022","","Interest Charge on Cash Advances","","0.00"
"8/16/2022","","BEGINNING CASH BACK BALANCE                         $30.45","","0.00"
"8/16/2022","","CASH BACK EARNED THIS CYCLE                         $34.71","","0.00"
"8/16/2022","","CASH BACK REDEEMED THIS CYCLE                       $42.27","","0.00"
"8/16/2022","","ENDING CASH BACK BALANCE                            $22.89","","0.00"
"8/12/2022","","Example  xxx-xxx-xxxx NY","58.87",""
"8/10/2022","","PAYMENT - THANK YOU","","-218.51"
```

# Example Output File
```
date,merchant,category,account,origin_statement,notes,amount
2022-12-11 00:00:00,Example cleaning supplies,Cleaning Supplies,BECU Credit Card,Example Cleaning Supplies,,-75.72
2022-12-09 00:00:00,PAYMENT - THANK YOU,Credit Card Payment,BECU Credit Card,PAYMENT - THANK YOU,,22.57
```
