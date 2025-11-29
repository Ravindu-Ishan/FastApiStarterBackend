"""
Application Startup Banner
"""
from config.app_config import config


def print_banner():
    """Print application startup banner"""
    banner = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     ███████╗ █████╗ ███████╗████████╗ █████╗ ██████╗ ██╗          ║
║     ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║          ║
║     █████╗  ███████║███████╗   ██║   ███████║██████╔╝██║          ║
║     ██╔══╝  ██╔══██║╚════██║   ██║   ██╔══██║██╔═══╝ ██║          ║
║     ██║     ██║  ██║███████║   ██║   ██║  ██║██║     ██║          ║
║     ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝          ║
║                                                                   ║
║                 Starter Template by Raizurai                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    Application: {config.app_name:<45}                                 
    Version:     1.0.0                                               
    Database:    {config.db_type.upper():<45} 
    Log Level:   {config.log_level:<45} 
    Debug Mode:  {'Enabled' if config.debug else 'Disabled':<45}
    Reload:      {'Enabled' if config.server_reload else 'Disabled':<45}
══════════════════════════════════════════════════════════════════════════  
    Server:      http://{config.server_host}:{config.server_port:<38}
    API Docs:    http://{config.server_host}:{config.server_port}/docs{' ' * 33} 
    API Prefix:  {config.api_prefix:<45} 
══════════════════════════════════════════════════════════════════════════
"""
    print(banner)
