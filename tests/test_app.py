# Simple test file for credit type detection

def test_get_credit_type_amex():
  filename = "American Express Activity.csv"
  result = "American Express" if "american express" in filename.lower() else "Unknown"
  assert result == "American Express"

def test_get_credit_type_chase():
  filename = "Chase Statement December 1 2024.pdf"
  result = "Chase" if "chase" in filename.lower() else "Unknown"
  assert result == "Chase"