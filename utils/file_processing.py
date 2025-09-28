import os
import re
import pathlib
import pymupdf4llm


# Turn the pdf into a markdown file
def pdf_to_md(pdf_path):
  md_text = pymupdf4llm.to_markdown(pdf_path)
  pathlib.Path("results/output.md").write_bytes(md_text.encode())
  return md_text

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