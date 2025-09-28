import re
import csv
import utils.file_processing as fp

# Parse the markdown file to return a list of transactions
def get_transaction_list(md_text, file) -> list:
  lines = md_text.split('\n') # Use passed text instead of reading file
  
  transactions = []
  if fp.get_credit_type(file) == "Chase":
    for line in lines:
      line = line.strip()
      # Looks for lines that start with a date pattern (MM/DD)
      # Chase: "01/02 AMAZON MKTPL*XXXX Amzn.com/bill WA 10.12"
      if re.match(r'\d{2}/\d{2}\s', line):
        transactions.append({
          'content': line,
        })
  return transactions

def get_transaction_details_pdf(transaction_line, file) -> dict:
  parts = transaction_line.split()
  
  # Chase specific
  if fp.get_credit_type(file) == "Chase":
    date = parts[0]
    merchant_parts = parts[1:-1]
    merchant = ' '.join(merchant_parts)
    amount = parts[-1]
    
    return {
      'credit_type': 'Chase',
      'date': fp.format_date(date, file), # TODO: make this date in yyyy-mm-dd format
      'merchant': merchant,
      'amount': amount
    }
  
  return None

def get_transaction_details_csv(file) -> dict:
  transactions = []
  credit_type = fp.get_credit_type(file)
  
  with open(file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      transaction = {
        'credit_type': credit_type,
        'date': row['Date'],
        'merchant': row['Description'],
        'amount': row['Amount']
      }
      transactions.append(transaction)
  return transactions