import requests
import sys
import time

def test_health():
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200 and response.json()["status"] == "ok":
            print("✅ Health check endpoint working")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_lookup():
    try:
        word = "hello"
        response = requests.get(f"http://localhost:8000/lookup/{word}")
        if response.status_code == 200 and isinstance(response.json(), list):
            data = response.json()
            if len(data) > 0 and data[0].get("word") == word:
                print(f"✅ Lookup endpoint working for word '{word}'")
                return True
        print(f"❌ Lookup failed: {response.status_code} - {response.text}")
        return False
    except Exception as e:
        print(f"❌ Lookup error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Dictionary API endpoints...")
    print("Make sure the API is running (python run.py)")
    
    # Wait a moment for the server to start if needed
    time.sleep(1)
    
    health_ok = test_health()
    lookup_ok = test_lookup()
    
    if health_ok and lookup_ok:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1) 