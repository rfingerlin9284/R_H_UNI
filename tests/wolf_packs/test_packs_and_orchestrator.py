import pytest


def test_packs_import_and_basic_generate():
    # import packs lazily and ensure generate_signals returns expected keys
    from wolf_packs.BULLISH_WOLF_PACK import BullishWolfPack
    from wolf_packs.BEARISH_WOLF_PACK import BearishWolfPack
    from wolf_packs.SIDEWAYS_WOLF_PACK import SidewaysWolfPack

    market = {'last_return': 0.005}

    b = BullishWolfPack()
    sig_b = b.generate_signals(market)
    assert 'side' in sig_b and 'notional' in sig_b

    br = BearishWolfPack()
    sig_br = br.generate_signals({'last_return': -0.01})
    assert 'side' in sig_br and 'notional' in sig_br

    s = SidewaysWolfPack()
    sig_s = s.generate_signals({'last_return': 0.0})
    assert 'side' in sig_s and 'notional' in sig_s


def test_orchestrator_basic_flow():
    from wolf_packs.orchestrator import WolfPackOrchestrator

    orch = WolfPackOrchestrator()
    market = {'last_return': 0.006}
    sig = orch.triage_and_generate(market, account_state={'balance': 10000, 'drawdown_pct': 0.02})
    assert 'regime' in sig and 'side' in sig

    # emergency stop path
    sig2 = orch.triage_and_generate({'last_return': -0.01}, account_state={'balance': 10000, 'drawdown_pct': 0.3})
    assert sig2['side'] == 'hold' and sig2.get('triage') == 'emergency_stop'
