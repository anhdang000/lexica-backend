import os
import configparser
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from configuration file."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = configparser.ConfigParser()
        self.config_path = config_path or os.getenv('CONFIG_PATH', 'config.ini')
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or create from template if not exists."""
        if not os.path.exists(self.config_path):
            self._create_config_from_template()
        
        self.config.read(self.config_path)
    
    def _create_config_from_template(self) -> None:
        """Create configuration file from template if it doesn't exist."""
        template_path = 'config.template.ini'
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file {template_path} not found")
        
        with open(template_path, 'r') as template:
            with open(self.config_path, 'w') as config:
                config.write(template.read())
    
    @property
    def server_host(self) -> str:
        return self.config.get('server', 'host', fallback='0.0.0.0')
    
    @property
    def server_port(self) -> int:
        return self.config.getint('server', 'port', fallback=8000)
    
    @property
    def server_reload(self) -> bool:
        return self.config.getboolean('server', 'reload', fallback=True)
    
    @property
    def server_workers(self) -> int:
        return self.config.getint('server', 'workers', fallback=1)
    
    @property
    def dictionary_api_url(self) -> str:
        return self.config.get('dictionary_api', 'base_url', 
                             fallback='https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    
    @property
    def dictionary_api_timeout(self) -> int:
        return self.config.getint('dictionary_api', 'timeout', fallback=10)
    
    @property
    def dictionary_api_max_retries(self) -> int:
        return self.config.getint('dictionary_api', 'max_retries', fallback=3)
    
    @property
    def log_level(self) -> str:
        return self.config.get('logging', 'level', fallback='INFO')
    
    @property
    def log_format(self) -> str:
        return self.config.get('logging', 'format', 
                             fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    @property
    def log_file(self) -> str:
        return self.config.get('logging', 'file', fallback='app.log')
    
    @property
    def allowed_origins(self) -> str:
        return self.config.get('security', 'allowed_origins', fallback='*')
    
    @property
    def rate_limit(self) -> int:
        return self.config.getint('security', 'rate_limit', fallback=100)
    
    @property
    def rate_limit_period(self) -> int:
        return self.config.getint('security', 'rate_limit_period', fallback=60)

    @property
    def gemini_model_name(self) -> str:
        """Get the Gemini model name from the config."""
        return self.config.get('ai', 'gemini_model_name', fallback='gemini-2.0-flash')

    @property
    def api_keys(self) -> List[str]:
        """Get API keys as a list from the environment variable."""
        keys = os.getenv('GEMINI_MODEL_API_KEY', '')
        return [key.strip() for key in keys.split(',') if key.strip()]

# Create a global settings instance
settings = Settings()