import yaml
from pathlib import Path
from typing import Dict, Any, List

class ScriptRegistry:
    """Registry to load and validate script configurations."""
    
    def __init__(self, config_path: str | Path = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.scripts = self.config.get("scripts", {})
        
    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
            
    def get_script_config(self, script_name: str) -> Dict[str, Any]:
        """
        Retrieves the configuration for a specific script.
        
        Args:
            script_name: The internal name of the script (e.g., 'devanagari').
            
        Returns:
            Dictionary containing the script configuration.
            
        Raises:
            ValueError: If the script is unsupported or disabled.
        """
        script_name = script_name.lower()
        if script_name not in self.scripts:
            raise ValueError(f"Unsupported script: '{script_name}'. Available scripts: {', '.join(self.scripts.keys())}")
            
        script_config = self.scripts[script_name]
        
        if not script_config.get("enabled", False):
            raise ValueError(f"Script '{script_name}' is currently disabled in configuration.")
            
        return script_config

    def discover_fonts(self, script_name: str) -> List[Path]:
        """
        Discovers fonts for a given script based on its config.
        
        Args:
            script_name: The name of the script.
            
        Returns:
            A list of paths to detected font files.
        """
        config = self.get_script_config(script_name)
        font_dir = Path(config.get("font_dir", ""))
        
        if not font_dir.exists() or not font_dir.is_dir():
            print(f"WARNING: Font directory not found: {font_dir}")
            print(f"Please ensure you place compatible TrueType (.ttf) or OpenType (.otf) fonts in {font_dir} (Respecting font licenses).")
            return []
            
        fonts = list(font_dir.glob("*.ttf")) + list(font_dir.glob("*.otf"))
        if not fonts:
            print(f"WARNING: No fonts found in {font_dir}")
            print(f"Please place compatible fonts in {font_dir}.")
            
        return fonts
