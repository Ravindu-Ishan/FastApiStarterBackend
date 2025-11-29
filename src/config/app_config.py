"""
Application Configuration Module
Reads configuration from deployment.toml and environment variables
Environment variables take precedence over TOML values

How to add new configuration settings:
1. Add the setting to deployment.toml under appropriate section:
   [section_name]
   setting_key = "default_value"

2. Add environment variable override in _override_from_env() method:
   self._config["section_name"]["setting_key"] = os.getenv("ENV_VAR_NAME", self._config["section_name"].get("setting_key"))

3. Add a convenience property (optional but recommended):
   @property
   def setting_key(self) -> str:
       '''Description of the setting'''
       return self.get("section_name", "setting_key", "default_value")

4. Document the environment variable in .env.example:
   ENV_VAR_NAME=default_value

Example:
   # In deployment.toml
   [application]
   api_timeout = 30

   # In _override_from_env()
   self._config["application"]["api_timeout"] = int(os.getenv("API_TIMEOUT", self._config["application"].get("api_timeout", 30)))

   # Property (optional)
   @property
   def api_timeout(self) -> int:
       return self.get("application", "api_timeout", 30)
"""

import os
import toml
from pathlib import Path
from typing import Any, Dict, List
from dotenv import load_dotenv


class AppConfig:
    """Application configuration handler"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern to ensure single config instance"""
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from TOML file and expand environment variables"""
        # Load .env file first
        env_path = Path(__file__).parent.parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Get the path to deployment.toml (in project root, one level up from src)
        config_path = Path(__file__).parent.parent.parent / "deployment.toml"
        
        # Load TOML configuration
        if config_path.exists():
            self._config = toml.load(config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Expand environment variables in config values
        self._expand_env_vars()
    
    def _expand_env_vars(self, obj=None):
        """
        Recursively expand environment variables in config
        Supports ${VAR_NAME} or $VAR_NAME syntax
        """
        import re
        
        if obj is None:
            obj = self._config
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self._expand_env_vars(value)
        elif isinstance(obj, list):
            return [self._expand_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Replace ${VAR} or $VAR with environment variable value
            def replace_env(match):
                var_name = match.group(1) or match.group(2)
                env_value = os.getenv(var_name)
                
                # If env var not found, keep placeholder
                if env_value is None:
                    return match.group(0)
                
                # Return the string value (don't convert yet)
                return env_value
            
            # Match ${VAR_NAME} or $VAR_NAME
            pattern = r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
            result = re.sub(pattern, replace_env, obj)
            
            # If the entire string is still a placeholder, return None so defaults can be used
            if result.startswith('${') and result.endswith('}'):
                return None
            if result.startswith('$') and result == obj:
                return None
            
            # Convert string booleans and numbers if entire string was replaced
            if result != obj:
                if result.lower() in ('true', 'false'):
                    return result.lower() == 'true'
                try:
                    return int(result)
                except ValueError:
                    pass
            return result
        
        return obj
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            section: Configuration section (e.g., 'database', 'application')
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        value = self._config.get(section, {}).get(key)
        # If value is None (env var not set), use the default
        return value if value is not None else default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section
        
        Args:
            section: Configuration section name
            
        Returns:
            Dictionary containing section configuration
        """
        return self._config.get(section, {})
    
    # Convenience properties for common configurations
    @property
    def db_type(self) -> str:
        # Database type (mysql or oracle)
        return self.get("database", "db_type", "mysql")
    
    @property
    def db_host(self) -> str:
        # Database host
        return self.get("database", "host", "localhost")
    
    @property
    def db_port(self) -> int:
        # Database port
        return self.get("database", "port", 3306)
    
    @property
    def db_username(self) -> str:
        # Database username
        return self.get("database", "username", "")
    
    @property
    def db_password(self) -> str:
        # Database password
        return self.get("database", "password", "")
    
    @property
    def db_database(self) -> str:
        # Database name
        return self.get("database", "database", "")
    
    @property
    def db_service_name(self) -> str:
        # Oracle service name
        return self.get("database", "service_name", "")
    
    @property
    def app_name(self) -> str:
        # Application name
        return self.get("application", "app_name", "FastAPI Application")
    
    @property
    def debug(self) -> bool:
        # Debug mode
        return self.get("application", "debug", False)
    
    @property
    def api_prefix(self) -> str:
        # API prefix path
        return self.get("application", "api_prefix", "/api/v1")
    
    @property
    def cors_origins(self) -> List[str]:
        # CORS allowed origins
        return self.get("cors", "origins", ["*"])
    
    @property
    def server_host(self) -> str:
        # Server host
        return self.get("server", "host", "0.0.0.0")
    
    @property
    def server_port(self) -> int:
        # Server port
        return self.get("server", "port", 8000)
    
    @property
    def server_reload(self) -> bool:
        # Server auto-reload
        return self.get("server", "reload", False)
    
    @property
    def log_level(self) -> str:
        # Logging level
        return self.get("logging", "log_level", "INFO")
    
    @property
    def log_to_file(self) -> bool:
        # Log to file
        return self.get("logging", "log_to_file", True)
    
    @property
    def log_dir(self) -> str:
        # Log directory
        return self.get("logging", "log_dir", "logs")
    
    @property
    def detailed_logs(self) -> bool:
        # Detailed logging with file and line numbers
        return self.get("logging", "detailed_logs", False)
    
    @property
    def rotation_type(self) -> str:
        # Log rotation type: "size" or "time"
        return self.get("logging", "rotation_type", "size")
    
    @property
    def max_bytes(self) -> int:
        # Maximum log file size before rotation (for size-based rotation)
        return self.get("logging", "max_bytes", 10485760)
    
    @property
    def backup_count(self) -> int:
        # Number of backup files to keep (for size-based rotation)
        return self.get("logging", "backup_count", 5)
    
    @property
    def rotation_when(self) -> str:
        # When to rotate logs (for time-based rotation)
        # Options: "S", "M", "H", "D", "midnight", "W0"-"W6"
        return self.get("logging", "rotation_when", "midnight")
    
    @property
    def rotation_interval(self) -> int:
        # Rotation interval (for time-based rotation)
        return self.get("logging", "rotation_interval", 1)
    
    @property
    def rotation_backup_count(self) -> int:
        # Number of backup files to keep (for time-based rotation)
        return self.get("logging", "rotation_backup_count", 30)


# Create singleton instance
config = AppConfig()
