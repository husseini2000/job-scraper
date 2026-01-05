""" Tests for helper functions. """

import pytest
from core.helpers import slugify_string, save_json, load_json, ensure_dir

def test_slugify_string():
    """ Test slugification of strings.
    Args:
        None
    Returns:
        None
    """

    assert slugify_string("Software Engineer") == "software-engineer"
    assert slugify_string("  Senior Developer  ") == "senior-developer"
    assert slugify_string("C++ Developer") == "c-developer"
    assert slugify_string("Data Scientist @ AI") == "data-scientist-ai"

def test_save_and_load_json(tmp_path):
    """ Test saving and loading JSON data.
    Args:
        tmp_path: Temporary path fixture
    Returns:
        None
    """

    data = {"key": "value", "number": 42}
    filepath = tmp_path / "test.json"

    save_json(data, filepath)
    loaded_data = load_json(filepath)

    assert data == loaded_data

def test_ensure_dir(tmp_path):
    """ Test ensuring a directory exists. 
    Args:
        tmp_path: Temporary path fixture
    Returns:
        None
    """

    dir_path = tmp_path / "new_directory"
    assert not dir_path.exists()

    ensured_path = ensure_dir(dir_path)
    assert ensured_path.exists()
    assert ensured_path.is_dir()