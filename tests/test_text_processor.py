from src.text.processor import TextProcessor

def test_clean_text():
    text = "# [DEVELOPMENT/TEST DATA]\n   \nLine 1   \nLine 2\n"
    cleaned = TextProcessor.clean_text(text)
    assert cleaned == "Line 1\nLine 2"

def test_split_into_paragraphs():
    text = "Paragraph 1\n\nParagraph 2\n\n\nParagraph 3"
    paragraphs = TextProcessor.split_into_paragraphs(text)
    assert len(paragraphs) == 3
    assert paragraphs[0] == "Paragraph 1"
    assert paragraphs[1] == "Paragraph 2"
    assert paragraphs[2] == "Paragraph 3"

def test_split_into_lines():
    paragraph = "Line 1\nLine 2\nLine 3"
    lines = TextProcessor.split_into_lines(paragraph)
    assert len(lines) == 3
    assert lines[0] == "Line 1"
    assert lines[2] == "Line 3"

def test_source_preservation():
    # Ensure Indic chars are preserved exactly, no weird normalization stripping
    text = "देवनागरी\n𑘦𑘻𑘚𑘲"
    cleaned = TextProcessor.clean_text(text)
    assert cleaned == text
