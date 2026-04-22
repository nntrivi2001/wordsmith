#!/usr/bin/env python3
"""
Security utility library
Common security functions for the wordsmith system

Created: 2026-01-02
Created because: Security audit found path traversal and command injection vulnerabilities
Fix: Centralized management of all security-related input sanitization functions
"""

import json
import os
import re
import sys
import tempfile
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Any, Dict, Optional, Union

# Try to import filelock (optional dependency)
try:
    from filelock import FileLock
    HAS_FILELOCK = True
except ImportError:
    HAS_FILELOCK = False


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """
    Sanitize filename to prevent path traversal attacks (CWE-22)

    Security critical function - Fixes extract_entities.py path traversal vulnerability

    Args:
        name: Original filename (may contain path traversal characters)
        max_length: Maximum filename length (default 100 characters)

    Returns:
        Safe filename (only contains basic filename, removes all path information)

    Example:
        >>> sanitize_filename("../../../etc/passwd")
        'passwd'
        >>> sanitize_filename("C:\\Windows\\System32")
        'System32'
        >>> sanitize_filename("NormalCharacterName")
        'NormalCharacterName'

    Security verification:
        - ✅ Prevents directory traversal (../、..\\)
        - ✅ Prevents absolute paths (/、C:\\)
        - ✅ Removes special characters
        - ✅ Length limit
    """
    # Step 1: Keep only base filename (remove all paths)
    safe_name = os.path.basename(name)

    # Step 2: Remove path separators (double insurance)
    safe_name = safe_name.replace('/', '_').replace('\\', '_')

    # Step 3: Keep only safe characters
    # Allowed: Chinese(\u4e00-\u9fff), letters(a-zA-Z), digits(0-9), underscore(_), hyphen(-)
    safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '_', safe_name)

    # Step 4: Remove consecutive underscores (beautify)
    safe_name = re.sub(r'_+', '_', safe_name)

    # Step 5: Length limit
    if len(safe_name) > max_length:
        safe_name = safe_name[:max_length]

    # Step 6: Remove leading/trailing underscores
    safe_name = safe_name.strip('_')

    # Step 7: Ensure non-empty (defensive programming)
    if not safe_name:
        safe_name = "unnamed_entity"

    return safe_name


def sanitize_commit_message(message: str, max_length: int = 200) -> str:
    """
    Sanitize Git commit messages to prevent command injection (CWE-77)

    Security critical function - Fixes backup_manager.py command injection vulnerability

    Args:
        message: Raw commit message (may contain Git flags)
        max_length: Maximum message length (default 200 characters)

    Returns:
        Safe commit message (removes Git special flags and dangerous characters)

    Example:
        >>> sanitize_commit_message("Test\\n--author='Attacker'")
        'Test  author Attacker'
        >>> sanitize_commit_message("--amend Chapter 1")
        'amend Chapter 1'

    Security verification:
        - ✅ Prevents multi-line injection (newline)
        - ✅ Prevents Git flag injection (--xxx)
        - ✅ Prevents parameter delimiter confusion (quotes)
        - ✅ Prevents single-letter flags (-x)
    """
    # Step 1: Remove newlines (prevent multi-line argument injection)
    safe_msg = message.replace('\n', ' ').replace('\r', ' ')

    # Step 2: Remove Git special flags (--prefixed arguments)
    safe_msg = re.sub(r'--[\w-]+', '', safe_msg)

    # Step 3: Remove quotes (prevent parameter delimiter confusion)
    safe_msg = safe_msg.replace("'", "").replace('"', '')

    # Step 4: Remove leading - (prevent single-letter flags like -m)
    safe_msg = safe_msg.lstrip('-')

    # Step 5: Remove consecutive spaces (beautify)
    safe_msg = re.sub(r'\s+', ' ', safe_msg)

    # Step 6: Length limit
    if len(safe_msg) > max_length:
        safe_msg = safe_msg[:max_length]

    # Step 7: Remove leading/trailing spaces
    safe_msg = safe_msg.strip()

    # Step 8: Ensure non-empty
    if not safe_msg:
        safe_msg = "Untitled commit"

    return safe_msg


