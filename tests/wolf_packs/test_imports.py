def test_wolf_pack_imports():
    import wolf_packs._base as base
    import wolf_packs.BULLISH_WOLF_PACK as b
    import wolf_packs.BEARISH_WOLF_PACK as br
    import wolf_packs.SIDEWAYS_WOLF_PACK as s

    assert hasattr(base, 'WolfPackBase')
    assert hasattr(b, 'BullishWolfPack')
    assert hasattr(br, 'BearishWolfPack')
    assert hasattr(s, 'SidewaysWolfPack')
