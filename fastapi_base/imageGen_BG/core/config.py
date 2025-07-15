import yaml
from typing import Dict, Any
from pathlib import Path

class Settings:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self, path: str = "imageGen_BG/core/config.yaml") -> Dict[str, Any]:
        config_path = Path(path)
        if not config_path.exists():
            config_path = "imageGen_BG/core/config.yaml"
        
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

settings = Settings()