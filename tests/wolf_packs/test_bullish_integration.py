def test_bullish_integration_basic():
    from wolf_packs.BULLISH_WOLF_PACK import BullishWolfPack

    pack = BullishWolfPack()

    # lightweight synthetic data: list of dicts mimicking rows
    data = [
        {'RSI': 40, 'close': 100, 'SMA_20': 99, 'SMA_50': 98, 'volatility': 1.0},
        {'RSI': 35, 'close': 101, 'SMA_20': 99.5, 'SMA_50': 98.5, 'volatility': 1.2},
    ]

    sig = pack.generate_signals(data)
    assert isinstance(sig, dict)
    assert 'side' in sig and 'notional' in sig
