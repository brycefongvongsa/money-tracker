import pymupdf4llm
import pathlib
import re
import os
import csv
import pandas as pd
from datetime import datetime

# Turn the pdf into a markdown file
def pdf_to_md(pdf_path):
  md_text = pymupdf4llm.to_markdown(pdf_path)
  pathlib.Path("results/output.md").write_bytes(md_text.encode())
  return md_text


# Parse the markdown file to return a list of transactions
def get_transaction_list(md_text, file) -> list:
  lines = md_text.split('\n') # Use passed text instead of reading file
  
  transactions = []
  if get_credit_type(file) == "Chase":
    for line in lines:
      line = line.strip()
      # Looks for lines that start with a date pattern (MM/DD)
      # Chase: "01/02 AMAZON MKTPL*XXXX Amzn.com/bill WA 10.12"
      if re.match(r'\d{2}/\d{2}\s', line):
        transactions.append({
          'content': line,
        })
  return transactions


def get_credit_type(file: str) -> str:
  filename = os.path.basename(file)
  if "american express" in filename.lower():
    return "American Express"
  elif "chase" in filename.lower():
    return "Chase"
  else:
    return "Unknown"


def get_statement_year(file):
  filename = os.path.basename(file)
  match = re.search(r'\d{4}', filename)
  if match:
    return int(match.group())
  else:
    raise Exception(f"Failed to extract year, expected 4 digits from {filename}")


# Chase Statements only provides date in mm/dd, format it to mm/dd/yyyy
def format_date(date_string, file):
  statement_year = get_statement_year(file)
  new_date_string = f"{date_string}/{statement_year}"
  return new_date_string
  

def get_transaction_details_pdf(transaction_line, file) -> dict:
  parts = transaction_line.split()
  
  # Chase specific
  if get_credit_type(file) == "Chase":
    date = parts[0]
    merchant_parts = parts[1:-1]
    merchant = ' '.join(merchant_parts)
    amount = parts[-1]
    
    return {
      'credit_type': 'Chase',
      'date': format_date(date, file), # TODO: make this date in yyyy-mm-dd format
      'merchant': merchant,
      'amount': amount
    }
  
  return None

def get_transaction_details_csv(file) -> dict:
  transactions = []
  credit_type = get_credit_type(file)
  
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
 
 
def main():
  # Get all files
  print("Beginning to load files")
  pdf_files = []
  amex_files = []
  
  for file in os.listdir("files/"):
    if file.endswith(".pdf"):
      print(f"Found file: {file}")
      pdf_files.append(f"files/{file}")
    if file.endswith(".csv") and get_credit_type(file) == "American Express":
      print(f"Found file: {file}")
      amex_files.append(f"files/{file}")
  print("Finished loading files" + '\n' + '--------------')
  
  # Process all files and collect results
  print("Beginning processing step")
  pdf_transactions = []
  amex_transactions = []
  
  ## PDF processing
  for pdf_file in pdf_files:
    print(f"Processing: {pdf_file}")
    md_text = pdf_to_md(pdf_file)
    
    # Get the list of transactions
    transaction_lines = get_transaction_list(md_text, pdf_file)
    
    # Extract details from each transaction
    for t in transaction_lines:
      t_details = get_transaction_details_pdf(t['content'], pdf_file)
      if t_details:
        pdf_transactions.append(t_details)
  
  ## Amex processing
  for csv_file in amex_files:
    print(f"Processing: {csv_file}")
    amex_transactions.extend(get_transaction_details_csv(csv_file))
  
  print("Processing step completed for all transactions in the files" + '\n' + '--------------')
    
  
  # Combine transactions into a DataFrame
  print("Combining all transactions")
  all_transactions = pdf_transactions + amex_transactions
  df = pd.DataFrame(all_transactions)
  print("Combining step complete")
  
  # Transformation step
  print("Transforming data")
  # Convert to yyyy-mm-dd format.
  df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
  print("Transformation complete")
  
  # Save to CSV
  print("Saving to csv")
  df.to_csv('results/transactions.csv', index=False)
  print("Saving step complete")
  
  # Delete temporary outputs
  # print("Deleting temporary outputs")
  # os.remove("results/output.md")
  # print("Deletion step complete")
  
  
if __name__ == "__main__":
    main()