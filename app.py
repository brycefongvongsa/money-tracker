import pymupdf4llm
import pathlib
import re
import os
import pandas as pd
from datetime import datetime

# Turn the pdf into a markdown file
def process_bank_statement(pdf_path):
  md_text = pymupdf4llm.to_markdown(pdf_path)
  pathlib.Path("results/output.md").write_bytes(md_text.encode())
  return md_text

# Parse the markdown file, return a list of transaction strings
def parse_transactions(md_text):
  lines = md_text.split('\n') # Use passed text instead of reading file
  
  transactions = []
  for line in lines:
    line = line.strip()
    # Look for lines that start with a date pattern (MM/DD)
    # Chase: "01/02 AMAZON MKTPL*XXXX Amzn.com/bill WA 10.12"
    if re.match(r'\d{2}/\d{2}\s', line):
      transactions.append({
        'content': line,
      })
  return transactions

def parse_credit_type(md_text):
  lines = md_text.split('\n')
  
  credit_type = ""
  for line in lines:
    if re.search(r'chase\.com', line):
      credit_type = "Chase"
      break
  
  return credit_type

# Breakdown the details from the transaction
def extract_transaction_details(transaction_line, md_text):
  parts = transaction_line.split()
  
  if len(parts) >= 2:
    date = parts[0]
    merchant_parts = parts[1:-1]
    merchant = ' '.join(merchant_parts)
    amount = parts[-1]
    
    return {
      'credit_type': parse_credit_type(md_text),
      'date': date,
      'merchant': merchant,
      'amount': amount
    }
  
  return None
 
def main():
  # Get all PDF files
  pdf_files = []
  for file in os.listdir("files/"):
    if file.endswith(".pdf"):
      pdf_files.append(f"files/{file}")
  
  # Process all PDF files and collect results
  all_transactions = []
  
  for pdf_file in pdf_files:
    print(f"Processing: {pdf_file}")
    md_text = process_bank_statement(pdf_file)
    
    # Get the list of transactions
    transaction_lines = parse_transactions(md_text)
    
    # Extract details from each transaction
    for transaction in transaction_lines:
      details = extract_transaction_details(transaction['content'], md_text)
      if details:
        all_transactions.append(details)
  
  # Create DataFrame
  df = pd.DataFrame(all_transactions)
  
  # Display results
  print(df)
  
  # Save to CSV
  df.to_csv('results/transactions.csv', index=False)
  
  # Delete temporary outputs
  os.remove("results/output.md")
  
  
if __name__ == "__main__":
    main()