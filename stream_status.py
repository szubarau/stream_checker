import json
import os
from datetime import datetime


class StreamStatusManager:
    """Класс для управления статусом стрима"""

    def __init__(self):
        self.status_file = os.path.join(
            os.path.dirname(__file__),
            "status.json"
        )

    def get_last_status(self):
        """Получение последнего статуса"""
        try:
            with open(self.status_file, 'r') as f:
                data = json.load(f)
                return data.get('is_live', False)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def save_status(self, is_live):
        """Сохранение текущего статуса"""
        data = {
            'is_live': is_live,
            'last_checked': datetime.utcnow().isoformat()
        }
        with open(self.status_file, 'w') as f:
            json.dump(data, f, indent=2)