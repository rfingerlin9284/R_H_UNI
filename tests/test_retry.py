import sys
import pathlib
import time

# Ensure repo root is on sys.path so local packages import during pytest
repo_root = pathlib.Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from util.retry import retry


def flaky(counter: dict):
    # fails twice then succeeds
    counter['n'] = counter.get('n', 0) + 1
    if counter['n'] < 3:
        raise ValueError('transient')
    return 'ok'


def test_retry_succeeds_after_retries():
    c = {}
    wrapped = retry(tries=4, backoff=0.01, jitter=False)(flaky)
    res = wrapped(c)
    assert res == 'ok'


def test_retry_raises_after_exhaust():
    def always_fail():
        raise RuntimeError('fail')

    wrapped = retry(tries=2, backoff=0.001, jitter=False)(always_fail)
    try:
        wrapped()
        assert False, 'expected exception'
    except RuntimeError:
        assert True
