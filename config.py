import json

class Config:
    CONFIG_FILE = 'data.json'

    @staticmethod
    def get_font() -> str:
        """Чтение ключей из JSON-файла"""
        try:
            with open(Config.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                return config_data.get('font', {})
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def get_keys() -> dict:
        """Чтение ключей из JSON-файла"""
        try:
            with open(Config.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                return config_data.get('keys', {})
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return {}

    @staticmethod
    def set_keys(new_keys) -> bool:
        """Обновление ключей в JSON-файле"""
        try:
            with open(Config.CONFIG_FILE, 'r') as f:
                config_data = json.load(f)

            if 'keys' in config_data:
                config_data['keys'].update(new_keys)
            else:
                config_data['keys'] = new_keys

            with open(Config.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error updating keys: {e}")
            return False
