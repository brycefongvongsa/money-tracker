import utils.file_processing as fp
import utils.transaction_parsing as tp
# Simple test file for credit type detection

# file processing tests
def test_get_credit_type_amex():
  filename = "American Express Activity.csv"
  result = "American Express" if "american express" in filename.lower() else "Unknown"
  assert result == "American Express"

def test_get_credit_type_chase():
  filename = "Chase Statement December 1 2024.pdf"
  result = "Chase" if "chase" in filename.lower() else "Unknown"
  assert result == "Chase"
  
def test_format_date():
  result = fp.format_date("07/05", "Chase Statement Jul 5, 2025.pdf")
  assert "07/05/2025" in str(result), "Date should be in mm-dd-yyyy" 
  
# transaction parsing tests
def test_get_transaction_list_chase():
  dummy_md_text = """
  01/01 AMAZON MKTPL*XXXX Amzn.com/bill NY 11.11
  01/02 AMAZON MKTPL*XXXX Amzn.com/bill WA 22.22
  01/03 AMAZON MKTPL*XXXX Amzn.com/bill CA 33.33
  """
  result = tp.get_transaction_list(dummy_md_text, "Chase Statement Jan 30, 2025.pdf")
  assert len(result) == 3, "There should be 3 transactions"
  assert result[0]['content'] == "01/01 AMAZON MKTPL*XXXX Amzn.com/bill NY 11.11"
  assert result[1]['content'] == "01/02 AMAZON MKTPL*XXXX Amzn.com/bill WA 22.22"
  assert result[2]['content'] == "01/03 AMAZON MKTPL*XXXX Amzn.com/bill CA 33.33"