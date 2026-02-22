# Test script for User Microservice
# This script demonstrates how to interact with the API

import requests
import json

BASE_URL = "http://localhost:8001/api/v1"

def test_health():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get("http://localhost:8001/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePassword123",
        "first_name": "Test",
        "last_name": "User"
    }

    response = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201


def test_login(username="testuser", password="SecurePassword123"):
    """Test user login"""
    print("\n=== Testing User Login ===")
    login_data = {
        "identifier": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")

    if response.status_code == 200:
        return result.get("access_token")
    return None


def test_get_profile(token):
    """Test getting current user profile"""
    print("\n=== Testing Get Profile ===")
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def main():
    """Run all tests"""
    print("=" * 60)
    print("User Microservice API Tests")
    print("=" * 60)

    # Test 1: Health check
    if not test_health():
        print("\n❌ Service is not healthy!")
        return

    print("\n✅ Service is healthy!")

    # Test 2: Register user
    if test_register():
        print("\n✅ User registration successful!")
    else:
        print("\n⚠️  User might already exist, continuing...")

    # Test 3: Login
    token = test_login()
    if token:
        print("\n✅ Login successful!")

        # Test 4: Get profile
        if test_get_profile(token):
            print("\n✅ Profile retrieval successful!")
        else:
            print("\n❌ Profile retrieval failed!")
    else:
        print("\n❌ Login failed!")

    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the service.")
        print("Make sure the service is running on http://localhost:8001")
    except Exception as e:
        print(f"\n❌ Error: {e}")

