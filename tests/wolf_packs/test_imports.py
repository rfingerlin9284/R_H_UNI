def test_imports():
    # ensure repo root is on sys.path so local packages import during pytest
    import sys, pathlib
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    # simple import smoke test
    try:
        import wolf_packs
    except Exception as e:
        raise AssertionError(f"Import failed: {e}")
    assert True
def test_imports():
    # ensure repo root is on sys.path so local packages import during pytest
    import sys, pathlib
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    # simple import smoke test
    try:
        import wolf_packs
    except Exception as e:
        raise AssertionError(f"Import failed: {e}")
    assert True