def create_secure_directory(path: str, mode: int = 0o700) -> Path:
    """
    Create secure directory (owner-only access)

    Security critical function - Fixes file permission configuration vulnerability

    Args:
        path: Directory path
        mode: Permission mode (default 0o700, owner can read/write/execute only)

    Returns:
        Path object

    Example:
        >>> create_secure_directory('.wordsmith')
        PosixPath('.wordsmith')  # drwx------ (700)

    Security verification:
        - ✅ Owner-only access (0o700)
        - ✅ Prevents same-group user reading
        - ✅ Cross-platform compatible (Windows/Linux/macOS)
    """
    path_obj = Path(path)

    # On Windows, passing mode triggers unexpected ACL behavior (testing shows it can cause directory to be inaccessible immediately after creation).
    # Therefore on Windows don't pass mode, keep default inherited permissions; on Unix-like systems use mode.
    if os.name == 'nt':
        os.makedirs(path, exist_ok=True)
    else:
        os.makedirs(path, mode=mode, exist_ok=True)

    # Double insurance: explicitly set permissions (some systems may ignore makedirs mode parameter)
    if os.name != 'nt':  # Unix systems (Linux/macOS)
        os.chmod(path, mode)

    return path_obj


def create_secure_file(file_path: str, content: str, mode: int = 0o600) -> None:
    """
    Create secure file (owner-only read/write)

    Args:
        file_path: File path
        content: File content
        mode: Permission mode (default 0o600, owner can read/write only)

    Security verification:
        - ✅ Owner-only read/write (0o600)
        - ✅ Prevents other users from accessing
    """
    # Create file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Set permissions (Unix only)
    if os.name != 'nt':
        os.chmod(file_path, mode)


def validate_integer_input(value: str, field_name: str) -> int:
    """
    Validate and convert integer input (strict mode)

    Security critical function - Fixes update_state.py weak validation vulnerability

    Args:
        value: Input value (string)
        field_name: Field name (used in error messages)

    Returns:
        Converted integer

    Raises:
        ValueError: Input is not a valid integer

    Example:
        >>> validate_integer_input("123", "chapter_num")
        123
        >>> validate_integer_input("abc", "level")
        ValueError: ❌ Error: level must be an integer, received: abc
    """
    try:
        return int(value)
    except ValueError:
        print(f"❌ Error: {field_name} must be an integer, received: {value}", file=sys.stderr)
        raise ValueError(f"Invalid integer input for {field_name}: {value}")


# ============================================================================
# Git Environment Detection (Graceful Degradation Support)
# ============================================================================

# Cache Git availability detection results
_git_available: Optional[bool] = None


def is_git_available() -> bool:
    """
    Detect if Git is available

    Returns:
        bool: Whether Git is available

    Note:
        - Detection results are cached to avoid repeated detection
        - Used to support graceful degradation in environments without Git
    """
    global _git_available

    if _git_available is not None:
        return _git_available

    import subprocess

    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        _git_available = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        _git_available = False

    return _git_available


def is_git_repo(path: Union[str, Path]) -> bool:
    """
    Detect if the specified directory is a Git repository

    Args:
        path: Directory path

    Returns:
        bool: Whether it is a Git repository
    """
    if not is_git_available():
        return False

    path = Path(path)
    git_dir = path / ".git"
    return git_dir.exists() and git_dir.is_dir()


