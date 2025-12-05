import requests
import json
import time

class ServerCommunicator:
    def __init__(self, server_url="http://localhost:8000"):
        self.base_url = server_url
        self.session_id = f"sess_{int(time.time())}"
        
    def send_telemetry(self, data: dict):
        url = f"{self.base_url}/api/v1/telemetry/{self.session_id}"
        try:
            # Clean data for JSON serialization (handle sets, etc)
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Connection Failed: {e}")
            return None