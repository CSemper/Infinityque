'''Cleans most recent cafe transactions data file.

TODO
- Currently just prints objects, need to save to Redshift Database.
- Basket and Transaction objects not yet linked
'''

from src.data_handling import find_last_csv_name, read_s3_csv, \
                              to_raw_transactions, \
                              to_clean_transactions

# Read latest cafe transactions csv
last_file = find_last_csv_name(bucket='cafe-transactions')
data = read_s3_csv(bucket='cafe-transactions', key=last_file)
# Clean data and print
raw_transactions = to_raw_transactions(data)
clean_transactions = to_clean_transactions(raw_transactions)
for transaction in clean_transactions:
    print(transaction)