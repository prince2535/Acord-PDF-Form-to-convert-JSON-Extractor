#!/usr/bin/env python3
"""
Test script for the PDF to JSON Extractor API
"""
import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    print("Testing user registration...")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "company": "Test Company"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_auth_endpoint(token):
    """Test authenticated endpoint"""
    print("\nTesting authenticated endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/test-auth/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_pdf_upload(token):
    """Test PDF upload (without actual file)"""
    print("\nTesting PDF upload endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test without file first
    response = requests.post(f"{BASE_URL}/acord/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("=== PDF to JSON Extractor API Test ===\n")
    
    # Test registration
    register_result = test_register()
    
    # Test login
    login_result = test_login()
    
    if login_result and 'tokens' in login_result:
        token = login_result['tokens']['access']
        print(f"\nGot access token: {token[:20]}...")
        
        # Test authenticated endpoint
        test_auth_endpoint(token)
        
        # Test PDF upload endpoint
        test_pdf_upload(token)
    else:
        print("Login failed, cannot test authenticated endpoints")










