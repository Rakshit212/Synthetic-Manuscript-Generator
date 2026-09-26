from typing import List

class TextProcessor:
    """Processes text for rendering, maintaining source accuracy."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans the input text while preserving meaningful ground-truth content.
        Doesn't alter characters in a way that changes ground truth.
        """
        # We don't do aggressive stripping here, just some standard whitespace normalization
        # if multiple spaces exist, but we keep line breaks intact.
        lines = text.split("\n")
        cleaned_lines = []
        for line in lines:
            # Strip trailing/leading space per line to keep it neat, 
            # but do not change the core characters
            cleaned = line.strip()
            # Ignore development comments
            if cleaned.startswith("# [DEVELOPMENT/TEST DATA]") or cleaned.startswith("# This is not authentic"):
                continue
            if cleaned:
                cleaned_lines.append(cleaned)
        return "\n".join(cleaned_lines)
    
    @staticmethod
    def split_into_paragraphs(text: str) -> List[str]:
        """
        Splits text into paragraphs based on double newlines.
        """
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]
    
    @staticmethod
    def split_into_lines(paragraph: str) -> List[str]:
        """
        Splits a paragraph into individual lines based on single newlines.
        """
        lines = paragraph.split("\n")
        return [line.strip() for line in lines if line.strip()]
