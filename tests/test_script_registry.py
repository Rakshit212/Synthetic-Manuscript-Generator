import pytest
import yaml
from pathlib import Path
from src.text.script_registry import ScriptRegistry

def test_script_registry_load(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_data = {
        "scripts": {
            "devanagari": {
                "enabled": True,
                "input_file": "dummy.txt",
                "font_dir": "fonts"
            }
        }
    }
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)
        
    registry = ScriptRegistry(config_file)
    assert "devanagari" in registry.scripts

def test_get_script_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_data = {
        "scripts": {
            "test_script": {
                "enabled": True,
                "name": "Test"
            },
            "disabled_script": {
                "enabled": False
            }
        }
    }
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)
        
    registry = ScriptRegistry(config_file)
    
    config = registry.get_script_config("test_script")
    assert config["name"] == "Test"
    
    with pytest.raises(ValueError, match="is currently disabled"):
        registry.get_script_config("disabled_script")
        
    with pytest.raises(ValueError, match="Unsupported script"):
        registry.get_script_config("invalid_script")

def test_discover_fonts(tmp_path):
    config_file = tmp_path / "config.yaml"
    font_dir = tmp_path / "fonts"
    font_dir.mkdir()
    (font_dir / "test1.ttf").touch()
    (font_dir / "test2.otf").touch()
    
    config_data = {
        "scripts": {
            "test": {
                "enabled": True,
                "font_dir": str(font_dir)
            }
        }
    }
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)
        
    registry = ScriptRegistry(config_file)
    fonts = registry.discover_fonts("test")
    assert len(fonts) == 2
