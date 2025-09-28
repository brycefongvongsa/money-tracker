import os
import pandas as pd
import utils.file_processing as fp
import utils.transaction_parsing as tp
 

def main():
  # Get all files
  print("Beginning to load files")
  pdf_files = []
  amex_files = []
  
  for file in os.listdir("files/"):
    if file.endswith(".pdf"):
      print(f"Found file: {file}")
      pdf_files.append(f"files/{file}")
    if file.endswith(".csv") and fp.get_credit_type(file) == "American Express":
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
    md_text = fp.pdf_to_md(pdf_file)
    
    # Get the list of transactions
    transaction_lines = tp.get_transaction_list(md_text, pdf_file)
    
    # Extract details from each transaction
    for t in transaction_lines:
      t_details = tp.get_transaction_details_pdf(t['content'], pdf_file)
      if t_details:
        pdf_transactions.append(t_details)
  
  ## Amex processing
  for csv_file in amex_files:
    print(f"Processing: {csv_file}")
    amex_transactions.extend(tp.get_transaction_details_csv(csv_file))
  
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