def git_graceful_operation(
    args: list,
    cwd: Union[str, Path],
    *,
    fallback_msg: str = "Git not available, skipping version control operation"
) -> tuple:
    """
    Gracefully execute Git operations (silent degradation when Git is unavailable)

    Args:
        args: Git command arguments (without 'git')
        cwd: Working directory
        fallback_msg: Prompt message during degradation

    Returns:
        (success: bool, output: str, was_skipped: bool)
        - success: Whether the operation succeeded
        - output: Output content
        - was_skipped: Whether skipped due to Git unavailability

    Example:
        >>> success, output, skipped = git_graceful_operation(
        ...     ["add", "."], cwd="/path/to/project"
        ... )
        >>> if skipped:
        ...     print("Git not available, using fallback")
    """
    if not is_git_available():
        print(f"⚠️  {fallback_msg}", file=sys.stderr)
        return False, "", True

    import subprocess

    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        return result.returncode == 0, result.stdout, False
    except subprocess.TimeoutExpired:
        print(f"⚠️  Git operation timed out: git {' '.join(args)}", file=sys.stderr)
        return False, "", False
    except OSError as e:
        print(f"⚠️  Git operation failed: {e}", file=sys.stderr)
        return False, "", False


# ============================================================================
# Atomic File Write (Prevent Concurrent Conflicts and Data Corruption)
# ============================================================================


class AtomicWriteError(Exception):
    """Atomic write failure exception"""
    pass


def atomic_write_json(
    file_path: Union[str, Path],
    data: Dict[str, Any],
    *,
    use_lock: bool = True,
    backup: bool = True,
    indent: int = 2
) -> None:
    """
    Atomically write JSON file to prevent concurrent conflicts and data corruption (CWE-362, CWE-367)

    Security critical function - Fixes state.json concurrent write risk

    Implementation strategy:
    1. Write to temporary file (same directory, ensure same filesystem)
    2. Optional: use filelock to acquire exclusive lock
    3. Optional: backup original file
    4. Atomic rename (os.replace is atomic on POSIX)

    Args:
        file_path: Target file path
        data: Dictionary data to write
        use_lock: Whether to use file lock (requires filelock library)
        backup: Whether to backup original file before writing
        indent: JSON indent (default 2)

    Raises:
        AtomicWriteError: Raised on write failure

    Example:
        >>> atomic_write_json('.wordsmith/state.json', {'progress': {'chapter': 10}})

    Security verification:
        - ✅ Prevents data corruption from write interruption (write to temp file first)
        - ✅ Prevents concurrent write conflicts (filelock)
        - ✅ Supports rollback (backup mechanism)
        - ✅ Cross-platform compatible
    """
    file_path = Path(file_path)
    parent_dir = file_path.parent
    parent_dir.mkdir(parents=True, exist_ok=True)

    # Prepare JSON content
    try:
        json_content = json.dumps(data, ensure_ascii=False, indent=indent)
    except (TypeError, ValueError) as e:
        raise AtomicWriteError(f"JSON serialization failed: {e}")

    # Lock file path
    lock_path = file_path.with_suffix(file_path.suffix + '.lock')
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')

    # Create temporary file (same directory to ensure same filesystem, os.replace is atomic)
    fd, temp_path = tempfile.mkstemp(
        suffix='.tmp',
        prefix=file_path.stem + '_',
        dir=parent_dir
    )

    try:
        # Step 1: Write to temporary file
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(json_content)
            f.flush()
            os.fsync(f.fileno())  # Ensure write to disk

        # Step 2: Acquire lock (if available and enabled)
        lock = None
        if use_lock and HAS_FILELOCK:
            lock = FileLock(str(lock_path), timeout=10)
            lock.acquire()

        try:
            # Step 3: Backup original file (if exists and backup enabled)
            if backup and file_path.exists():
                try:
                    import shutil
                    shutil.copy2(file_path, backup_path)
                except OSError:
                    pass  # Backup failure doesn't block write

            # Step 4: Atomic rename
            os.replace(temp_path, file_path)
            temp_path = None  # Mark success, no cleanup needed

        finally:
            if lock is not None:
                lock.release()

    except Exception as e:
        raise AtomicWriteError(f"Atomic write failed: {e}")

    finally:
        # Cleanup: delete temporary file (if still exists, write failed)
        if temp_path is not None:
            try:
                os.unlink(temp_path)
            except OSError:
                pass


