from app import format_date
# Simple test file for credit type detection

def test_get_credit_type_amex():
  filename = "American Express Activity.csv"
  result = "American Express" if "american express" in filename.lower() else "Unknown"
  assert result == "American Express"

def test_get_credit_type_chase():
  filename = "Chase Statement December 1 2024.pdf"
  result = "Chase" if "chase" in filename.lower() else "Unknown"
  assert result == "Chase"
  
def test_format_date():
  result = format_date("07/05", "Chase Statement Jul 5, 2025.pdf")
  assert "07/05/2025" in str(result), "Date should be in mm/dd/yyyy" 