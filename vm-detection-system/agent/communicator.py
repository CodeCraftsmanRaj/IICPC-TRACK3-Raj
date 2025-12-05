import requests
import json
import time
import socket

class ServerCommunicator:
    def __init__(self, server_url="http://localhost:8000"):
        self.base_url = server_url
        # Use hostname + timestamp to create a persistent ID for this run
        self.hostname = socket.gethostname()
        self.session_id = f"USER-{self.hostname}-{int(time.time())}"
        
    def send_telemetry(self, data: dict):
        url = f"{self.base_url}/api/v1/telemetry/{self.session_id}"
        try:
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                # print(f"Server Error: {response.text}") # Debug
                return None
        except Exception as e:
            # print(f"Connection Failed: {e}") # Debug
            return None