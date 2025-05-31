import json
import os
from datetime import datetime


class StreamStatusManager:
    def __init__(self):
        self.status_file = os.path.join(os.path.dirname(__file__), "status.json")

    def get_last_status(self):
        try:
            with open(self.status_file, 'r') as f:
                data = json.load(f)
                return data.get('is_live', False), data.get('last_check')
        except (FileNotFoundError, json.JSONDecodeError):
            return False, None

    def save_status(self, is_live):
        data = {
            'is_live': is_live,
            'last_check': datetime.utcnow().isoformat()
        }
        with open(self.status_file, 'w') as f:
            json.dump(data, f)