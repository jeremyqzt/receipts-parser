
from receiptparser.config import read_config
from receiptparser.parser import process_receipt

config = read_config('./config/config.yml')
receipt = process_receipt(config, "testImages/test.jpeg", out_dir=None, verbosity=0)

print("Filename:   ", receipt.filename)
print("Company:    ", receipt.company)
print("Postal code:", receipt.postal)
print("Date:       ", receipt.date)
print("Amount:     ", receipt.sum)
print(receipt.__dict__)