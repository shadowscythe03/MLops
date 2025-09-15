from src.preprocessing.clean_articles import clean_text

def test_basic_cleaning():
    raw = "  Hello <b>World</b>!  "
    expected = "Hello World!"
    assert clean_text(raw) == expected

def test_non_ascii_removal():
    raw = "Café naïve résumé"
    expected = "Cafe naive resume"
    assert clean_text(raw) == expected