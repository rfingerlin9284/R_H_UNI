import os
import importlib
import time

import stochastic


def test_env_vars_do_not_control_random_hex():
    # Ensure env vars do not override or fix run ids
    os.environ["RBOT_RUN_ID"] = "deadbeef"
    os.environ["RBOT_DETERMINISTIC"] = "1"

    # reload module to simulate environment read at import time (if any)
    importlib.reload(stochastic)

    a = stochastic.random_hex(8)
    b = stochastic.random_hex(8)

    # They should be non-empty, hex strings, and highly likely different
    assert isinstance(a, str) and isinstance(b, str)
    assert len(a) == 16 and len(b) == 16
    assert a != "deadbeef" and b != "deadbeef"
    assert a != b
