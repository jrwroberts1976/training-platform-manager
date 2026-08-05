from pathlib import Path
from training_manager.utils import markdown_title, numeric_key

def test_numeric_key():
    assert numeric_key(Path("02-example")) < numeric_key(Path("10-example"))

def test_markdown_title():
    assert markdown_title(Path("01-github-actions.md")) == "GitHub Actions"
