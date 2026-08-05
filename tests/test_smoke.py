from pathlib import Path
from training_manager.utils import numeric_key
def test_numeric_sort():
    assert numeric_key(Path("02-two")) < numeric_key(Path("10-ten"))
