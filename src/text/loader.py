from pathlib import Path

class TextLoader:
    """Loads text securely while preserving Unicode characters."""
    
    @staticmethod
    def load_text(file_path: str | Path) -> str:
        """
        Loads UTF-8 text from the given file path.
        
        Args:
            file_path: Path to the text file.
            
        Returns:
            The file content as a string.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or cannot be read.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise ValueError(f"Error reading file {path}: {e}")
            
        if not content.strip():
            raise ValueError(f"Input file is empty: {path}")
            
        # Normalize line endings to \n
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        return content
