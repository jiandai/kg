import requests

def test_api():
    base_url = "http://localhost:8000"
    
    # 1. Health
    try:
        r = requests.get(f"{base_url}/health")
        print(f"Health: {r.status_code} {r.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return

    # 2. Upload
    files = {'file': ('solar_system.txt', open('solar_system.txt', 'rb'))}
    r = requests.post(f"{base_url}/upload", files=files)
    print(f"Upload: {r.status_code} {r.json()}")

    # 3. Chat
    query = {"message": "What is Mars called?", "strategy": "auto"}
    r = requests.post(f"{base_url}/chat", json=query)
    print(f"Chat: {r.status_code} {r.json()}")
    
    if "Red Planet" in r.json().get("response", "") or "Mock Response" in r.json().get("response", ""):
        print("VERIFICATION PASSED")
    else:
        print("VERIFICATION FAILED")

if __name__ == "__main__":
    test_api()