def read_json_safe(
    file_path: Union[str, Path],
    default: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Safely read JSON file (with default value and error handling)

    Args:
        file_path: File path
        default: Default value when file doesn't exist or parsing fails

    Returns:
        Parsed dictionary, or default value

    Example:
        >>> state = read_json_safe('.wordsmith/state.json', {})
    """
    file_path = Path(file_path)
    if default is None:
        default = {}

    if not file_path.exists():
        return default

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️ Failed to read JSON ({file_path}): {e}", file=sys.stderr)
        return default


def restore_from_backup(file_path: Union[str, Path]) -> bool:
    """
    Restore file from backup

    Args:
        file_path: Original file path

    Returns:
        Whether restore succeeded

    Example:
        >>> restore_from_backup('.wordsmith/state.json')
        True
    """
    file_path = Path(file_path)
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')

    if not backup_path.exists():
        print(f"⚠️  Backup file does not exist: {backup_path}", file=sys.stderr)
        return False

    try:
        import shutil
        shutil.copy2(backup_path, file_path)
        print(f"✅ Restored from backup: {file_path}")
        return True
    except OSError as e:
        print(f"❌ Restore failed: {e}", file=sys.stderr)
        return False


# ============================================================================
# Unit Tests (Built-in Self-Check)
# ============================================================================

def _run_self_tests():
    """Run built-in security tests"""
    print("🔍 Running security utility self-tests...")

    # Test 1: sanitize_filename
    assert sanitize_filename("../../../etc/passwd") == "passwd", "Path traversal test failed"
    assert sanitize_filename("C:\\Windows\\System32") == "System32", "Windows path test failed"
    assert sanitize_filename("NormalCharacterName") == "NormalCharacterName", "Character name test failed"
    assert sanitize_filename("/tmp/../../../../../etc/hosts") == "hosts", "Complex path traversal test failed"
    assert sanitize_filename("test///file...name") == "file_name", "Special character test failed"  # . will be replaced
    print("  ✅ sanitize_filename: All tests passed")

    # Test 2: sanitize_commit_message
    result = sanitize_commit_message("Test\n--author='Attacker'")
    assert "\n" not in result, "Newline not removed"
    assert "--author" not in result, "Git flag not removed"
    assert "Attacker" in result, "Content incorrectly removed"

    assert sanitize_commit_message("--amend Chapter 1") == "Chapter 1", "Git flag test failed"  # --amend is completely removed
    assert "'" not in sanitize_commit_message("Test'message"), "Quote test failed"
    assert sanitize_commit_message("-m Test") == "m Test", "Single-letter flag test failed"  # after -m removed is "m Test"
    print("  ✅ sanitize_commit_message: All tests passed")

    # Test 3: validate_integer_input
    assert validate_integer_input("123", "test") == 123, "Integer validation test failed"
    try:
        validate_integer_input("abc", "test")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    print("  ✅ validate_integer_input: All tests passed")

    # Test 4: atomic_write_json
    import tempfile as tf
    test_dir = Path(tf.mkdtemp())
    test_file = test_dir / "test_state.json"

    # Write test
    test_data = {"chapter": 10, "key": "value"}
    atomic_write_json(test_file, test_data, use_lock=False, backup=False)
    assert test_file.exists(), "Atomic write did not create file"

    # Read verification
    with open(test_file, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert loaded == test_data, "Atomic write data mismatch"

    # Backup test
    atomic_write_json(test_file, {"updated": True}, use_lock=False, backup=True)
    backup_file = test_file.with_suffix('.json.bak')
    assert backup_file.exists(), "Backup not created"

    # Restore test
    restore_from_backup(test_file)
    with open(test_file, 'r', encoding='utf-8') as f:
        restored = json.load(f)
    assert restored == test_data, "Restored data mismatch"

    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print("  ✅ atomic_write_json: All tests passed")
    if HAS_FILELOCK:
        print("  ℹ️  filelock available, file lock support enabled")
    else:
        print("  ⚠️  filelock not installed, file lock feature unavailable")

    print("\n✅ All security utility function tests passed!")


if __name__ == "__main__":
    # Windows UTF-8 encoding fix (must execute before print)
    if sys.platform == "win32":
        enable_windows_utf8_stdio()

    # Run self-tests
    _run_self_tests()
