#!/usr/bin/env python3
"""
Test script for the PDF to JSON Extractor API with actual PDF upload
"""
import requests
import json
import os

BASE_URL = "http://localhost:8000"

def create_test_pdf():
    """Create a simple test PDF file"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "test_acord.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Add some test content that looks like an ACORD form
        c.drawString(100, 750, "ACORD 125 - Commercial Insurance Application")
        c.drawString(100, 720, "Business Name: Test Insurance Company")
        c.drawString(100, 690, "Contact: John Doe")
        c.drawString(100, 660, "Email: john@testcompany.com")
        c.drawString(100, 630, "Phone: 555-123-4567")
        c.drawString(100, 600, "Address: 123 Main St, Anytown, ST 12345")
        c.drawString(100, 570, "Business Type: Insurance Agency")
        c.drawString(100, 540, "Annual Revenue: $500,000")
        c.drawString(100, 510, "Number of Employees: 25")
        
        c.save()
        print(f"Created test PDF: {filename}")
        return filename
    except ImportError:
        print("ReportLab not available, creating a simple text file instead")
        filename = "test_acord.txt"
        with open(filename, 'w') as f:
            f.write("ACORD 125 - Commercial Insurance Application\n")
            f.write("Business Name: Test Insurance Company\n")
            f.write("Contact: John Doe\n")
            f.write("Email: john@testcompany.com\n")
            f.write("Phone: 555-123-4567\n")
            f.write("Address: 123 Main St, Anytown, ST 12345\n")
            f.write("Business Type: Insurance Agency\n")
            f.write("Annual Revenue: $500,000\n")
            f.write("Number of Employees: 25\n")
        return filename

def test_login():
    """Test user login"""
    print("Testing user login...")
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Login Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Login successful for user: {result['user']['username']}")
        return result['tokens']['access']
    else:
        print(f"Login failed: {response.json()}")
        return None

def test_pdf_upload(token, pdf_file):
    """Test PDF upload with actual file"""
    print(f"\nTesting PDF upload with file: {pdf_file}")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {'file': (pdf_file, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/acord/", headers=headers, files=files)
        
        print(f"Upload Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ PDF extraction successful!")
            print("Extracted JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ PDF extraction failed")
            
    except FileNotFoundError:
        print(f"❌ File {pdf_file} not found")
    except Exception as e:
        print(f"❌ Error during upload: {e}")

def test_user_profile(token):
    """Test user profile endpoint"""
    print("\nTesting user profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    print(f"Profile Status: {response.status_code}")
    print(f"Profile Response: {response.json()}")

def test_extraction_history(token):
    """Test extraction history endpoint"""
    print("\nTesting extraction history...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/extractions/", headers=headers)
    print(f"History Status: {response.status_code}")
    print(f"History Response: {response.json()}")

if __name__ == "__main__":
    print("=== PDF to JSON Extractor API Test with PDF Upload ===\n")
    
    # Create test PDF
    pdf_file = create_test_pdf()
    
    # Test login
    token = test_login()
    
    if token:
        print(f"\nGot access token: {token[:20]}...")
        
        # Test user profile
        test_user_profile(token)
        
        # Test PDF upload
        test_pdf_upload(token, pdf_file)
        
        # Test extraction history
        test_extraction_history(token)
        
        # Clean up
        if os.path.exists(pdf_file):
            os.remove(pdf_file)
            print(f"\nCleaned up test file: {pdf_file}")
    else:
        print("❌ Cannot proceed without authentication token")










