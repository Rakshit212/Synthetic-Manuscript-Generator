import pytest
from pathlib import Path
from src.text.loader import TextLoader

def test_load_text_success(tmp_path):
    # Test valid utf-8 loading
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello\nWorld", encoding="utf-8")
    
    content = TextLoader.load_text(test_file)
    assert content == "Hello\nWorld"

def test_load_text_indic(tmp_path):
    # Test valid Indic unicode
    test_file = tmp_path / "indic.txt"
    test_file.write_text("देवनागरी", encoding="utf-8")
    
    content = TextLoader.load_text(test_file)
    assert content == "देवनागरी"

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        TextLoader.load_text("nonexistent_file.txt")

def test_empty_file(tmp_path):
    test_file = tmp_path / "empty.txt"
    test_file.write_text("   \n  ", encoding="utf-8")
    with pytest.raises(ValueError, match="Input file is empty"):
        TextLoader.load_text(test_file)
