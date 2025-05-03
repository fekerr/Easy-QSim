# tests/test_packio_utils.py (example unit test)
import pytest
from unittest.mock import patch, MagicMock
from packio import file_utils # Assuming file_utils contains filtering logic

def test_apply_filters_simple_ignore():
    """Test basic ignore pattern."""
    files = ["a.py", "b.txt", "c.py", "subdir/d.py"]
    include =
    ignore = ["*.txt"]
    expected = ["a.py", "c.py", "subdir/d.py"]
    result = file_utils.apply_filters(files, include, ignore)
    assert sorted(result) == sorted(expected)

def test_apply_filters_include_and_ignore():
    """Test interaction of include and ignore patterns."""
    files = ["a.py", "b.txt", "c.md", "docs/manual.md", "src/main.py"]
    include = ["*.py", "*.md"]
    ignore = ["docs/*"]
    expected = ["a.py", "c.md", "src/main.py"] # docs/manual.md ignored
    result = file_utils.apply_filters(files, include, ignore)
    assert sorted(result) == sorted(expected)

# Example mocking os.walk (if testing list_files_recursive)
@patch("os.walk")
def test_list_files_recursive(mock_walk):
    """Test recursive file listing using mocked os.walk."""
    mock_walk.return_value = [
        ('/project', ['subdir'], ['file1.txt']),
        ('/project/subdir',, ['file2.py']),
    ]
    expected = ["file1.txt", os.path.join("subdir", "file2.py")]
    result = file_utils.list_files_recursive("/project")
    # Normalize paths for cross-platform comparison if necessary
    result_normalized = [p.replace(os.sep, '/') for p in result]
    expected_normalized = [p.replace(os.sep, '/') for p in expected]
    assert sorted(result_normalized) == sorted(expected_normalized)
    mock_walk.assert_called_once_with("/project")
