# tests/test_packio_cli.py (example integration test)
import pytest
import subprocess
import os

# Sample.gitignore content
GITIGNORE_CONTENT = """
*.log
build/
venv/
!important.log
"""

# Sample file contents
FILE1_CONTENT = "print('hello')"
FILE2_CONTENT = "# Temporary file"
IMPORTANT_LOG_CONTENT = "This log is important"

def setup_test_directory(tmp_path, use_git=False):
    """Helper function to create a sample directory structure."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text(FILE1_CONTENT, encoding="utf-8")
    (src_dir / "temp.log").write_text("Temporary log data", encoding="utf-8")

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "config.txt").write_text("key=value", encoding="utf-8")

    (tmp_path / "important.log").write_text(IMPORTANT_LOG_CONTENT, encoding="utf-8")
    (tmp_path / "README.md").write_text("# Test Project", encoding="utf-8")

    if use_git:
        # Create.git directory and.gitignore
        (tmp_path / ".git").mkdir() # Simplified mock git dir
        (tmp_path / ".gitignore").write_text(GITIGNORE_CONTENT, encoding="utf-8")
        # In real tests, might need `git init` and `git add` via subprocess
        # to make ls-files work as expected if not mocking subprocess.

def run_packio(cwd, args: list[str]) -> subprocess.CompletedProcess:
    """Runs the packio command via subprocess."""
    command = [sys.executable, "-m", "packio.main"] + args # Or directly use 'packio' if installed editable
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

def test_packio_basic_run(tmp_path):
    """Test basic run outputting to stdout."""
    setup_test_directory(tmp_path)
    result = run_packio(tmp_path, [str(tmp_path)]) # Input dir is tmp_path

    assert result.returncode == 0
    assert "--- File: README.md ---" in result.stdout
    assert "# Test Project" in result.stdout
    assert f"--- File: {os.path.join('src', 'main.py')} ---" in result.stdout
    assert FILE1_CONTENT in result.stdout
    assert f"--- File: {os.path.join('data', 'config.txt')} ---" in result.stdout
    assert "key=value" in result.stdout
    assert "--- File: important.log ---" in result.stdout # Not ignored by default
    assert IMPORTANT_LOG_CONTENT in result.stdout
    assert "temp.log" not in result.stdout # Not explicitly included

def test_packio_with_git_ignore(tmp_path):
    """Test that git ls-files respects.gitignore."""
    setup_test_directory(tmp_path, use_git=True)
    # Mock subprocess if not actually running git init/add
    # For this example, assume git ls-files works conceptually
    # A real test might mock subprocess.run for git ls-files call

    # Mocking example (replace run_packio with direct call + mock):
    # with patch("subprocess.run") as mock_run:
    #     # Configure mock_run to return specific output for 'git ls-files'
    #     mock_process = MagicMock()
    #     mock_process.stdout = "README.md\0src/main.py\0data/config.txt\0important.log\0" # Expected tracked files
    #     mock_process.returncode = 0
    #     mock_run.return_value = mock_process
    #     # Now call the packio function directly, not via subprocess
    #     # packio.main.process_directory(...)

    # Assuming packio uses git ls-files when.git exists:
    result = run_packio(tmp_path, [str(tmp_path)])

    assert result.returncode == 0
    assert "--- File: README.md ---" in result.stdout
    assert f"--- File: {os.path.join('src', 'main.py')} ---" in result.stdout
    assert f"--- File: {os.path.join('data', 'config.txt')} ---" in result.stdout
    assert "--- File: important.log ---" in result.stdout # Explicitly not ignored (!)
    assert "temp.log" not in result.stdout # Ignored by *.log

def test_packio_output_file(tmp_path):
    """Test outputting to a file."""
    setup_test_directory(tmp_path)
    output_file = tmp_path / "output.pack"
    result = run_packio(tmp_path, [str(tmp_path), "-o", str(output_file)])

    assert result.returncode == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "--- File: README.md ---" in content
    assert f"--- File: {os.path.join('src', 'main.py')} ---" in content

def test_packio_ignore_pattern(tmp_path):
    """Test user-provided ignore pattern."""
    setup_test_directory(tmp_path)
    result = run_packio(tmp_path, [str(tmp_path), "--ignore", "*.py"])

    assert result.returncode == 0
    assert "--- File: README.md ---" in result.stdout
    assert f"--- File: {os.path.join('data', 'config.txt')} ---" in result.stdout
    assert "main.py" not in result.stdout # Ignored by pattern
